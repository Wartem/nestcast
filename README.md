# NestCast

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-green.svg)](https://flask.palletsprojects.com/en/3.0.x/)
[![pychromecast](https://img.shields.io/badge/pychromecast-14.0.4-orange.svg)](https://github.com/home-assistant-libs/pychromecast)
[![Edge-TTS](https://img.shields.io/badge/Edge--TTS-latest-yellow.svg)](https://github.com/rany2/edge-tts)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)

NestCast is a Flask-based web application designed to run on a Raspberry Pi, enabling users to send text-to-speech messages, stream media, and control audio playback on Chromecast-enabled devices within their local network. The application provides a simple web interface for device discovery and message sending, primarily targeting Google Nest devices with built-in Chromecast functionality.

<p align="center">
  <img src="https://github.com/user-attachments/assets/90e337bb-31bc-448e-9086-851e86db30db" alt="GUI" max-width="600">
</p>

## Table of Contents

- [Key Features](#key-features)
- [Technical Details](#technical-details)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Key Features

- **Device Compatibility**: Works with a wide range of Google Nest devices, including smart displays and speakers such as Google Nest Hub, Nest Hub Max, and Nest Audio.
- **Primary Focus**: Tested specifically with Google Nest Mini devices, but compatible with various Chromecast-enabled products.
- **Tested Devices**: Verified functionality on Google Nest Mini (Gen 1) and Google Chromecast (Gen 2).
- **Local Network Operation**: Designed to operate within the user's local network, leveraging Chromecast capabilities.
- **Web Interface**: Offers an intuitive interface for device discovery and message sending.
- **Text-to-Speech**: Converts user-input text into spoken messages on target devices using Edge TTS.
- **Media Streaming**: Supports streaming of audio, video, and images from URLs to Chromecast-enabled screens.
- **Audio Playback**: Enables playing audio files on selected devices.
- **Audio Control**: Allows pausing and stopping audio on devices.
- **Language Support**: Enables sending messages in different languages.
- **Volume Control**: Allows setting custom volume levels for messages.
- **Google Chrome Extension**: Provides a browser extension for quick access to NestCast features (requires customization for your environment).

## Technical Details

- **Framework**: Built using Flask, a lightweight Python web framework.
- **Platform**: Optimized for deployment on Raspberry Pi.
- **Authentication**: Operates without requiring user authentication, simplifying local network use.
- **Device Discovery**: Utilizes pychromecast for automatic discovery of Chromecast devices.
- **Background Processing**: Implements threading for device discovery and message queue processing.
- **Logging**: Incorporates rotating log files for better debugging and monitoring.

### Device Discovery

The application uses the `pychromecast` library to discover Google Nest devices on the local network. Device discovery runs in the background every 5 minutes to keep the device list up-to-date.

### Text-to-Speech

Text messages are converted to speech using the `edge-tts` (Microsoft Edge Text-to-Speech) library. The resulting audio files are temporarily stored on the Raspberry Pi.

### Audio Serving

The Flask application serves the generated audio files to the Google Nest devices. Audio files are kept for 1 hour after creation to ensure they are available for playback, then automatically deleted to conserve storage space.

### Threading

The application uses Python's threading module to handle background tasks such as device discovery and message sending. This allows the web interface to remain responsive while performing these operations.

## Requirements

- Raspberry Pi 4 (or similar Linux-based system)
- Python 3.11 or higher
- Flask 3.0.3 
- pychromecast 14.0.4
- edge-tts (latest version)
- A local network with Chromecast devices, like Google Nests.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Wartem/nestcast.git
   cd nestcast
   ```

2. Set up a virtual environment (recommended):
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure your firewall to allow incoming connections on port 5030 (or your chosen port).

## Usage

1. Start the Flask application:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://<raspberry_pi_ip>:5030`

3. Use the web interface to discover devices, select target devices, and send messages or stream media.

## Project Structure

```
nestcast/
├── app.py                 # Main Flask application
├── chromecast_utils.py    # Utility functions for Chromecast operations
├── templates/
│   └── index.html         # HTML template for the web interface
├── static/
│   └── json/
│       └── device_ip.json # JSON file for device IP mappings
├── logs/
│   └── app.log           # Application log file
├── requirements.txt       # List of Python dependencies
└── README.md             # This file
```

## API Endpoints

- `GET /api/devices`: Returns a list of discovered devices
- `POST /api/send_message`: Sends a message to selected devices
- `POST /api/discover`: Manually triggers device discovery
- `GET /audio/<filename>`: Retrieves audio file by filename
- `POST /api/play_audio`: Initiates playback of audio on selected devices
- `POST /api/stream_media`: Starts streaming media to selected devices
- `POST /api/pause_audio`: Pauses audio playback on selected devices
- `POST /api/stop_audio`: Stops audio playback on selected devices

## Google Chrome Extension

NestCast includes a Google Chrome extension that needs to be customized for your environment. You'll need to manually adjust strings like IP address and port to match your setup.

Chrome Extension Screenshot:
![Chrome Extension](https://github.com/user-attachments/assets/d2f66809-c4fa-4303-96bc-4961eaf6375d)

## Troubleshooting

### Windows Compatibility

This project has been primarily tested and developed for use on a Raspberry Pi 4 running a Linux-based operating system. If you're experiencing issues running the application on a Windows machine, it may be due to the following reasons:

1. **Firewall restrictions**: Windows Firewall may be blocking the necessary network traffic. Ensure that Python and the Flask application are allowed through the firewall.

2. **Network discovery limitations**: Windows may have stricter network discovery settings, which can interfere with the Chromecast device discovery process.

3. **Path handling differences**: Windows uses backslashes (`\`) for file paths, while the code is written with forward slashes (`/`). This may cause issues with file handling.

4. **Multicast DNS (mDNS) support**: Windows does not natively support mDNS, which is used for Chromecast discovery. You may need to install additional software like Bonjour for Windows.

To resolve these issues, you may need to adjust your Windows security settings, install additional software, or modify the code to be more Windows-compatible. However, for the best experience, it's recommended to run this application on a Raspberry Pi or Linux-based system.

### Common Issues

1. **Devices not discovered**: Ensure that your Raspberry Pi and Google Nest devices are on the same local network and that multicast traffic is allowed.

2. **Audio playback fails**: Check that the Flask server is accessible from the local network and that the correct IP address is being used in the audio URL.

3. **Permission errors**: Make sure the user running the Flask application has permission to create and delete files in the temporary directory.

4. **Media streaming issues**: If you encounter problems with media streaming, verify that the URL is correct and accessible. Support for Youtube videos is added but is in early testing. Ensure that the video ID is correctly extracted.

5. **Volume control not working**: Double-check that the volume value is within the valid range (0.0 to 1.0). The application will default to 0.5 if an invalid volume is provided.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
