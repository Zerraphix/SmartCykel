from time import sleep
import gc
import secrets
from machine import UART

from gps_module import get_lat_lon
from battery_simple import read_battery
from uthingsboard.client import TBDeviceMqttClient
from rc522_test import read_tag, tag_is_allowed


uart = UART(2, 9600)

client = TBDeviceMqttClient(
    secrets.SERVER_IP_ADDRESS,
    access_token=secrets.ACCESS_TOKEN
)

print("Forbinder til ThingsBoard...")
client.connect()
print("Connected.")


SEND_INTERVAL = 30
counter = 0


while True:


    pos = get_lat_lon()
    battery = read_battery()
    
    tag = read_tag()
    tag_ok = False
    if tag:
        tag_ok = tag_is_allowed()

    if counter >= SEND_INTERVAL:
        data = {}
        data.update(battery)

        if pos:
            data["latitude"] = pos[0]
            data["longitude"] = pos[1]

        if tag:
            data["rfid_tag"] = tag
            data["rfid_allowed"] = tag_ok

        client.send_telemetry(data)
        print("SENDT:", data)

        counter = 0

    sleep(1)
    counter += 1
    gc.collect()

