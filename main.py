from time import sleep
import gc
import secrets
from machine import UART

from gps_module import get_lat_lon
#from battery_simple import read_battery
import time
import ldr_sensor
import lygter
import acceloremeter
import lcd_display
from uthingsboard.client import TBDeviceMqttClient


uart = UART(2, 9600)

client = TBDeviceMqttClient(
    secrets.SERVER_IP_ADDRESS,
    access_token=secrets.ACCESS_TOKEN
)

print("Forbinder til ThingsBoard...")
try:
    client.connect()
    print("Connected.")
except:
    print("Error connecting")


SEND_INTERVAL = 30
counter = 0

ldr = "MØRKT"
last_brake_check = True

acceloremeter.init()

while True:


    gps = get_lat_lon()
    #battery = read_battery()
    data = {}
    data["battery_soc"] = 10.1

    if gps != None:
        data["latitude"] = gps[0]
        data["longitude"] = gps[1]
        data["speed"] = gps[2]
        
    lcd_display.lcd_show_status(data)

    if counter >= SEND_INTERVAL:
        
        client.send_telemetry(data)
        print("SENDT:", data)

        counter = 0

        
    if ldr_sensor.DayorNight() != ldr or acceloremeter.check_brake() != last_brake_check:
        if acceloremeter.check_brake():
            lygter.bremse_lys()
        elif ldr_sensor.DayorNight() == "MØRKT":
            lygter.mørke_lys()
        else:
            lygter.light_off()
        last_brake_check = acceloremeter.check_brake()
        ldr = ldr_sensor.DayorNight()
    
    sleep(1)
    counter += 1
    gc.collect()
