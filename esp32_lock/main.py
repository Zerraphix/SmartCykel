import RFID_reader as rfid
import alarm
import lock_rpc
import gc
import acceloremeter, lygter, ldr_sensor
from time import sleep


connection = False
locked = False

ldr = "MØRKT"
last_brake_check = True

acceloremeter.init()

print("Forbinder til ThingsBoard...")
try:
    client = lock_rpc.create_client()
    connection = True
    print("Connected.")
except Exception as e:
    print("Error connecting:", e)
    
if connection:
    alarm.set_rpc_client(client)

while True:
    if gc.mem_free() < 2000:
        print("Garbage collected!")
        gc.collect()
        
    if connection:
        client.check_msg()
    
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
        
    if acceloremeter.is_still(3 * 60 * 1000):
        print("Locking")
        locked = True
        locked = alarm.Alarm_Lock_System("Lock")
            
    
    
    if ldr_sensor.DayorNight() != ldr or acceloremeter.check_brake() != last_brake_check:
        if acceloremeter.check_brake():
            lygter.bremse_lys()

        elif ldr_sensor.DayorNight() == "MØRKT":
            lygter.mørke_lys()

        else:
            lygter.light_off()

    last_brake_check = acceloremeter.check_brake()
    ldr = ldr_sensor.DayorNight()
    
    print("In Main")
    sleep(0.2)