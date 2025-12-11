from machine import I2C, Pin
from time import sleep, ticks_ms
from mpu6050 import MPU6050

BRAKE_DECEL_THRESHOLD = -0.15 # deacceleration i g der skal til
BRAKE_HOLD_MS = 800 # hvor længe lyset skal være tændt (ms)
ACC_SCALE = 16384.0

TAMPER_THRESHOLD = 0.50  # change in g before we say "moved"

i2c = None
imu = None

ax_prev = None                  # til brake-beregning
prev_ax = None                  # til tamper-check
prev_ay = None
prev_az = None

brake_off_time = 0


def init():
    global i2c, imu, ax_prev, prev_ax, prev_ay, prev_az, brake_off_time

    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
    imu = MPU6050(i2c)

    ax_prev = get_vals_g()[0]
    prev_ax = prev_ay = prev_az = None
    brake_off_time = 0

def get_vals_g():
    vals = imu.get_values()
    ax = vals["acceleration x"] / ACC_SCALE
    ay = vals["acceleration y"] / ACC_SCALE
    az = vals["acceleration z"] / ACC_SCALE
    return ax, ay, az

def check_brake():
    global ax_prev, brake_off_time
    
    now = ticks_ms()
    ax = get_vals_g()[0]

    # Ændring i acceleration siden sidst.
    delta_a = ax - ax_prev
    ax_prev = ax

    # Hvis deacceleration er under threshold. Start/forlæng "hold"-periode
    if delta_a < BRAKE_DECEL_THRESHOLD:
        brake_off_time = now + BRAKE_HOLD_MS

    brake_active = now < brake_off_time
    
    return brake_active

def check_tamper():
    global prev_ax, prev_ay, prev_az

    ax, ay, az = get_vals_g()

    if prev_ax is None:
        prev_ax, prev_ay, prev_az = ax, ay, az
        return False

    # Vi checker om der er sket en hvis ændring i position
    moved = (
        abs(ax - prev_ax) > TAMPER_THRESHOLD or
        abs(ay - prev_ay) > TAMPER_THRESHOLD or
        abs(az - prev_az) > TAMPER_THRESHOLD
    )

    prev_ax, prev_ay, prev_az = ax, ay, az

    return moved



if __name__ == "__main__":
    init()
    test = check_tamper()
    print(test)

