import pychromecast
import time
from gtts import gTTS
import os
import tempfile
import socket
from flask import send_file
import threading

# Global dictionary to store audio file paths and their deletion timers
audio_files = {}

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def discover_devices():
    services, browser = pychromecast.discovery.discover_chromecasts()
    pychromecast.discovery.stop_discovery(browser)
    return [{"name": service.friendly_name, "ip": service.host} for service in services]

def create_audio_file(message):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3', dir=tempfile.gettempdir()) as fp:
        tts = gTTS(text=message, lang='sv')
        tts.save(fp.name)
        return fp.name

def delete_audio_file(filepath):
    global audio_files
    if os.path.exists(filepath):
        os.unlink(filepath)
    if filepath in audio_files:
        del audio_files[filepath]

def send_message_to_device(device_name, message):
    try:
        local_ip = get_local_ip()
        
        # Find the device by name
        chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[device_name])
        if not chromecasts:
            raise ValueError(f"Device '{device_name}' not found")
        
        cast = chromecasts[0]
        cast.wait()

        audio_file = create_audio_file(message)
        mc = cast.media_controller
        cast.set_volume(0.8)

        audio_url = f"http://{local_ip}:5000/audio/{os.path.basename(audio_file)}"
        mc.play_media(audio_url, "audio/mp3")
        mc.block_until_active()

        # Store the audio file path and set a timer to delete it after 60 seconds
        global audio_files
        audio_files[audio_file] = threading.Timer(60.0, delete_audio_file, args=[audio_file])
        audio_files[audio_file].start()

        while mc.status.player_state != 'IDLE':
            time.sleep(0.1)

        print(f"Message sent successfully to {device_name}")
    except Exception as e:
        print(f"Error sending message to {device_name}: {str(e)}")

# Add a route to serve audio files
def serve_audio_file(filename):
    filepath = os.path.join(tempfile.gettempdir(), filename)
    if os.path.exists(filepath):
        return send_file(filepath, conditional=True)
    else:
        return "File not found", 404