from machine import Pin
from dht import DHT11
from time import sleep

DHT_PIN = 23
sensor = DHT11(Pin(DHT_PIN))

def read_temperature():
    try:
        sensor.measure()
        t = sensor.temperature()
        h = sensor.humidity()
        return {
            "temperature_c": t,
            "humidity": h
        }
    except:
        return {
            "temperature_c": None,
            "humidity": None
        }
