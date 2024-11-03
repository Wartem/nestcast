import pychromecast
from pychromecast.controllers.media import MediaController
import time
import zeroconf
import urllib.parse

import pychromecast
from pychromecast.discovery import discover_chromecasts
from pychromecast.controllers.media import MediaController

def find_google_nest(ip=None):
    if ip:
        chromecasts, browser = pychromecast.get_listed_chromecasts(known_hosts=[ip])
    
    else:
        zconf = zeroconf.Zeroconf()
        chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["Google Nest Mini"], zeroconf_instance=zconf)
    
    if chromecasts:
        cast = chromecasts[0]
        cast.wait()
        print(f"Found: {cast.device.friendly_name}")
        return cast
    else:
        print(f"Could not find a Chromecast device at IP {ip}")
        return None

def send_message(cast, message):
    if not cast:
        print("Ingen Chromecast tillgänglig")
        return

    cast.wait(15)
    mc = cast.media_controller

    cast.set_volume(0.5)  # Ställ in volymen till 50%
    
    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={urllib.parse.quote(message)}&tl=sv&client=tw-ob"
    
    try:
        mc.play_media(tts_url, "audio/mp3")
        mc.block_until_active()
    except pychromecast.error.UnsupportedNamespace:
        print("Enheten stöder inte uppspelning av ljud")
    except Exception as e:
        print(f"Ett fel uppstod: {e}")

    print(f"Spelar meddelande: {message}")
    
    # Vänta tills meddelandet har spelats klart
    while mc.status.player_state != 'IDLE':
        time.sleep(0.5)

def main():
    # nest_mini = find_google_nest()
    nest_mini = find_google_nest('192.168.68.111')
    nest_mini = find_google_nest('192.168.68.106')
    nest_mini = find_google_nest('192.168.68.102')
    nest_mini = find_google_nest('192.168.68.108')
    nest_mini = find_google_nest('192.168.68.103')
    
    if nest_mini:
        send_message(nest_mini, "Hej från din Raspberry Pi!")
    else:
        print("Kunde inte hitta Google Nest Mini")
    # pychromecast.discovery.stop_discovery(browser)

if __name__ == "__main__":
    main()

# Felsökning:
# 1. Kontrollera att din Google Nest Mini är på samma nätverk som din Raspberry Pi.
# 2. Verifiera att du har de senaste versionerna av pychromecast och glocaltokens:
#    pip install --upgrade pychromecast glocaltokens
# 3. Om du fortfarande har problem, prova att använda zeroconf för upptäckt:
#    pip install zeroconf
# 4. Se till att din brandvägg tillåter upptäckt och kommunikation med Chromecast-enheter.