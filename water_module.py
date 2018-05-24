import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

def openInterval(seconds):
    if seconds is None:
        seconds = 2

    print("GPIO setup")
    GPIO.setup(18, GPIO.OUT)
    time.sleep(seconds)

    print("GPIO cleanup")
    GPIO.cleanup()

