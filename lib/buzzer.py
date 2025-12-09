from machine import Pin, PWM
from time import sleep

# Tilføj ledning mellem JP6 GP6 og JP1 SCLK

# Lav Buzzer object
BUZZER_PIN = 14
buzzer_pin = Pin(BUZZER_PIN, Pin.OUT)
buzzer_pwm = PWM(buzzer_pin, duty=0)


def sound(frequency, tone_duration, silence_duration):
    buzzer_pwm.duty(512)
    buzzer_pwm.freq(frequency)
    sleep(tone_duration)
    buzzer_pwm.duty(0)
    sleep(silence_duration)


