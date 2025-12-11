from time import sleep
import gc
import secrets

from battery_simple import read_battery
from temperature import read_temperature
from RFIDLæser import read_tag, tag_is_allowed
from uthingsboard.client import TBDeviceMqttClient
import lock_lib
import alarm_knap_lib

SERVER = secrets.SERVER_IP_ADDRESS
TOKEN = secrets.ACCESS_TOKEN

SEND_INTERVAL = 5
counter = 0
client = TBDeviceMqttClient(SERVER, access_token=TOKEN)
client.set_server_side_rpc_request_handler(lock_lib.handle_rpc, alarm_knap_lib.handle_rpc)
client.connect()
print("Forbundet til ThingsBoard")


while True:
    try:
        batt = read_battery()
        th = read_temperature()
        tag = read_tag()
        allowed = tag_is_allowed(tag) if tag else False

        print("BAT:", batt)
        print("TEMP/HUM:", th)
        print("TAG:", tag, "ALLOWED:", allowed)
        if counter >= SEND_INTERVAL:
            data = {}

            data.update(batt)

            if th["temperature_c"] is not None:
                data["temperature_c"] = th["temperature_c"]
            if th["humidity"] is not None:
                data["humidity"] = th["humidity"]

            data["rfid_tag"] = tag if tag else ""
            data["rfid_allowed"] = bool(allowed)

            client.send_telemetry(data)
            print("SENDT:", data)
            counter = 0
        client.check_msg()
        sleep(1)
        counter += 1
        gc.collect()

    except KeyboardInterrupt:
        print("Stopper...")
        client.disconnect()
        break

    except Exception as e:
        print("Main fejl:", e)
        sleep(2)
