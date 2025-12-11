from uthingsboard.client import TBDeviceMqttClient
from machine import Pin
from time import sleep
import gc
import secrets
import network
import time

UNLOCK_PIN_NUMBER = 16
LOCK_PIN_NUMBER   = 17
PULSE_TIME_SECONDS = 0.7

unlock_pin = Pin(UNLOCK_PIN_NUMBER, Pin.OUT)
lock_pin   = Pin(LOCK_PIN_NUMBER, Pin.OUT)

unlock_pin.value(0)
lock_pin.value(0)


while not wlan.isconnected():
    print("Connecting WiFi...")
    time.sleep(1)

print("WiFi connected:", wlan.ifconfig())

# --- ThingsBoard client setup ---
client = TBDeviceMqttClient(
    secrets.SERVER_IP_ADDRESS,
    access_token=secrets.ACCESS_TOKEN
)

def unlock_bike_lock():
    print("ÅBNER cykellås...")
    unlock_pin.value(1)
    sleep(PULSE_TIME_SECONDS)
    unlock_pin.value(0)
    print("Cykellås åbnet")

def lock_bike_lock():
    print("LÅSER cykellås...")
    lock_pin.value(1)
    sleep(PULSE_TIME_SECONDS)
    lock_pin.value(0)
    print("Cykellås låst")

def handler(req_id, method, params):
    """Handler callback to receive RPC from server."""
    print("=== RPC MODTAGET I lock_lib ===")
    print("req_id:", req_id)
    print("method:", method)
    print("params:", params)
    try:
        if method == "unlockBikeLock":
            unlock_bike_lock()
        elif method == "lockBikeLock":
            lock_bike_lock()
        elif method == "testPrint":
            print("RPC testPrint modtaget (ingen lås-bevægelse)")
        else:
            print("Ukendt RPC-metode:", method)
    except TypeError as e:
        print("TypeError in handler:", e)

# Connect once and set handler once
client.connect()
client.set_server_side_rpc_request_handler(handler)

# --- Main loop ---
while True:
    try:
        print(f"free memory: {gc.mem_free()}")
        if gc.mem_free() < 2000:
            print("Garbage collected!")
            gc.collect()

        # If you want telemetry, uncomment and fill in:
        # telemetry = {}
        # client.send_telemetry(telemetry)

        client.check_msg()  # check for incoming RPC
        sleep(3)
    except KeyboardInterrupt:
        print("Disconnected!")
        client.disconnect()
        break
