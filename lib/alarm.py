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
remote_unlock_requested = False

ALARM_FREQ = 1000
BEEP_TIME = 0.2
PAUSE = 0.1
count = 0

rpc_client = None

acceloremeter.init()


def set_rpc_client(client):
    global rpc_client
    rpc_client = client

def send_lock_state():
    global rpc_client, Lock, Alarm
    if rpc_client is None:
        return  # no connection yet

    try:
        state_str = "LOCKED" if Lock else "UNLOCKED"
        payload = {
            "lock": state_str,   # for nice text on dashboard
            "lock_bool": Lock,   # for boolean logic if you want it
            "alarm": Alarm
        }
        
        rpc_client.send_attributes({
            "lock": Lock,
            "alarm": Alarm
        })
        rpc_client.send_telemetry(payload)
        print("Sent telemetry:", payload)
    except Exception as e:
        print("Failed to send lock state:", e)
    
def pump_rpc():
    global rpc_client
    if rpc_client is not None:
        rpc_client.check_msg()

def request_remote_unlock():
    global remote_unlock_requested
    remote_unlock_requested = True
    
def perma_alarm_off():
    global Alarm
    Alarm = False
    send_lock_state()
    print("Alarm turned off")

def Timed_Alarm():
    global Alarm, Lock, remote_unlock_requested
    send_lock_state()
    for x in range(10):
        pump_rpc()

        if remote_unlock_requested:
            Alarm = False
            Lock = False
            remote_unlock_requested = False
            send_lock_state()
            solenoid.unlock()
            print("Unlocked via RPC (during timed alarm)")
            return

        tag = rfid.read_tag()
        if tag and rfid.tag_is_allowed(tag):
            remote_unlock_requested = False
            send_lock_state()
            solenoid.unlock()
            print("Alarm stopped early by RFID")
            return

        lygter.alarm_light()
        buzzer.sound(ALARM_FREQ, BEEP_TIME, PAUSE)
        lygter.light_off()


def Alarm_Lock_System(message):
    global Alarm, Lock, lock_active, remote_unlock_requested
    
    remote_unlock_requested = False
    Lock = False
    Alarm = False
    lock_active = False
    if message == "ALARM":
        Alarm = True
    else:
        Lock = True
        
    send_lock_state()
    
    while Lock or Alarm:
        pump_rpc()

        if Alarm:
            lygter.alarm_light()
            buzzer.sound(ALARM_FREQ, BEEP_TIME, PAUSE)
            lygter.light_off()
            if acceloremeter.is_still() and lock_active != True:
                print("Lock me")
                solenoid.lock()
                Lock = True
                lock_active = True

        if Lock:
            if acceloremeter.is_still() and lock_active != True:
                print("Lock me")
                solenoid.lock()
                lock_active = True
            if acceloremeter.check_tamper():
                Alarm = True
                Timed_Alarm()
            sleep(0.2)

        tag = rfid.read_tag()
        if tag and rfid.tag_is_allowed(tag):
            Alarm = False
            Lock = False
            remote_unlock_requested = False
            send_lock_state()
            solenoid.unlock()
            print("Unlocked by RFID")
            return False

        if remote_unlock_requested:
            Alarm = False
            Lock = False
            remote_unlock_requested = False
            send_lock_state()
            solenoid.unlock()
            print("Unlocked via RPC")
            return False
    send_lock_state()
    return False
