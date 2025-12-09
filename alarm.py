import buzzer
import lygter
import acceloremeter
import gps_module
import solenoid
from time import sleep

Alarm = False
Lock = True
lock_active = True

ALARM_FREQ = 1000
BEEP_TIME = 0.3
PAUSE = 0.2
count = 0

while True:
    if Alarm:
        count = count + 1
        print(count)
        if count >= 10:
            print("Whoops")
            Alarm = False
            Lock = True
            count = 0
        gps = gps_module.get_lat_lon()
        speed = gps[2]
        if speed < 0.01 and lock_active != True:
            solenoid.lock()
            Lock = True
        lygter.alarm_light()
        buzzer.sound(ALARM_FREQ, BEEP_TIME, PAUSE)
        lygter.light_off()
    
    if Lock:
        solenoid.lock()
        if acceloremeter.check_tamper():
            Alarm = True
            Lock = False
        
    sleep(0.1)
    

    
        