from machine import Pin
import time

# Skift 5 til den GPIO du bruger
led_ctrl = Pin(5, Pin.OUT)

# Start med slukket
led_ctrl.value(0)

def Brake():
    led_ctrl.value(1)

while True:
    # Tænd alle LED'erne
    Brake()
    time.sleep(1)

    # Sluk alle LED'erne
    led_ctrl.value(0)
    time.sleep(1)
