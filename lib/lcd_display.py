# lcd_display.py
from machine import Pin
from gpio_lcd import GpioLcd

lcd = GpioLcd(
    rs_pin=Pin(14),
    enable_pin=Pin(27),
    d4_pin=Pin(26),
    d5_pin=Pin(25),
    d6_pin=Pin(19),
    d7_pin=Pin(18),
    num_lines=2,
    num_columns=16
)

lcd_bl_pin = Pin(13, Pin.OUT)
lcd_bl_pin.value(1)


def lcd_backlight(on):
    lcd_bl_pin.value(1 if on else 0)


def _pad_16(text):
    if not isinstance(text, str):
        text = str(text)
    if len(text) < 16:
        text = text + (" " * (16 - len(text)))
    return text[:16]


def lcd_init_message(text):
    lcd.clear()
    lcd.putstr(_pad_16(text))


def lcd_show_status(battery, gps_fix):
    soc = battery.get("battery_soc", 0)
    volt = battery.get("battery_voltage", 0)
    state = battery.get("battery_state", "")
    rest = battery.get("battery_remaining_text", "Ukendt")

    # kort ladestatus
    if state.startswith("L"):
        st = "Lad"
    elif state.startswith("A"):
        st = "Afl"
    else:
        st = "Sti"

    # linje 1: "68.7% 3.82V Lad"
    line1 = "{:4.1f}% {:4.2f}V {}".format(soc, volt, st)
    lcd.move_to(0, 0)
    lcd.putstr(_pad_16(line1))

    # GPS tekst
    if gps_fix:
        gps_txt = "GPS OK"
    else:
        gps_txt = "GPS ?"

    # linje 2: "4h 12m GPS OK" / "Ukendt GPS ?"
    line2 = "{} {}".format(rest, gps_txt)
    lcd.move_to(0, 1)
    lcd.putstr(_pad_16(line2))
