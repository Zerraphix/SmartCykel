from time import sleep
import gc
import secrets
from battery_simple import read_battery
from temperature import read_temperature
from RFIDLæser import read_tag, tag_is_allowed
from uthingsboard.client import TBDeviceMqttClient
import lock_lib
import alarm_knap_lib
from gps_module import get_lat_lon
import ldr_sensor
import lygter
import acceloremeter
import lcd_display
from machine import UART
    
SERVER = secrets.SERVER_IP_ADDRESS
TOKEN = secrets.ACCESS_TOKEN

SEND_INTERVAL = 5

uart = UART(2, 9600)

# Første ThingsBoard-client (du oprettede to – holder kun den rigtige)
client = TBDeviceMqttClient(SERVER, access_token=TOKEN)
client.set_server_side_rpc_request_handler(lock_lib.handle_rpc, alarm_knap_lib.handle_rpc)

print("Forbinder til ThingsBoard...")
try:
    client.connect()
    print("Connected.")
except Exception as e:
    print("Error connecting:", e)

counter = 0

ldr = "MØRKT"
last_brake_check = True

acceloremeter.init()

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

            # Batteri tilføjes direkte
            data.update(batt)

            # Temperatur & luftfugtighed
            if th.get("temperature_c") is not None:
                data["temperature_c"] = th["temperature_c"]
            if th.get("humidity") is not None:
                data["humidity"] = th["humidity"]

            # RFID
            data["rfid_tag"] = tag if tag else ""
            data["rfid_allowed"] = bool(allowed)

            # GPS
            gps = get_lat_lon()
            if gps:
                data["latitude"] = gps[0]
                data["longitude"] = gps[1]
                data["speed"] = gps[2]

            client.send_telemetry(data)
            print("SENDT:", data)
            counter = 0

        # MQTT check
        client.check_msg()

        # LCD opdatering
        lcd_display.lcd_show_status(locals().get("data", {}))

        # Sensorbaseret lysstyring
        """if ldr_sensor.DayorNight() != ldr or acceloremeter.check_brake() != last_brake_check:

            if acceloremeter.check_brake():
                lygter.bremse_lys()

            elif ldr_sensor.DayorNight() == "MØRKT":
                lygter.mørke_lys()

            else:
                lygter.light_off()

        #last_brake_check = acceloremeter.check_brake()
        ldr = ldr_sensor.DayorNight()"""

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
