from machine import Pin, PWM
import time


LED_PIN = 5

pwm = PWM(Pin(LED_PIN))
pwm.freq(1000)


def mørke_lys(): # normal baglygte (svag)
    pwm.duty_u16(20000) # ca. 30% (0-65535)
    print("light on")

def bremse_lys(): # bremse-lys (kraftig)
    pwm.duty_u16(65000) # næsten 100%
    print("Brems")

def light_off():
    pwm.duty_u16(0)
    print("light off")
    
ldr = "MØRKT"
last_brake_check = True
while True:
    mørke_lys()
    time.sleep(2)
    bremse_lys()
    time.sleep(2)    
    light_off()
    time.sleep(2)

    
