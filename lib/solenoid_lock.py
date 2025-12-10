from machine import Pin

solenoid = Pin(5, Pin.OUT)   # GPIO5 example
def lock():
    solenoid.value(1)
    
def unlock():
    solenoid.value(0)
    

