import network
from time import sleep
import secrets

SSID = secrets.SSID
PASSWORD = secrets.PASSWORD


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("WiFi: forbinder til", SSID)
        try:
            wlan.connect(SSID, PASSWORD)
        except OSError as e:
            print("WiFi fejl ved connect:", e)
            return wlan

        timeout = 20
        while not wlan.isconnected() and timeout > 0:
            print(".", end="")
            sleep(1)
            timeout -= 1

    print()
    print("WiFi connected:", wlan.isconnected())
    print("ifconfig:", wlan.ifconfig())
    return wlan


wlan = do_connect()
