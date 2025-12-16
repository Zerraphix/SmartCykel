from machine import Pin
import time

unlock_pin = Pin(16, Pin.OUT)
lock_pin   = Pin(17, Pin.OUT)


unlock_pin.value(0)
lock_pin.value(0)


pulse_time = 0.7

def unlock_bike():
    print("Åbner cykellås...")
    unlock_pin.value(1)
    time.sleep(pulse_time)
    unlock_pin.value(0)
    print("cykellås er åbnet")


def lock_bike():
    print("Låser cykellås...")
    lock_pin.value(1)
    time.sleep(pulse_time)
    lock_pin.value(0)
    print("cykellås er låst")
