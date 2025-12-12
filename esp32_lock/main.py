import RFID_reader as rfid
import alarm
import lock_rpc
import gc
from time import sleep


connection = False
locked = False

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
    print("In Main")
    sleep(0.2)