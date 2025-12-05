from machine import I2C, Pin
from time import sleep, ticks_ms
from mpu6050 import MPU6050

BRAKE_DECEL_THRESHOLD = -0.15 # deacceleration i g der skal til
BRAKE_HOLD_MS = 800 # hvor længe lyset skal være tændt (ms)
ACC_SCALE = 16384.0

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
imu = MPU6050(i2c)

ax_prev = 0.0
brake_off_time = 0


def check_brake():
    global ax_prev, brake_off_time

    now = ticks_ms()

    # Læs accelerationen fra IMU og konverter til g
    vals = imu.get_values()
    ax = vals["acceleration x"] / ACC_SCALE

    # Ændring i acceleration siden sidst.
    delta_a = ax - ax_prev
    ax_prev = ax

    # Hvis deacceleration er under threshold. Start/forlæng "hold"-periode
    if delta_a < BRAKE_DECEL_THRESHOLD:
        brake_off_time = now + BRAKE_HOLD_MS

    brake_active = now < brake_off_time
    
    return brake_active





vals = imu.get_values()
ax_prev = vals["acceleration x"] / ACC_SCALE
