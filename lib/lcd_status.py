from machine import Pin
from gpio_lcd import GpioLcd

lcd = GpioLcd(
    rs_pin=Pin(27),
    enable_pin=Pin(25),
    d4_pin=Pin(33),
    d5_pin=Pin(32),
    d6_pin=Pin(21),
    d7_pin=Pin(22),
    num_lines=4,
    num_columns=20
)

def _pad20(txt):
    txt = "" if txt is None else str(txt)
    if len(txt) > 20:
        return txt[:20]
    return txt + (" " * (20 - len(txt)))

def lcd_show_status(data):
    speed = data.get("speed", 0)
    direction = data.get("direction", "---")
    lat = data.get("latitude")
    lon = data.get("longitude")
    soc = data.get("battery_soc", 0)
    rest = data.get("battery_remaining_text", "--:--")
    temp = data.get("temperature_c")
    line1 = "SPD:{:.1f} DIR:{}".format(float(speed), str(direction)[:3])
    if temp is not None:
        line1 = "SPD:{:.1f} T:{:.1f}C".format(float(speed), float(temp))
    if lat is None or lon is None:
        line2 = "GPS: ingen data"
        line3 = ""
    else:
        line2 = "Lat:{:.4f}".format(float(lat))
        line3 = "Lon:{:.4f}".format(float(lon))
    line4 = "Bat:{}% Rt:{}".format(int(float(soc)), rest)
    lcd.move_to(0, 0); lcd.putstr(_pad20(line1))
    lcd.move_to(0, 1); lcd.putstr(_pad20(line2))
    lcd.move_to(0, 2); lcd.putstr(_pad20(line3))
    lcd.move_to(0, 3); lcd.putstr(_pad20(line4))
