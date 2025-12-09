import time
import ldr_sensor
import acceloremeter

ldr = "MØRKT"
last_brake_check = True
while True:

    if ldr_sensor.DayorNight() != ldr or acceloremeter.check_brake() != last_brake_check:
        if acceloremeter.check_brake():
            bremse_lys()
        elif ldr_sensor.DayorNight() == "MØRKT":
            mørke_lys()
        else:
            light_off()
        last_brake_check = acceloremeter.check_brake()
        ldr = ldr_sensor.DayorNight()
            
    time.sleep(0.5)