from machine import Pin, PWM
import time
import ldr_sensor
import acceloremeter

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

    if ldr_sensor.DayorNight() != ldr:
        
        if ldr_sensor.DayorNight() == "MØRKT":
            mørke_lys()
        if ldr_sensor.DayorNight() == "LYS":
            light_off()
        ldr = ldr_sensor.DayorNight()
    if acceloremeter.check_brake() != last_brake_check:
        if acceloremeter.check_brake():
            bremse_lys()
            last_brake_check = acceloremeter.check_brake()
        elif ldr_sensor.DayorNight() == "MØRKT":
            mørke_lys()
            last_brake_check = acceloremeter.check_brake()
        else:
            light_off()
            last_brake_check = acceloremeter.check_brake()
    time.sleep(0.5)

    
