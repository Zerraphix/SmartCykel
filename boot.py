import network
from time import ticks_ms, sleep
import secrets

ssid = secrets.SSID
password = secrets.PASSWORD

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    wlan.ifconfig((
        "192.168.2.4",     # IP-adresse til ESP32
        "255.255.255.0",   # Netmaske
        "192.168.2.2",     # Gateway
        "8.8.8.8"          # DNS
    ))

    print("WiFi: forbinder til:", ssid)

    if not wlan.isconnected():
        wlan.connect(ssid, password)
        start = ticks_ms()
        while not wlan.isconnected():
            sleep(0.5)
            print(".", end="")
            if ticks_ms() - start > 10000:
                print("\nKunne ikke forbinde til WiFi.")
                return wlan

    print("\nForbundet til WiFi!")
    print("ESP32 IP:", wlan.ifconfig()[0])
    return wlan

wlan = do_connect()
