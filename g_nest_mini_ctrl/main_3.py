import pychromecast
from pychromecast.controllers.media import MediaController
import time
import zeroconf

def find_google_nest():
    services, browser = pychromecast.discovery.discover_chromecasts()
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["Google Nest Mini"])
    
    if chromecasts:
        cast = chromecasts[0]
        print(f"Hittade: {cast.name}")
        return cast
    else:
        print("Kunde inte hitta Google Nest Mini")
        return None

def send_message(cast, message):
    if not cast:
        print("Ingen Chromecast tillgänglig")
        return

    cast.wait()
    mc = cast.media_controller

    cast.set_volume(0.5)  # Ställ in volymen till 50%
    
    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={message}&tl=sv&client=tw-ob"
    mc.play_media(tts_url, "audio/mp3")
    mc.block_until_active()

    print(f"Spelar meddelande: {message}")
    
    # Vänta tills meddelandet har spelats klart
    while mc.status.player_state != 'IDLE':
        time.sleep(0.5)

def main():
    nest_mini = find_google_nest()
    if nest_mini:
        send_message(nest_mini, "Hej från din Raspberry Pi!")
    else:
        print("Kunde inte hitta Google Nest Mini")

if __name__ == "__main__":
    main()

# Felsökning:
# 1. Kontrollera att din Google Nest Mini är på samma nätverk som din Raspberry Pi.
# 2. Verifiera att du har de senaste versionerna av pychromecast och glocaltokens:
#    pip install --upgrade pychromecast glocaltokens
# 3. Om du fortfarande har problem, prova att använda zeroconf för upptäckt:
#    pip install zeroconf
# 4. Se till att din brandvägg tillåter upptäckt och kommunikation med Chromecast-enheter.