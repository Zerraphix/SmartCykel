# battery_simple.py
from machine import I2C, Pin
from ina219_lib import INA219

BAT_CAPACITY_MAH = 2000
FULL_VOLT = 4.20
EMPTY_VOLT = 3.30

THRESH_MA = 5
MIN_DISCHARGE_MA = 50

i2c = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
ina = INA219(i2c, addr=0x40)
ina.set_calibration_32V_2A()


def clamp(x, lo, hi):
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x


def read_battery():
    bus_v = ina.get_bus_voltage()
    shunt_v = ina.get_shunt_voltage()
    current_ma = ina.get_current()
    voltage = bus_v + shunt_v

    soc = (voltage - EMPTY_VOLT) / (FULL_VOLT - EMPTY_VOLT) * 100.0
    soc = clamp(soc, 0, 100)

    if current_ma < -THRESH_MA:
        charging = True
        state_text = "Lader"
    elif current_ma > THRESH_MA:
        charging = False
        state_text = "Aflader"
    else:
        charging = False
        state_text = "Staar"

    remaining_hours = None
    remaining_text = "Ukendt"

    if current_ma > MIN_DISCHARGE_MA and soc > 0:
        remaining_mah = (soc / 100.0) * BAT_CAPACITY_MAH
        hours = remaining_mah / current_ma
        remaining_hours = hours
        h = int(hours)
        m = int((hours - h) * 60)
        remaining_text = "{}h {}m".format(h, m)

    return {
        "battery_voltage": round(voltage, 3),
        "battery_current": round(current_ma, 1),
        "battery_soc": round(soc, 1),
        "battery_remaining_hours": remaining_hours,
        "battery_remaining_text": remaining_text,
        "battery_charging": charging,
        "battery_state": state_text,
        "total_bat_mAh": BAT_CAPACITY_MAH,
    }
