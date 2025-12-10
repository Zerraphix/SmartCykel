from machine import I2C, Pin
from time import sleep, ticks_ms
from mpu6050 import MPU6050

BRAKE_DECEL_THRESHOLD = -0.15 # deacceleration i g der skal til
BRAKE_HOLD_MS = 800 # hvor længe lyset skal være tændt (ms)
ACC_SCALE = 16384.0

TAMPER_THRESHOLD = 0.40  # change in g before we say "moved"

prev_ax = None
prev_ay = None
prev_az = None

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
imu = MPU6050(i2c)

brake_off_time = 0


def check_brake():
    global ax_prev, brake_off_time
    
    now = ticks_ms()
    ax = check_acceleration()

    # Ændring i acceleration siden sidst.
    delta_a = ax - ax_prev
    ax_prev = ax

    # Hvis deacceleration er under threshold. Start/forlæng "hold"-periode
    if delta_a < BRAKE_DECEL_THRESHOLD:
        brake_off_time = now + BRAKE_HOLD_MS

    brake_active = now < brake_off_time
    
    return brake_active

def check_acceleration():
    # Læs accelerationen fra IMU og konverter til g
    vals = imu.get_values()
    ax = vals["acceleration x"] / ACC_SCALE
    
    return ax

def get_vals_g():
    vals = imu.get_values()
    ax = vals["acceleration x"] / ACC_SCALE
    ay = vals["acceleration y"] / ACC_SCALE
    az = vals["acceleration z"] / ACC_SCALE
    return ax, ay, az

def check_tamper():
    """Return True if the bike was moved since last check."""
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




