
import RPi.GPIO as GPIO
from time import sleep

def open_the_lock_for_n_seconds(n:int):

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(25,GPIO.OUT)
    GPIO.output(25,GPIO.HIGH)
    sleep(n)
    GPIO.cleanup(25)



