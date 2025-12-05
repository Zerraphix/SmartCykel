from machine import Pin, PWM
import time
from neopixel import NeoPixel
import ldr_sensor
import acceloremeter

#JP1 3v3 til +
#JP1 12 til DI
#JP1 GND til GND
antal = 12
np = NeoPixel(Pin(12, Pin.OUT), antal)
LED_PIN = 5

pwm = PWM(Pin(LED_PIN))
pwm.freq(1000)


def mørke_lys(): # normal baglygte (svag)
    pwm.duty_u16(20000) # ca. 30% (0-65535) for baglygte
    for i in range(antal): # for forlygte
        np[i] = (255,255,255)
    np.write()
    print("light on")

def bremse_lys(): # bremse-lys (kraftig)
    pwm.duty_u16(65000) # næsten 100%
    print("Brems")

def light_off():
    pwm.duty_u16(0) # for baglygte
    for i in range(antal): # for forlygte
        np[i] = (0,0,0)
    np.write()
    print("light off")
    
ldr = "MØRKT"
last_brake_check = True
while True:

    if ldr_sensor.DayorNight() != ldr or acceloremeter.check_brake() != last_brake_check:
        if acceloremeter.check_brake():
            bremse_lys()
        elif ldr_sensor.DayorNight() == "MØRKT":
            mørke_lys()
        else:
            light_off()
        last_brake_check = acceloremeter.check_brake()
        ldr = ldr_sensor.DayorNight()
            
    time.sleep(0.5)

    
