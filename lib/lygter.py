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
LED_PIN = 4

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
    
def alarm_light():
    pwm.duty_u16(65000)
    for i in range(antal):
        np[i] = (255,0,0)
    np.write()

