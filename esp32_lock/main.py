import RFID_reader as rfid
import alarm
from time import sleep



locked = False

while True:
    tag = rfid.read_tag()
    if tag and rfid.tag_is_allowed(tag):
        print("Test")
        if locked:
            print("Unlocked")
            locked = False
        else:
            print("Locking")
            locked = True
            locked = alarm.Alarm_Lock_System("Lock")
    elif tag:
        print("Unknown tag")
    print("In Main")
    sleep(0.2)