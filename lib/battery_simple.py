from machine import I2C, Pin
from ina219_lib import INA219

BAT_CAPACITY = 2000 
THRESH = 5               
SAMPLE_SEC = 1          

i2c = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
ina = INA219(i2c, addr=0x40)
ina.set_calibration_32V_2A()

remaining_mah = BAT_CAPACITY


def read_battery():
    global remaining_mah

    bus_v = ina.get_bus_voltage()
    shunt_v = ina.get_shunt_voltage()
    current = ina.get_current()

    voltage = bus_v + shunt_v
    hours = SAMPLE_SEC / 3600

    if current > THRESH:
        remaining_mah -= current * hours
    elif current < -THRESH:
        remaining_mah += (-current) * hours

    #hold indenfor 0–kapacitet
    if remaining_mah < 0:
        remaining_mah = 0
    if remaining_mah > BAT_CAPACITY:
        remaining_mah = BAT_CAPACITY

    #procent
    soc = (remaining_mah / BAT_CAPACITY) * 100

    # status
    if current < -THRESH:
        state = "charging"
        charging = True
    elif current > THRESH:
        state = "discharging"
        charging = False
    else:
        state = "idle"
        charging = False

    #resterende tid kun ved afladning
    if current > THRESH and remaining_mah > 0:
        hours_left = remaining_mah / current
        h = int(hours_left)
        m = int((hours_left - h) * 60)
        time_text = "{}h {}m".format(h, m)
    else:
        hours_left = None
        time_text = "Ukendt"

    return {
        "battery_voltage": round(voltage, 3),
        "battery_current": round(current, 1),
        "battery_remaining_mah": round(remaining_mah, 1),
        "battery_soc": round(soc, 1),
        "battery_remaining_hours": hours_left,
        "battery_remaining_text": time_text,
        "battery_state": state,
        "battery_charging": charging
    }
