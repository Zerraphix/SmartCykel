# temperature

from machine import Pin
from dht import DHT11


dht = DHT11(Pin(5))

def read_temperature():
    dht.measure()
    temperature = dht.temperature()   # °C
    humidity = dht.humidity()         # %
    return {
        "temperature_c": temperature,
        "humidity": humidity
    }
