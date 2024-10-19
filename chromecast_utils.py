# chromecast_utils_oct.py

import pychromecast
import time
import ipaddress
import os
import tempfile
import socket
import threading
import queue
from flask import send_file
from logger_utils import chromecast_logger
from tts_handler import create_audio_file_gtts, delete_audio_file, create_custom_audio_file_edge

PORT = 5030

# Create logger
#chromecast_logger = setup_logger('chromecast', 'logs/chromecast.log')

# Global dictionary to store audio file paths and their deletion timers
audio_files = {}

class MessageQueue:
    def __init__(self):
        self.queue = queue.Queue()

    def put(self, item):
        self.queue.put(item)

    def get(self):
        return self.queue.get()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception as e:
        chromecast_logger.error(f"Error getting local IP: {str(e)}")
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def discover_devices():
    try:
        services, browser = pychromecast.discovery.discover_chromecasts()
        pychromecast.discovery.stop_discovery(browser)
        devices = [{"name": service.friendly_name, "ip": service.host} for service in services]
        
        # Keep only the first occurrence of each IP address
        devices = [next(d for d in devices if d['ip'] == ip) for ip in {d['ip'] for d in devices}]
        
        # Sort devices by IP address
        sorted_devices = sorted(devices, key=lambda d: ipaddress.ip_address(d['ip']))
        
        return sorted_devices
    except Exception as e:
        chromecast_logger.error(f"Error discovering devices: {str(e)}")
        return []

def send_message_to_device(device_name, message, volume, lang='en'):
    chromecast_logger.info(f"Sending message to {device_name} in language {lang} with volume {volume}")
    try:
        local_ip = get_local_ip()
        chromecast_logger.info(f"Local IP: {local_ip}")
        
        chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[device_name])
        if not chromecasts:
            raise ValueError(f"Device '{device_name}' not found")
        
        cast = chromecasts[0]
        cast.wait()
        chromecast_logger.info(f"Connected to device {device_name}")

        audio_file = create_custom_audio_file_edge(message, lang)
        chromecast_logger.info(f"Created audio file: {audio_file}")
        
        mc = cast.media_controller
        cast.set_volume(volume)
        chromecast_logger.info(f"Set volume to {volume}")

        audio_url = f"http://{local_ip}:{PORT}/audio/{os.path.basename(audio_file)}"
        chromecast_logger.info(f"Audio URL: {audio_url}")
        
        mc.play_media(audio_url, "audio/mp3")
        mc.block_until_active()
        chromecast_logger.info(f"Started playing audio on {device_name}")
        
        global audio_files
        audio_files[audio_file] = threading.Timer(3600.0, delete_audio_file, args=[audio_file])
        audio_files[audio_file].start()

        # Wait for the audio to finish playing
        while mc.status.player_state != 'IDLE':
            time.sleep(1)

        chromecast_logger.info(f"Message sent successfully to {device_name}")
    except Exception as e:
        chromecast_logger.error(f"Error sending message to {device_name}: {str(e)}")
        raise
        

def serve_audio_file(filename):
    filepath = os.path.join(tempfile.gettempdir(), filename)
    if os.path.exists(filepath):
        return send_file(filepath, mimetype="audio/mp3", conditional=True)
    else:
        chromecast_logger.warning(f"Audio file not found: {filepath}")
        return "File not found", 404
    
def pause_audio_on_device(device_name):
    chromecast_logger.info(f"Pause audio requested on {device_name}")
    try:
        chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[device_name])
        if not chromecasts:
            raise ValueError(f"Device '{device_name}' not found")

        cast = chromecasts[0]
        cast.wait()
        mc = cast.media_controller
        
        """ 
        "PLAYING"
        "BUFFERING"
        "PAUSED"
        "IDLE"
        "UNKNOWN" """

        if mc.status.player_state != 'IDLE':
            mc.pause()
            chromecast_logger.info(f"Message paused on {device_name} with state {mc.status.player_state}")
        else:
            chromecast_logger.warning(f"Cannot pause: Device '{device_name}' is in state {mc.status.player_state}")
    except Exception as e:
        chromecast_logger.error(f"Error pausing message on {device_name}: {str(e)}")
        raise
    finally:
        pychromecast.discovery.stop_discovery(browser)

def stop_audio_on_device(device_name):
    chromecast_logger.info(f"Stop audio requested on {device_name}")
    try:
        chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[device_name])
        if not chromecasts:
            raise ValueError(f"Device '{device_name}' not found")

        cast = chromecasts[0]
        cast.wait()
        mc = cast.media_controller

        if mc.status.player_state not in ["IDLE"]: # ['PLAYING', 'PAUSED']:
            mc.stop()
            chromecast_logger.info(f"Audio stopped on {device_name}")
        else:
            chromecast_logger.warning(f"Cannot stop: Device '{device_name}' is in state {mc.status.player_state}")
    except Exception as e:
        chromecast_logger.error(f"Error stopping audio on {device_name}: {str(e)}")
        raise
    finally:
        pychromecast.discovery.stop_discovery(browser)