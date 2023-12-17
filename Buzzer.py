import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
buzzer_pin = 18
GPIO.setup(buzzer_pin, GPIO.OUT)

def triple_beat():
    for _ in range(3):
        GPIO.output(buzzer_pin, GPIO.HIGH)
        time.sleep(0.2)  # Buzzer on for 0.2 seconds
        GPIO.output(buzzer_pin, GPIO.LOW)
        time.sleep(0.2)  # Buzzer off for 0.2 seconds

try:
    while True:
        triple_beat()
        time.sleep(1)

except KeyboardInterrupt:
    exit()
