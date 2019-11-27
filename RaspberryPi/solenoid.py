import time
import RPi.GPIO as GPIO

class Solenoid:
    def __init__(self):
        self.relay_pin = 26
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.relay_pin, GPIO.OUT)
    def lock(self):
        GPIO.output(self.relay_pin, 1)
        time.sleep(5)
        
    def unlock(self):
        GPIO.output(self.relay_pin, 0)
        time.sleep(5)
"""
S = Solenoid()
S.lock()
time.sleep(5)

S.unlock()
time.sleep(5)

S.lock()
time.sleep(5)
"""