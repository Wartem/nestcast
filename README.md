# NestCast

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-green.svg)](https://flask.palletsprojects.com/en/3.0.x/)
[![pychromecast](https://img.shields.io/badge/pychromecast-14.0.4-orange.svg)](https://github.com/home-assistant-libs/pychromecast)
[![Edge-TTS](https://img.shields.io/badge/Edge--TTS-latest-yellow.svg)](https://github.com/rany2/edge-tts)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)

NestCast is a Flask-based web application using pychromecast and edge-tts. It is designed to run on a Raspberry Pi, enabling users to send text-to-speech messages, stream media, and control audio playback on Chromecast-enabled devices within their local network. The application provides a simple web interface for device discovery and message sending, primarily targeting Google Nest devices with built-in Chromecast functionality. Other scripts and applications like Google Chrome extentions running on the LAN can access the endpoints making this project suitable to run on a Raspberry Pi server. Do not open this up to the Internet.

it's crucial not to expose this setup directly to the internet without implementing proper security measures. Keeping it as a LAN-only service is a good starting point for maintaining security.

**Note:** NestCast is based on PyChromecast and is designed for use on local, secured networks. Users should ensure they have appropriate network security measures in place and follow best practices when deploying this application. As with any network-connected application, use caution and common sense to protect your devices and data.

--------------

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

Edge-tts provideds 83 languages and they are available in this app:

<details>
<summary>Click to expand!</summary>
  This appears to be a list of options for a text-to-speech system, with different languages and dialects represented. Here is a breakdown of the options by language:

1. Afrikaans: 
   - South Africa (Female: AdriNeural, Male: WillemNeural)

2. Albanian: 
   - Albania (Female: VjosaNeural, Male: IlirNeural)

3. Amharic: 
   - Ethiopia (Female: MekdesNeural, Male: AmareNeural)

4. Arabic: 
   - Algeria (Female: AminaNeural, Male: IsmailNeural)
   - Bahrain (Female: FatimaNeural, Male: RashidNeural)
   - Egypt (Female: SalmaNeural, Male: TarekNeural)
   - Iraq (Female: RanaNeural, Male: BasselNeural)
   - Jordan (Female: SanaNeural, Male: TaimNeural)
   - Kuwait (Female: NouraNeural, Male: FahadNeural)
   - Lebanon (Female: LeilaNeural, Male: FadiNeural)
   - Libya (Female: ImanNeural, Male: OmarNeural)
   - Morocco (Female: JamilaNeural, Male: AmirNeural)
   - Oman (Female: AhlamNeural, Male: HilalNeural)
   - Palestine (Female: FatimaNeural, Male: TamerNeural)
   - Qatar (Female: HessaNeural, Male: RashidNeural)
   - Saudi Arabia (Female: ReemNeural, Male: NaifNeural)
   - Syria (Female: AbeerNeural, Male: LaithNeural)
   - Tunisia (Female: YosraNeural, Male: HediNeural)
   - United Arab Emirates (Female: ShaikhaNeural, Male: AbdullaNeural)
   - Yemen (Female: MaryamNeural, Male: AliNeural)

5. Armenian: 
   - Armenia (Female: AnahitNeural, Male: ArtakNeural)

6. Azerbaijani: 
   - Azerbaijan (Female: BanuNeural, Male: BabakNeural)

7. Bangla: 
   - Bangladesh (Female: NabanitaNeural, Male: PradeepNeural)
   - India (Female: TanishNeural, Male: ArnabNeural)

8. Basque: 
   - Spain (Female: AinhoaNeural, Male: KepaNeural)

9. Belarusian: 
   - Belarus (Female: DaryaNeural, Male: AliakseiNeural)

10. Bosnian: 
    - Bosnia and Herzegovina (Female: LanaNeural, Male: IgorNeural)

11. Bulgarian: 
    - Bulgaria (Female: KalinaNeural, Male: IvanNeural)

12. Catalan: 
    - Spain (Female: NuriaNeural, Male: EnricNeural)

13. Chinese: 
    - China (Female: XiaoxiaoNeural, Male: YunyangNeural)
    - Hong Kong (Female: HiuMaanNeural, Male: WanLungNeural)
    - Macau (Female: MengjieNeural, Male: ChengNeural)
    - Taiwan (Female: HsiaoChenNeural, Male: PoWeiNeural)

14. Croatian: 
    - Croatia (Female: SreckaNeural, Male: PavaoNeural)

15. Czech: 
    - Czech Republic (Female: ZuzanaNeural, Male: JakubNeural)

16. Danish: 
    - Denmark (Female: FrejaNeural, Male: MagnusNeural)

17. Dutch: 
    - Netherlands (Female: ColetteNeural, Male: MaartenNeural)

18. English: 
    - Australia (Female: NatashaNeural, Male: WilliamNeural)
    - Canada (Female: ClaraNeural, Male: LiamNeural)
    - India (Female: AaradhyaNeural, Male: KabirNeural)
    - Ireland (Female: SaoirseNeural, Male: CianNeural)
    - New Zealand (Female: ArohaNeural, Male: ManaNeural)
    - Nigeria (Female: NneomaNeural, Male: IkeNeural)
    - Philippines (Female: MayumiNeural, Male: AngeloNeural)
    - South Africa (Female: AyandaNeural, Male: ThembaNeural)
    - United Kingdom (Female: LibbyNeural, Male: RyanNeural)
    - United States (Female: JennyNeural, Male: GuyNeural)

19. Estonian: 
    - Estonia (Female: AnuNeural, Male: KertNeural)

20. Farsi (Persian): 
    - Iran (Female: DorsaNeural, Male: PeymanNeural)

21. Filipino: 
    - Philippines (Female: BlessieNeural, Male: AngeloNeural)

22. Finnish: 
    - Finland (Female: SelmaNeural, Male: HarriNeural)

23. French: 
    - Belgium (Female: ColetteNeural, Male: GauthierNeural)
    - Canada (Female: SylvieNeural, Male: AntoineNeural)
    - France (Female: DeniseNeural, Male: HenriNeural)
    - Switzerland (Female: ArianeNeural, Male: FabriceNeural)

24. Galician: 
    - Spain (Female: SabelaNeural, Male: CarlosNeural)

25. Georgian: 
    - Georgia (Female: NinoNeural, Male: GiorgiNeural)

26. German: 
    - Austria (Female: IngridNeural, Male: JohannNeural)
    - Germany (Female: KatjaNeural, Male: StefanNeural)
    - Switzerland (Female: UrsulaNeural, Male: MarcelNeural)

27. Greek: 
    - Greece (Female: MelinaNeural, Male: NikosNeural)

28. Gujarati: 
    - India (Female: DhwaniNeural, Male: KunalNeural)

29. Hebrew: 
    - Israel (Female: HilaNeural, Male: AsafNeural)

30. Hindi: 
    - India (Female: SwaraNeural, Male: SameerNeural)

31. Hungarian: 
    - Hungary (Female: NoemiNeural, Male: TamasNeural)

32. Icelandic: 
    - Iceland (Female: HrafnhildurNeural, Male: GunnarNeural)

33. Indonesian: 
    - Indonesia (Female: IntanNeural, Male: BudiNeural)

34. Irish: 
    - Ireland (Female: OrlaNeural, Male: CianNeural)

35. Italian: 
    - Italy (Female: ElisabettaNeural, Male: RoccoNeural)
    - Switzerland (Female: GiuliaNeural, Male: AlessandroNeural)

36. Japanese: 
    - Japan (Female: NanamiNeural, Male: KeitaNeural)

37. Javanese: 
    - Indonesia (Female: SitiNeural, Male: BambangNeural)

38. Kannada: 
    - India (Female: SapnaNeural, Male: RakeshNeural)

39. Kazakh: 
    - Kazakhstan (Female: DinaraNeural, Male: DauletNeural)

40. Khmer: 
    - Cambodia (Female: SreymomNeural, Male: PisethNeural)

41. Korean: 
    -
- South Korea (Female: JiMinNeural, Male: JunHwanNeural)

42. Kurdish: 
    - Iraq (Female: BaharNeural, Male: SirwanNeural)

43. Latvian: 
    - Latvia (Female: EveritaNeural, Male: NaurisNeural)

44. Lithuanian: 
    - Lithuania (Female: OnaNeural, Male: LeonasNeural)

45. Luxembourgish: 
    - Luxembourg (Female: PauletteNeural, Male: FrançoisNeural)

46. Macedonian: 
    - North Macedonia (Female: KaterinaNeural, Male: GoranNeural)

47. Malay: 
    - Malaysia (Female: YasminNeural, Male: OsmanNeural)

48. Malayalam: 
    - India (Female: NaliniNeural, Male: MidhunNeural)

49. Maltese: 
    - Malta (Female: GiuliaNeural, Male: MichaelNeural)

50. Maori: 
    - New Zealand (Female: ArohaNeural, Male: TamaNeural)

51. Marathi: 
    - India (Female: AaradhyaNeural, Male: TusharNeural)

52. Mongolian: 
    - Mongolia (Female: NominNeural, Male: TemujinNeural)

53. Nepali: 
    - Nepal (Female: ApsaraNeural, Male: AyushNeural)

54. Norwegian: 
    - Norway (Female: LivNeural, Male: SindreNeural)

55. Pashto: 
    - Afghanistan (Female: ZarghonaNeural, Male: GulzarNeural)

56. Persian (Dari): 
    - Afghanistan (Female: YaldaNeural, Male: KavehNeural)

57. Polish: 
    - Poland (Female: ZofiaNeural, Male: JacekNeural)

58. Portuguese: 
    - Brazil (Female: FranciscaNeural, Male: AntonioNeural)
    - Portugal (Female: BeatrizNeural, Male: DuarteNeural)

59. Punjabi: 
    - India (Female: HeerNeural, Male: KuldeepNeural)
    - Pakistan (Female: AyeshaNeural, Male: AliNeural)

60. Quechua: 
    - Peru (Female: KusiNeural, Male: JuanNeural)

61. Romanian: 
    - Romania (Female: AlinaNeural, Male: DragosNeural)

62. Russian: 
    - Russia (Female: AnastasiaNeural, Male: DmitryNeural)

63. Scottish Gaelic: 
    - United Kingdom (Female: MorvenNeural, Male: AngusNeural)

64. Serbian: 
    - Serbia (Female: MarijaNeural, Male: SretenNeural)

65. Sinhala: 
    - Sri Lanka (Female: NadeejaNeural, Male: AsankaNeural)

66. Slovak: 
    - Slovakia (Female: ViktoriaNeural, Male: FilipNeural)

67. Slovenian: 
    - Slovenia (Female: TjašaNeural, Male: ŽigaNeural)

68. Somali: 
    - Somalia (Female: UbahNeural, Male: AbdiNeural)

69. Spanish: 
    - Argentina (Female: ElenaNeural, Male: MateoNeural)
    - Bolivia (Female: LucianaNeural, Male: MarceloNeural)
    - Chile (Female: FranciscaNeural, Male: RodrigoNeural)
    - Colombia (Female: SoledadNeural, Male: CarlosNeural)
    - Costa Rica (Female: MaríaNeural, Male: JuanNeural)
    - Cuba (Female: LauraNeural, Male: LuisNeural)
    - Dominican Republic (Female: RosaNeural, Male: JuanNeural)
    - Ecuador (Female: SofíaNeural, Male: LuisNeural)
    - El Salvador (Female: MargaritaNeural, Male: CarlosNeural)
    - Guatemala (Female: MartaNeural, Male: JuanNeural)
    - Honduras (Female: MaríaNeural, Male: CarlosNeural)
    - Mexico (Female: LucianaNeural, Male: LuisNeural)
    - Nicaragua (Female: MaríaNeural, Male: LeonardoNeural)
    - Panama (Female: AnaNeural, Male: LuisNeural)
    - Paraguay (Female: SofíaNeural, Male: CarlosNeural)
    - Peru (Female: MaríaNeural, Male: LuisNeural)
    - Puerto Rico (Female: IsabelNeural, Male: CarlosNeural)
    - Spain (Female: SofíaNeural, Male: LuisNeural)
    - United States (Female: MaríaNeural, Male: LuisNeural)
    - Uruguay (Female: LucianaNeural, Male: LuisNeural)
    - Venezuela (Female: GabrielaNeural, Male: CarlosNeural)

70. Swahili: 
    - Tanzania (Female: RehemaNeural, Male: DaudiNeural)

71. Swedish: 
    - Sweden (Female: HedvigNeural, Male: LarsNeural)

72. Tamil: 
    - India (Female: KavithaNeural, Male: KumarNeural)
    - Sri Lanka (Female: NalayiniNeural, Male: SivakumarNeural)

73. Telugu: 
    - India (Female: SwathiNeural, Male: SrinivasNeural)

74. Thai: 
    - Thailand (Female: NichaNeural, Male: KietNeural)

75. Turkish: 
    - Turkey (Female: FilizNeural, Male: ÖmerNeural)

76. Ukrainian: 
    - Ukraine (Female: AnastasiaNeural, Male: OleksandrNeural)

77. Urdu: 
    - India (Female: AyeshaNeural, Male: RashidNeural)
    - Pakistan (Female: UzmaNeural, Male: AsadNeural)

78. Uzbek: 
    - Uzbekistan (Female: NodiraNeural, Male: BakhodirNeural)

79. Vietnamese: 
    - Vietnam (Female: LinhNeural, Male: MinhNeural)

80. Welsh: 
    - United Kingdom (Female: BranwenNeural, Male: AneurinNeural)

81. Xhosa: 
    - South Africa (Female: NtombiNeural, Male: ThembaNeural)

82. Yoruba: 
    - Nigeria (Female: EniolaNeural, Male: OluwafemiNeural)

83. Zulu: 
    - South Africa (Female: NandiNeural, Male: SibusisoNeural)
      
</details>

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
- `POST /api/pause_audio`: Pauses audio playback on selected devices (Not yet available)
- `POST /api/stop_audio`: Stops audio playback on selected devices (Not yet available)

Note that for simplification and ease of use there is not yet any authentication for accessing the endpoints. HTTPS might also be added later for encrypted communication.

## Google Chrome Extension

NestCast includes a Google Chrome extension that needs to be customized for your environment. You'll need to manually adjust strings like IP address and port to match your setup.

Chrome Extension Screenshot:
![Chrome Extension](https://github.com/user-attachments/assets/d2f66809-c4fa-4303-96bc-4961eaf6375d)

## Security Considerations

NestCast is designed for use on local, private networks. Please keep the following in mind:

1. **Network**: Use only on secured, private networks you control.

2. **Access**: By default, there's no user authentication. Add access controls if needed.

3. **Updates**: Keep NestCast and its dependencies current for best security.

4. **Usage**: Ensure your use complies with local laws and respects others' privacy.

5. **Customization**: For use in open environments, consider adding authentication and HTTPS.

This project is based on PyChromecast and inherits its security model. Use common sense when deploying network-connected applications to protect your devices and data.


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
