from machine import UART
from time import ticks_ms, ticks_diff, sleep_ms
from gps_simple import GPS_SIMPLE

uart = UART(2, 9600)
gps = GPS_SIMPLE(uart)

def read_gps(timeout_sec=5):
    start = ticks_ms()
    timeout_ms = timeout_sec * 1000

    while ticks_diff(ticks_ms(), start) < timeout_ms:
        if gps.receive_nmea_data():
            lat = gps.get_latitude()
            lon = gps.get_longitude()
            speed = gps.get_speed()
            direction = gps.get_course()  # hvis din GPS_SIMPLE har course

            valid = gps.get_validity()
            if lat != -999.0 and lon != -999.0 and valid == "A":
                return {
                    "latitude": lat,
                    "longitude": lon,
                    "speed": speed,
                    "direction": direction
                }

        sleep_ms(500)

    return None
