# app.py

from flask import Flask, render_template, request, jsonify, current_app
from chromecast_utils import discover_devices, send_message_to_device, serve_audio_file, get_local_ip
from chromecast_utils import MessageQueue, pause_audio_on_device, stop_audio_on_device, PORT
from threading import Thread
import time
import json, tempfile, os
import logging
from urllib.parse import urlparse, parse_qs, unquote
from logging.handlers import RotatingFileHandler
import pychromecast
import requests

app = Flask(__name__, template_folder='templates', static_folder='static')

devices = []
message_queue = MessageQueue()
device_ip = {}

def load_device_ip():
    with current_app.open_resource('static/json/device_ip.json') as f:
        return json.load(f)

# Set up logging with rotation
def setup_logger(name, log_file, level=logging.INFO):
    handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Create loggers
app_logger = setup_logger('app', 'logs/app.log')

def background_discovery():
    global devices
    while True:
        try:
            devices = discover_devices()
            # Irritating logging
            # app_logger.info(f"Discovered {len(devices)} devices")
        except Exception as e:
            app_logger.error(f"Error in device discovery: {str(e)}")
        time.sleep(300)  # Discover devices every 5 minutes

def process_queue():
    while True:
        message, device_name, volume, language = message_queue.get()
        try:
            volume = validate_volume(volume)
            send_message_to_device(device_name, message, volume, language)
            app_logger.info(f"Message sent to {device_name}")
        except Exception as e:
            app_logger.error(f"Error sending message to {device_name}: {str(e)}")
        time.sleep(1)  # Small delay to prevent overloading

def validate_volume(volume):
    print("input volume:", volume)
    try:
        volume = float(volume)
        if 0.0 <= volume <= 1.0:
            return volume
    except (TypeError, ValueError):
        pass
    app_logger.warning(f"Invalid volume {volume}, using default 0.5")
    return 0.5

def is_youtube_url(url):
    return 'youtube.com' in url or 'youtu.be' in url

def extract_youtube_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
        if parsed_url.path.startswith(('/embed/', '/v/')):
            return parsed_url.path.split('/')[2]

    return None

def determine_content_type(url):
    if is_youtube_url(url):
        video_id = extract_youtube_video_id(url)
        if video_id:
            return f'https://www.youtube.com/embed/{video_id}', 'video/youtube'
        else:
            raise ValueError("Unable to extract YouTube video ID")

    # Define known file extensions and their corresponding MIME types
    mime_types = {
        'mp4': 'video/mp4',
        'mp3': 'audio/mpeg',
        'wav': 'audio/wav',
        'ogg': 'audio/ogg',
        'webm': 'video/webm',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif'
    }

    # Parse the URL
    parsed_url = urlparse(unquote(url))
    path = parsed_url.path.lower()

    # Check for known extensions in the path
    for ext, mime_type in mime_types.items():
        if path.endswith(f'.{ext}'):
            app_logger.info(f"Determined content type from path: audio/{mime_type} for URL: {url}")
            return url, mime_type

    # If no extension found in path, try HEAD request
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        content_type = response.headers.get('content-type', '').lower()
        
        if content_type:
            # Check if the content type is an image type
            if content_type.startswith('image/'):
                app_logger.info(f"Determined image content type from HEAD request: {content_type} for URL: {url}")
                return url, content_type
            
            app_logger.info(f"Determined content type from HEAD request: {content_type} for URL: {url}")
            return url, content_type
    except requests.RequestException as e:
        app_logger.error(f"Error in HEAD request: {str(e)}")

    # If all else fails, try to guess the content type from the URL
    for ext, mime_type in mime_types.items():
        if f'.{ext}' in url.lower():
            app_logger.info(f"Guessed content type from URL: {mime_type} for URL: {url}")
            return url, mime_type

    # If still unable to determine, default to application/octet-stream
    app_logger.warning(f"Could not determine content type, defaulting to application/octet-stream for URL: {url}")
    return url, 'application/octet-stream'

def get_chromecast_device(device_name, chromecasts):
    """Get the Chromecast device by name or fallback to device_ip."""
    chromecast = next((cc for cc in chromecasts if cc.name == device_name), None)

    if not chromecast:
        # If the device is not found, check the device_ip dictionary
        if device_name in device_ip:
            ip_address = device_ip[device_name]
            app_logger.info(f"Device {device_name} not found in discovered devices, using IP from device_ip: {ip_address}")
            chromecast = pychromecast.Chromecast(ip_address)
            chromecast.wait()
        else:
            app_logger.error(f"Device {device_name} not found")
            raise ValueError(f"Device {device_name} not found")

    return chromecast

