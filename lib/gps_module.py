# gps_module.py
from machine import UART
from time import ticks_ms, ticks_diff, sleep_ms
from gps_simple import GPS_SIMPLE

uart = UART(2, 9600)
gps = GPS_SIMPLE(uart)

def get_lat_lon(timeout_sec=5):
    """Returnerer (lat, lon) eller None hvis der ikke er GPS-fix."""
    start = ticks_ms()
    timeout_ms = timeout_sec * 1000

    while ticks_diff(ticks_ms(), start) < timeout_ms:
        try:
            if gps.receive_nmea_data():
                lat = gps.get_latitude()
                lon = gps.get_longitude()
                speed = gps.get_speed()
                valid = gps.get_validity()  # "A" = aktiv fix

                if lat != -999.0 and lon != -999.0 and valid == "A":
                    return lat, lon, speed
        except Exception as e:
            print("GPS fejl i get_lat_lon:", e)
            # Hvis der sker en fejl i gps_simple, så stop og returner None
            return None

        sleep_ms(500)

    return None