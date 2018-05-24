import RPi.GPIO as GPIO
import time

def water():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    print("GPIO setup")
    GPIO.setup(18, GPIO.OUT)
    time.sleep(3)

    print("GPIO cleanup")
    GPIO.cleanup()

