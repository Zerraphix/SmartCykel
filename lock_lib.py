from machine import Pin
from time import sleep



UNLOCK_PIN_NUMBER = 16   
LOCK_PIN_NUMBER   = 17


PULSE_TIME_SECONDS = 0.7

unlock_pin = Pin(UNLOCK_PIN_NUMBER, Pin.OUT)
lock_pin   = Pin(LOCK_PIN_NUMBER, Pin.OUT)

unlock_pin.value(0)
lock_pin.value(0)


def unlock_bike_lock():
    """Åbn cykellås (kort puls på unlock-pin)."""
    print("ÅBNER cykellås...")
    unlock_pin.value(1)
    sleep(PULSE_TIME_SECONDS)
    unlock_pin.value(0)
    print("Cykellås åbnet")


def lock_bike_lock():
    """Lås cykellås (kort puls på lock-pin)."""
    print("LÅSER cykellås...")
    lock_pin.value(1)
    sleep(PULSE_TIME_SECONDS)
    lock_pin.value(0)
    print("Cykellås låst")


def handle_rpc(req_id, method, params):
    """
    Simpel RPC-handler til ThingsBoard.

    Forventede metoder:
      - unlockBikeLock
      - lockBikeLock
      - testPrint (til ren test)
    """
    print("=== RPC MODTAGET I lock_lib ===")
    print("req_id:", req_id)
    print("method:", method)
    print("params:", params)

    if method == "unlockBikeLock":
        unlock_bike_lock()

    elif method == "lockBikeLock":
        lock_bike_lock()

    elif method == "testPrint":
        print("RPC testPrint modtaget (ingen lås-bevægelse)")

    else:
        print("Ukendt RPC-metode:", method)
