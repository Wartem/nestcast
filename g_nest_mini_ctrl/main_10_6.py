import pychromecast
from pychromecast.controllers.media import MediaController
import time
from gtts import gTTS
import os
import tempfile
import http.server
import socketserver
import threading
import socket

def start_local_server(directory, start_port=8000):
    """ Start a local HTTP server to serve the audio files. """
    for port in range(start_port, start_port + 100):  # Try up to 100 ports
        handler = http.server.SimpleHTTPRequestHandler
        try:
            with socketserver.TCPServer(("", port), handler) as httpd:
                print(f"Serving files from {directory} on port {port}")
                return httpd, port
        except OSError:
            print(f"Port {port} is in use, trying next...")
    raise RuntimeError("Unable to find an open port")

def find_google_nest(name):
    """ Find Google Nest Mini by name. """
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[name])
    if chromecasts:
        cast = chromecasts[0]
        cast.wait()
        print(f"Found: {cast.name}")
        return cast
    else:
        print(f"Could not find a Google Nest Mini device named {name}")
        return None

def send_message(cast, message, server_ip, server_port):
    if not cast:
        print("No Google Nest Mini available, skipping message.")
        return

    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
        tts = gTTS(text=message, lang='sv')
        tts.save(fp.name)
        audio_file = fp.name

    mc = cast.media_controller
    cast.set_volume(0.5)  # Set volume to 50%

    try:
        print("Attempting to play media")
        audio_url = f"http://{server_ip}:{server_port}/{os.path.basename(audio_file)}"
        mc.play_media(audio_url, "audio/mp3")
        print(f"Media play command sent: {audio_url}")
        
        # Wait for the media to start playing
        mc.block_until_active(timeout=10)
        print(f"Playing message: {message}")

        # Wait until the message has finished playing
        while mc.status.player_state != 'IDLE':
            time.sleep(0.5)
            mc.update_status()
            if mc.status.player_state == 'IDLE':
                break
        
        print(f"Finished playing message on {cast.name}")
    except Exception as e:
        print(f"An error occurred while playing the message: {e}")
    finally:
        os.unlink(audio_file)

def discover_all_devices():
    """ Discover all available Chromecast devices. """
    services, browser = pychromecast.discovery.discover_chromecasts()
    if services:
        print(f"Found {len(services)} device(s)")
        for service in services:
            print(f"Device: {service.friendly_name}, IP: {service.host}")
    else:
        print("No devices found")
    pychromecast.discovery.stop_discovery(browser)

def main():
    discover_all_devices()
    
    local_ip = socket.gethostbyname(socket.gethostname())
    temp_dir = tempfile.gettempdir()
    
    try:
        httpd, server_port = start_local_server(temp_dir)
        try:
            server_thread = threading.Thread(target=httpd.serve_forever)
        except ValueError as e:
            print(f"Error starting server: {e}")
            exit
        
        server_thread.daemon = True
        server_thread.start()

        # Wait for the server to start
        time.sleep(2)

        device_names = ["Brygghuset", "Kökets nest", "Matrummet", "Sovrummet", "Mårtens rum"]
        for name in device_names:
            nest_mini = find_google_nest(name)
            if nest_mini:
                send_message(nest_mini, f"Hej från din Raspberry Pi till {name}!", local_ip, server_port)
            time.sleep(2)  # Add a small delay between devices
        print("Finished sending messages to all devices")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'httpd' in locals():
            httpd.shutdown()
            httpd.server_close()

if __name__ == "__main__":
    main()
