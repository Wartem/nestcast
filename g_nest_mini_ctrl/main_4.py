import pychromecast
from pychromecast.controllers.media import MediaController
import time
import zeroconf
import urllib.parse

def find_google_nest(ip=None, name="Google Nest Mini"):
    """ Hitta Google Nest Mini via IP eller namn. """
    zconf = zeroconf.Zeroconf()
    
    if ip:
        # Sök specifikt på en viss IP
        services, browser = pychromecast.discovery.discover_chromecasts(known_hosts=[ip])
    else:
        # Sök via namn om IP inte är angett
        services, browser = pychromecast.discovery.discover_chromecasts()
    
    cast_info = next((service for service in services if service.friendly_name == name or service.host == ip), None)
    
    if cast_info:
        cast = pychromecast.Chromecast(cast_info)
        cast.wait()
        print(f"Found: {cast.device.friendly_name}")
        pychromecast.discovery.stop_discovery(browser)
        return cast
    else:
        print(f"Could not find a Chromecast device at IP {ip or name}")
        pychromecast.discovery.stop_discovery(browser)
        return None

def stop_discovery(browser):
    pychromecast.discovery.stop_discovery(browser)

def send_message(cast, message):
    """ Skickar ett meddelande till en Chromecast-enhet för uppspelning. """
    if not cast:
        print("Ingen Chromecast tillgänglig")
        return

    mc = cast.media_controller
    cast.set_volume(0.5)  # Ställ in volymen till 50%
    
    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={urllib.parse.quote(message)}&tl=sv&client=tw-ob"
    
    try:
        mc.play_media(tts_url, "audio/mp3")
        mc.block_until_active()
        print(f"Spelar meddelande: {message}")
    except pychromecast.error.UnsupportedNamespace:
        print("Enheten stöder inte uppspelning av ljud")
    except Exception as e:
        print(f"Ett fel uppstod: {e}")
    
    # Vänta tills uppspelningen är klar
    start_time = time.time()
    while mc.status.player_state != 'IDLE':
        if time.time() - start_time > 30:  # 30 seconds timeout
            print("Timeout waiting for message to finish playing")
            break
        time.sleep(0.5)

def discover_all_chromecasts():
    services, browser = pychromecast.discovery.discover_chromecasts()
    if services:
        print(f"Found {len(services)} Chromecast(s)")
        for service in services:
            print(f"Device: {service.friendly_name}, IP: {service.host}")
    else:
        print("No Chromecasts found")
    pychromecast.discovery.stop_discovery(browser)

def main():
    
    discover_all_chromecasts()
    # Nest Mini-hittningen kommer efter detta för att se vilka enheter som är tillgängliga
    nest_mini = find_google_nest()
    if nest_mini:
        send_message(nest_mini, "Hej från din Raspberry Pi!")
    else:
        print("Kunde inte hitta någon Google Nest Mini-enhet")
    
    """ Main-funktion som försöker hitta och kommunicera med en Google Nest Mini. """
    ips = ['192.168.68.111', '192.168.68.106', '192.168.68.102', '192.168.68.108', '192.168.68.103']
    
    # Försök hitta en Google Nest Mini via flera IP-adresser
    for ip in ips:
        nest_mini = find_google_nest(ip)
        if nest_mini:
            send_message(nest_mini, "Hej från din Raspberry Pi!")
            break
    else:
        print("Kunde inte hitta någon Google Nest Mini-enhet")
    
if __name__ == "__main__":
    main()

# Felsökningstips:
# 1. Kontrollera att din Google Nest Mini och Raspberry Pi är på samma nätverk.
# 2. Uppdatera pychromecast och glocaltokens:
#    pip install --upgrade pychromecast glocaltokens
# 3. Installera zeroconf för att förbättra upptäckten av enheter:
#    pip install zeroconf
# 4. Se till att din brandvägg tillåter kommunikation med Chromecast-enheter.
