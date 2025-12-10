from machine import I2C, Pin
from ina219_lib import INA219

#Indstillinger
FULL_VOLT = 4.20          # Spænding ved 100% batteri
EMPTY_VOLT = 3.30         # Spænding ved 0% batteri
BAT_CAPACITY_MAH = 2000   # Batterikapacitet i mAh (fx 2000mAh)

#Opsæt I2C og INA219
i2c = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
ina = INA219(i2c, addr=0x40)
ina.set_calibration_32V_2A()

def read_battery():
    # Læs spænding og strøm fra INA219
    bus_voltage = ina.get_bus_voltage()      # Spænding på bussen (V)
    shunt_voltage = ina.get_shunt_voltage()  # Spænding over shunt (V)
    current_ma = abs(ina.get_current())      # Strøm i mA (absolut værdi)
    
    #Batteriets samlede spænding er bus + shunt
    battery_voltage = bus_voltage + shunt_voltage

    #Beregn SoC (State of Charge)
    #Simpel lineær beregning mellem EMPTY_VOLT og FULL_VOLT
    soc = (battery_voltage - EMPTY_VOLT) / (FULL_VOLT - EMPTY_VOLT) * 100

    # Sørg for at SoC altid ligger mellem 0 og 100%
    if soc < 0:
        soc = 0
    if soc > 100:
        soc = 100

    #Beregn resterende tid
    #Hvis strømmen er meget lille, kan vi ikke beregne tid → uendelig / ukendt
    if current_ma < 1:
        remaining_hours = None
        remaining_text = "Ukendt"
    else:
        #Hvor mange mAh er der tilbage i batteriet?
        remaining_mAh = (soc / 100.0) * BAT_CAPACITY_MAH

        #Timer tilbage = mAh / mA
        remaining_hours = remaining_mAh / current_ma

        #Lav timer til "Xh Ym" tekst
        h = int(remaining_hours)
        m = int((remaining_hours - h) * 60)
        remaining_text = "{}h {}m".format(h, m)

    #Returnér simple værdier
    return {
        "battery_voltage": round(battery_voltage, 3),  # V
        "battery_current": round(current_ma, 1),       # mA
        "battery_soc": round(soc, 1),                  # %
        "battery_remaining_hours": remaining_hours,    # tal eller None
        "battery_remaining_text": remaining_text,      # tekst
    }


data = read_battery()
print(data)
