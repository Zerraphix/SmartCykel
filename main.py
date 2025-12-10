from time import sleep
import gc
import secrets

from battery_simple import read_battery
from temperature import read_temperature
from rc522_test import read_tag, tag_is_allowed
from uthingsboard.client import TBDeviceMqttClient

SERVER = secrets.SERVER_IP_ADDRESS
TOKEN = secrets.ACCESS_TOKEN

SEND_INTERVAL = 2
counter = 0


def send_once(data):
    try:
        client = TBDeviceMqttClient(SERVER, access_token=TOKEN)
        client.connect()
        client.send_telemetry(data)
        client.disconnect()
    except Exception as e:
        print("TB fejl:", e)


while True:
    try:
        batt = read_battery()
        th = read_temperature()
        tag = read_tag()
        allowed = tag_is_allowed(tag) if tag else False

        print("BAT:", batt)
        print("TEMP:", th)
        print("TAG:", tag, allowed)

        if counter >= SEND_INTERVAL:
            data = {}

            data.update(batt)

            if th["temperature_c"] is not None:
                data["temperature_c"] = th["temperature_c"]
            if th["humidity"] is not None:
                data["humidity"] = th["humidity"]

            if tag:
                data["rfid_tag"] = tag
                data["rfid_allowed"] = allowed

            if data:
                send_once(data)

            counter = 0

        sleep(1)
        counter += 1
        gc.collect()

    except KeyboardInterrupt:
        break
    except Exception as e:
        print("Main fejl:", e)
        sleep(2)
