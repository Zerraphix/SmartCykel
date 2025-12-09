import buzzer
import lygter
import acceloremeter
import gps_module
import solenoid
from time import sleep

Alarm = True

ALARM_FREQ = 1000
BEEP_TIME = 0.3
PAUSE = 0.2

while Alarm:
    gps = gps_module.get_lat_lon()
    speed = gps[2]
    if speed < 0.01:
        solenoid.lock()
    lygter.alarm_light()
    buzzer.sound(ALARM_FREQ, BEEP_TIME, PAUSE)
    lygter.light_off()
    sleep(0.1)