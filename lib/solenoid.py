from machine import Pin

solenoid = Pin(2, Pin.OUT)
def lock():
    solenoid.value(1)
    
def unlock():
    solenoid.value(0)
    
