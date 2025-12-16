from time import sleep
import gc
import secrets
from battery_simple import read_battery
from temperature import read_temperature
from uthingsboard.client import TBDeviceMqttClient
from lcd_status import lcd_show_status
from gps_module import read_gps

SERVER = secrets.SERVER_IP_ADDRESS
TOKEN = secrets.ACCESS_TOKEN

SEND_INTERVAL = 5
counter = 0
client = TBDeviceMqttClient(SERVER, access_token=TOKEN)
print("Forbinder til ThingsBoard...")

try:
    client.connect()
    print("Forbundet")
except Exception as e:
    print("Kunne ikke forbinde:", e)

while True:
    try:
        batt = read_battery()
        temp = read_temperature()
        data = {}
        data.update(batt)
        gps_data = read_gps(2)
        if gps_data is not None:
            data.update(gps_data)

        if temp.get("temperature_c") is not None:
            data["temperature_c"] = temp["temperature_c"]
        if temp.get("humidity") is not None:
            data["humidity"] = temp["humidity"]

        lcd_show_status(data)
        if counter >= SEND_INTERVAL:
            try:
                client.send_telemetry(data)
                print("SENDT:", data)
            except Exception as e:
                print("Sendefejl:", e)
            counter = 0
        sleep(1)
        counter += 1
        gc.collect()

    except KeyboardInterrupt:
        print("Program stoppet")
        try:
            client.disconnect()
        except:
            pass
        break

    except Exception as e:
        print("Fejl i main:", e)
        sleep(2)

