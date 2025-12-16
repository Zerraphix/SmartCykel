from machine import Pin, PWM
import time
from neopixel import NeoPixel
import ldr_sensor
import acceloremeter

antal = 12
np = NeoPixel(Pin(12, Pin.OUT), antal)
LED_PIN = 4

pwm = PWM(Pin(LED_PIN))
pwm.freq(1000)


def mørke_lys():
    pwm.duty_u16(20000)
    for i in range(antal):
        np[i] = (255,255,255)
    np.write()

def bremse_lys():
    pwm.duty_u16(65000)
    print("Brems")

def light_off():
    pwm.duty_u16(0)
    for i in range(antal):
        np[i] = (0,0,0)
    np.write()
    
def alarm_light():
    pwm.duty_u16(65000)
    for i in range(antal):
        np[i] = (255,0,0)
    np.write()