@app.route('/')
def index():
    return render_template('index.html', devices=devices)

@app.route('/api/devices')
def get_devices():
    return jsonify(devices)

@app.route('/api/send_message', methods=['POST'])
def send_message():
    app_logger.info("Received request to /api/send_message")
    message = request.form.get('message')
    volume = request.form.get('volume')
    language = request.form.get('language', 'en')  # Default to English
    device_names = json.loads(request.form.get('devices', '[]'))
    
    app_logger.info(json.dumps(request.form.to_dict()))
    
    app_logger.info(f"Message: {message}, Volume: {volume} Language: {language}, Devices: {device_names}")
    
    volume = validate_volume(volume)
    
    if not message or not device_names:
        error_msg = "Missing message or devices"
        app_logger.error(error_msg)
        return jsonify({"status": "Error", "message": error_msg}), 400
    
    results = []
    for device_name in device_names:
        try:
            app_logger.info(f"Attempting to send message to {device_name}")
            send_message_to_device(device_name, message, volume, language)
            results.append({"device": device_name, "status": "Message sent"})
            app_logger.info(f"Message sent successfully to {device_name}")
        except Exception as e:
            error_msg = f"Error sending message to {device_name}: {str(e)}"
            app_logger.error(error_msg)
            results.append({"device": device_name, "status": "Error", "message": str(e)})
    
    return jsonify({"results": results})

@app.route('/api/discover', methods=['POST'])
def trigger_discovery():
    global devices
    try:
        devices = discover_devices()
        app_logger.info(f"Manual discovery completed, found {len(devices)} devices")
        return jsonify({"status": "Discovery completed", "devices": devices})
    except Exception as e:
        app_logger.error(f"Error in manual device discovery: {str(e)}")
        return jsonify({"status": "Error", "message": str(e)}), 500
    
def get_chromecast_device(device_name, chromecasts):
    """Get the Chromecast device by name or fallback to device_ip."""
    chromecast = next((cc for cc in chromecasts if cc.name == device_name), None)
    
    if not chromecast:
        # If the device is not found, check the device_ip dictionary
        if device_name in device_ip:
            ip_address = device_ip[device_name]
            app_logger.info(f"Device {device_name} not found in discovered devices, using IP from device_ip: {ip_address}")
            chromecast = pychromecast.Chromecast(ip_address)
            chromecast.wait()
        else:
            app_logger.error(f"Device {device_name} not found")
            raise ValueError(f"Device {device_name} not found")
    
    return chromecast

@app.route('/api/stream_media', methods=['POST'])
def stream_media():
    media_url = request.form.get('media_url')
    provided_content_type = request.form.get('content_type')
    volume = request.form.get('volume', 0.5)
    device_names = json.loads(request.form.get('devices', '[]'))
    app_logger.info(f"Received request: media_url='{media_url}', content_type='{provided_content_type}', volume={volume}, devices={device_names}")
    
    try:
        media_url, determined_content_type = determine_content_type(media_url)
        
        # Use the determined content type for images, otherwise use provided content type if available
        if determined_content_type.startswith('image/'):
            content_type = determined_content_type
        else:
            content_type = provided_content_type if provided_content_type else determined_content_type
        
        app_logger.info(f"Using content type: {content_type} for URL: {media_url}")
    except Exception as e:
        app_logger.error(f"Error determining content type: {str(e)}")
        return jsonify({"status": "Error", "message": f"Error determining content type: {str(e)}"}), 400
    
    results = []
    chromecasts, browser = pychromecast.get_chromecasts()
    for device_name in device_names:
        try:
            chromecast = get_chromecast_device(device_name, chromecasts)
            chromecast.wait()
            mc = chromecast.media_controller
            
            # Set volume for all content types
            chromecast.set_volume(float(volume))
            
            mc.play_media(media_url, content_type)
            mc.block_until_active(timeout=10)
            results.append({"device": device_name, "status": "Media streaming started"})
            app_logger.info(f"Media streaming started on {device_name} with content type: {content_type}")
        except Exception as e:
            results.append({"device": device_name, "status": "Error", "message": str(e)})
            app_logger.error(f"Error streaming media to {device_name}: {str(e)}")
    
    return jsonify({"results": results})

