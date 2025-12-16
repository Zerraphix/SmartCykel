from machine import I2C, Pin
from ina219_lib import INA219

BAT_CAPACITY = 2000
SAMPLE_SEC = 1
THRESH = 5

FULL_VOLT = 4.0
EMPTY_VOLT = 3.3

i2c = I2C(0, scl=Pin(18), sda=Pin(19))
ina = INA219(i2c, addr=0x40)
ina.set_calibration_32V_2A()

bus_v = ina.get_bus_voltage()
shunt_v = ina.get_shunt_voltage()
voltage = bus_v + shunt_v

soc_start = (voltage - EMPTY_VOLT) / (FULL_VOLT - EMPTY_VOLT)
if soc_start < 0:
    soc_start = 0
if soc_start > 1:
    soc_start = 1

remaining_mah = BAT_CAPACITY * soc_start


def read_battery():
    global remaining_mah

    bus_v = ina.get_bus_voltage()
    shunt_v = ina.get_shunt_voltage()
    current = ina.get_current()
    voltage = bus_v + shunt_v

    delta_h = SAMPLE_SEC / 3600

    if current > THRESH:
        remaining_mah -= current * delta_h
    elif current < -THRESH:
        remaining_mah += (-current) * delta_h

    if remaining_mah < 0:
        remaining_mah = 0
    if remaining_mah > BAT_CAPACITY:
        remaining_mah = BAT_CAPACITY

    soc = (remaining_mah / BAT_CAPACITY) * 100

    if current > THRESH:
        state = "discharging"
        charging = False
    elif current < -THRESH:
        state = "charging"
        charging = True
    else:
        state = "idle"
        charging = False

    if current > THRESH:
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
