from machine import Pin
from gpio_lcd import GpioLcd

lcd = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
              d4_pin=Pin(33), d5_pin=Pin(32), d6_pin=Pin(21), d7_pin=Pin(22),
              num_lines=4, num_columns=20)



def lcd_show_status(data):
    soc = data.get("battery_soc", 0)
    lat = round(data.get("latitude"),2)
    lon = round(data.get("longitude"),2)
    speed = round(data.get("speed"),2)
    
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr(f"Km/t: {speed}")
    lcd.move_to(0,1)
    lcd.putstr(f"Battery: {soc}%")
    lcd.move_to(0,2)
    lcd.putstr(f"Lat:{lat} Lon:{lon}")

