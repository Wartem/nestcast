from flask import Flask, render_template, request, jsonify
from chromecast_utils import discover_devices, send_message_to_device, serve_audio_file
from threading import Thread
import time

app = Flask(__name__)

devices = []

def background_discovery():
    global devices
    while True:
        devices = discover_devices()
        time.sleep(300)  # Discover devices every 5 minutes

@app.route('/')
def index():
    return render_template('index.html', devices=devices)

@app.route('/api/devices')
def get_devices():
    return jsonify(devices)

@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message')
    device_names = data.get('devices', [])
    
    results = []
    for device_name in device_names:
        try:
            Thread(target=send_message_to_device, args=(device_name, message)).start()
            results.append({"device": device_name, "status": "Message sending initiated"})
        except Exception as e:
            results.append({"device": device_name, "status": "Error", "message": str(e)})
    
    return jsonify({"results": results})

@app.route('/api/discover', methods=['POST'])
def trigger_discovery():
    global devices
    devices = discover_devices()
    return jsonify({"status": "Discovery completed", "devices": devices})

@app.route('/audio/<filename>')
def audio(filename):
    return serve_audio_file(filename)

if __name__ == '__main__':
    Thread(target=background_discovery, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=True)