from machine import Pin, I2C
import time

I2C_SCL_PIN = 22
I2C_SDA_PIN = 21
MPU6050_ADDR = 0x68

BRAKE_DECEL_THRESHOLD = -0.15   # hvor meget deceleration (g) der skal til
BRAKE_HOLD_MS = 800             # hvor længe lyset skal være tændt (ms)

PWR_MGMT_1   = 0x6B
ACCEL_XOUT_H = 0x3B

i2c = I2C(0, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=400000)

def read_raw_word(reg):
    high = i2c.readfrom_mem(MPU6050_ADDR, reg, 1)[0]
    low  = i2c.readfrom_mem(MPU6050_ADDR, reg + 1, 1)[0]
    value = (high << 8) | low
    if value > 32767:
        value -= 65536
    return value

def read_accel_x_g():
    ax = read_raw_word(ACCEL_XOUT_H)
    return ax / 16384.0   # konverter til g (tyngdeacceleration)

ax_prev = read_accel_x_g()
brake_off_time = 0

while True:
    now = time.ticks_ms()

    # læs nuværende acceleration
    ax = read_accel_x_g()
    delta_a = ax - ax_prev
    ax_prev = ax


    if delta_a < BRAKE_DECEL_THRESHOLD:
        brake_off_time = now + BRAKE_HOLD_MS

    
    if now < brake_off_time:

        brake_state = "ON"
    else:

        brake_state = "off"

    print("ax={:+.2f}g | Δa={:+.2f}g | BRAKE={}".format(ax, delta_a, brake_state))

    time.sleep(0.1)
