import RPi.GPIO as GPIO
from db import sendLogOut
from db import number_of_people_inside
import time

def count_exiting_people():
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    TRIG = 20
    ECHO = 21

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    person_flag = 0
    counter = 0


    while True:
        
      GPIO.output(TRIG, False)
      time.sleep(0.1)

      GPIO.output(TRIG, True)
      time.sleep(0.00001)
      GPIO.output(TRIG, False)

      while GPIO.input(ECHO)==0:
        pulse_start = time.time()

      while GPIO.input(ECHO)==1:
        pulse_end = time.time()

      pulse_duration = pulse_end - pulse_start

      distance = pulse_duration * 17150
      distance = round(distance, 2)
              
      if distance < 50 or distance >= 1000:
        if person_flag == 0:
            if counter >= 4:
               sendLogOut()
               print(number_of_people_inside())
               person_flag = 1
               counter = 0
               print("One person left.", flush=True)
      else:  
        person_flag = 0
        counter += 1




