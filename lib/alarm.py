import buzzer
import lygter
import acceloremeter
import gps_module
import solenoid
from time import sleep
import RFID_reader as rfid

Alarm = False
Lock = True
lock_active = True

ALARM_FREQ = 1000
BEEP_TIME = 0.2
PAUSE = 0.1
count = 0

acceloremeter.init()

def Timed_Alarm():
    for x in range(10):
        tag = rfid.read_tag()
        if tag and rfid.tag_is_allowed(tag):
            print("Alarm stopped early")
            break
        #gps = gps_module.get_lat_lon()
        #speed = gps[2]
        #if speed < 0.01 and lock_active != True:
        #    solenoid.lock()
        #    Lock = True
        lygter.alarm_light()
        buzzer.sound(ALARM_FREQ, BEEP_TIME, PAUSE)
        lygter.light_off()
        
        
        
def Alarm_Lock_System(message):
    Lock = False
    Alarm = False
    if message == "ALARM":
        Alarm = True
    else:
        Lock = True
    
    while Lock or Alarm:
        if Alarm:  
            #gps = gps_module.get_lat_lon()
            #speed = gps[2]
            #if speed < 0.01 and lock_active != True:
            #    solenoid.lock()
            #    Lock = True
            lygter.alarm_light()
            buzzer.sound(ALARM_FREQ, BEEP_TIME, PAUSE)
            lygter.light_off()
            # En måde til at slukke
        if Lock:
            solenoid.lock()
            if acceloremeter.check_tamper():
                Timed_Alarm()
            sleep(0.5)
        tag = rfid.read_tag()
        if tag and rfid.tag_is_allowed(tag):
            Alarm = False
            Lock = False
            print("Unlocked")
            return False