@app.route('/api/play_audio', methods=['POST'])
def play_audio():
    app_logger.info("Received request to /api/play_audio")
    if 'audio' not in request.files:
        app_logger.error("No audio file provided")
        return jsonify({"status": "Error", "message": "No audio file provided"}), 400
    
    audio_file = request.files['audio']
    devices = json.loads(request.form.get('devices', '[]'))
    volume = float(request.form.get('volume', 0.5))
    
    app_logger.info(f"/api/play_audio devices: {devices}, volume: {volume}")
    
    if not audio_file or not audio_file.filename or not devices:
        error_str = "Invalid request"
        app_logger.error(error_str)
        return jsonify({"status": "Error", "message": error_str}), 400

    # Check file extension and set appropriate MIME type
    file_extension = os.path.splitext(audio_file.filename)[1].lower()
    mime_types = {
        '.mp3': 'audio/mp3',
        '.wav': 'audio/wav',
        '.ogg': 'audio/ogg',
        '.flac': 'audio/flac',
        '.aac': 'audio/aac',
        '.m4a': 'audio/mp4',
        '.wma': 'audio/x-ms-wma'
    }
    
    if file_extension not in mime_types:
        error_str = f"Unsupported audio format: {file_extension}"
        app_logger.error(error_str)
        return jsonify({"status": "Error", "message": error_str}), 400

    mime_type = mime_types[file_extension]

    # Save the file temporarily
    temp_dir = tempfile.gettempdir()
    filename = os.path.join(temp_dir, audio_file.filename)
    app_logger.info(f"Saving the audio file temporarily @ {temp_dir}, filename: {audio_file.filename}")
    audio_file.save(filename)

    results = []
    chromecasts, browser = pychromecast.get_chromecasts()
    for device_name in devices:
        try:
            # Find the Chromecast device
            chromecast = next((cc for cc in chromecasts if cc.name == device_name), None)
            if not chromecast:
                app_logger.error(f"Device {device_name} not found")
                ip_address = device_ip[device_name]
                app_logger.info(f"Device {device_name} not found in discovered devices, using IP from device_ip: {ip_address}")
                chromecast = pychromecast.Chromecast(ip_address) 
                   
            if not chromecast:
                raise ValueError(f"Device {device_name} not found")

            # Connect to the Chromecast
            chromecast.wait()
            mc = chromecast.media_controller

            # Play the audio file
            local_ip = get_local_ip()
            chromecast.set_volume(volume)
            mc.play_media(f'http://{local_ip}:{PORT}/audio/{os.path.basename(filename)}', f"audio/{mime_type}")
            mc.block_until_active()

            results.append({"device": device_name, "status": "Audio playback started"})
            app_logger.info(f"Audio playback started on {device_name}")
        except Exception as e:
            results.append({"device": device_name, "status": "Error", "message": str(e)})
            app_logger.error(f"Error playing audio on {device_name}: {str(e)}")

    return jsonify({"results": results})

@app.route('/audio/<filename>')
def audio(filename):
    return serve_audio_file(filename)
    
@app.route('/api/pause_audio', methods=['POST'])
def pause_audio():
    data = request.json
    devices = data.get('devices', [])
    results = []
    for device in devices:
        try:
            pause_audio_on_device(device)
            results.append({"device": device, "status": "Message paused"})
        except Exception as e:
            results.append({"device": device, "status": "Error", "message": str(e)})
    return jsonify({"results": results})

@app.route('/api/stop_audio', methods=['POST'])
def stop_audio():
    data = request.json
    devices = data.get('devices', [])
    results = []
    for device in devices:
        try:
            stop_audio_on_device(device)
            results.append({"device": device, "status": "Message stopped"})
        except Exception as e:
            results.append({"device": device, "status": "Error", "message": str(e)})
    return jsonify({"results": results})

if __name__ == '__main__':
    Thread(target=background_discovery, daemon=True).start()
    Thread(target=process_queue, daemon=True).start()
    app.run(host='0.0.0.0', port=PORT, debug=True)
    
@app.route('/api/set_volume', methods=['POST'])
def set_volume():
    pass

@app.route('/api/resume_audio', methods=['POST'])
def resume_audio():
    pass