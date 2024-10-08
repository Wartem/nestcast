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

class AudioHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self):
        if self.path.startswith('/'):
            self.path = os.path.join(self.directory, self.path[1:])
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def start_local_server(directory, start_port=8000):
    for port in range(start_port, start_port + 100):  # Try up to 100 ports
        handler = lambda *args, **kwargs: AudioHandler(*args, directory=directory, **kwargs)
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
    """ Send a message to a Google Nest Mini device for playback. """
    if not cast:
        print("No Google Nest Mini available")
        return

    # Create a temporary file to store the audio
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
        mc.block_until_active()
        print(f"Playing message: {message}")

        # Wait until the message has finished playing
        start_time = time.time()
        while mc.status.player_state != 'IDLE':
            if time.time() - start_time > 30:  # 30 seconds timeout
                print("Timeout waiting for message to finish playing")
                break
            time.sleep(0.5)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up the temporary file
        os.unlink(audio_file)

def discover_all_devices():
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
    
    # Start a local server
    local_ip = get_local_ip()
    temp_dir = tempfile.gettempdir()
    
    try:
        httpd, server_port = start_local_server(temp_dir)
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        # Wait a moment for the server to start
        time.sleep(1)

        # Try to find by name
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

if __name__ == "__main__":
    main()