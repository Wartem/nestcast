# Integration av Google Nest Mini med Raspberry Pi

## Förberedelser:

# 1. Säkerställ att din Google Nest Mini är konfigurerad och ansluten till samma nätverk som din Raspberry Pi.
# 2. Installera nödvändiga bibliotek på din Raspberry Pi:

# ```
# pip install glocaltokens pychromecast
# pip install --upgrade pychromecast glocaltokens zeroconf
# pip install --upgrade pychromecast glocaltokens zeroconf
# p```

## Python-kod för grundläggande integration:

import pychromecast
from glocaltokens.client import GLocalAuthenticationTokens

# Funktion för att hitta din Google Nest Mini
def find_google_nest():
    chromecasts, browser = pychromecast.get_chromecasts()
    for cast in chromecasts:
        if "Google Nest Mini" in cast.device.friendly_name:
            print(f"Hittade: {cast.device.friendly_name}")
            return cast
    return None

# Funktion för att skicka ett meddelande till Google Nest Mini
def send_message(cast, message):
    cast.wait()
    cast.set_volume(0.5)  # Ställ in volymen till 50%
    cast.media_controller.play_media(
        "https://translate.google.com/translate_tts?ie=UTF-8&q=" + message + "&tl=sv&client=tw-ob",
        "audio/mp3"
    )

# Huvudfunktion
def main():
    nest_mini = find_google_nest()
    if nest_mini:
        send_message(nest_mini, "Hej från din Raspberry Pi!")
    else:
        print("Kunde inte hitta Google Nest Mini")

if __name__ == "__main__":
    main()

# OBS: Denna kod ger grundläggande funktionalitet. För mer avancerad 
# integrering, överväg att använda Google Assistant SDK eller IFTTT.