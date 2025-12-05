from machine import Pin
import time

ldr = Pin(15, Pin.IN)  

def DayorNight():
    value = ldr.value()
    
    if value == 0:
        return("LYS")
    else:
        return("MØRKT")
    