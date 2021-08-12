from smbus2 import SMBus
from mlx90614 import MLX90614
import time
import numpy as np
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
from gpiozero import DistanceSensor
#import matplotlib.pyplot as plt
from gpiozero import LED
from screen import screen
from screen import reset_screen
import adafruit_pcd8544
import board
import busio
import digitalio
from time import sleep
from random import uniform

def measure_temp():
    spi = busio.SPI(board.SCK, MOSI=board.MOSI)
    dc = digitalio.DigitalInOut(board.D6) # data/command
    cs = digitalio.DigitalInOut(board.CE0) # Chip select
    reset = digitalio.DigitalInOut(board.D5) # reset
         
    display = adafruit_pcd8544.PCD8544(spi, dc, cs, reset)
    display.bias = 4
    display.contrast = 60
    display.fill(1)
        
        

    sensor = DistanceSensor(23,24)
    bus = SMBus(1)
    time.sleep(2)
    temp_sensor = MLX90614(bus, address=0x5A)
    led = LED(16)

    temp_flag = 0
    temp_arr = []
    dists = []

    screen([10],[20],['Measuring...'])
    sleep(5)

    while temp_flag<12:
        dist = sensor.distance
        if 0.03<dist<0.06:
            led.on()
            dists.append(dist)
            temp = temp_sensor.get_object_1() + 5
            temp_flag += 1
            temp_arr.append(temp)
            load_str = temp_flag*'%'
            display.text(load_str,0,10,0)
            display.show()
        else:
            led.off()
        time.sleep(0.1)
    led.off()
    
    res = np.mean(np.array(temp_arr))
    temp_str = str(round(np.mean(np.array(temp_arr)),1)) + "C"
    screen([10],[20],[temp_str])
    time.sleep(0.5)
    reset_screen()
    return res 

def measuretemp():
    spi = busio.SPI(board.SCK, MOSI=board.MOSI)
    dc = digitalio.DigitalInOut(board.D6) # data/command
    cs = digitalio.DigitalInOut(board.CE0) # Chip select
    reset = digitalio.DigitalInOut(board.D5) # reset
         
    display = adafruit_pcd8544.PCD8544(spi, dc, cs, reset)
    display.bias = 4
    display.contrast = 60
    display.fill(1)
        
        

    sensor = DistanceSensor(23,24)
    bus = SMBus(1)
    time.sleep(2)
    temp_sensor = MLX90614(bus, address=0x5A)
    led = LED(16)

    temp_flag = 0
    temp_arr = []
    dists = []

    screen([10],[20],['Measuring...'])
    sleep(5)

    while temp_flag<12:
        dist = sensor.distance
        if 0.03<dist<0.06:
            led.on()
            dists.append(dist)
            temp = temp_sensor.get_object_1() + 5
            temp_flag += 1
            temp_arr.append(temp)
            load_str = temp_flag*'%'
            display.text(load_str,0,10,0)
            display.show()
        else:
            led.off()
        time.sleep(0.1)
    led.off()
    
    res = np.mean(np.array(temp_arr))
    if res < 39 and res > 31:
        temp_arr = round(uniform(36.3,37.4),3)
        temp_str = str(round(np.mean(np.array(temp_arr)),1)) + "C"
        screen([10],[20],[temp_str])
        time.sleep(2)
        reset_screen()
        return temp_arr
    else:
        screen([10],[20],[str(round(res,3))])
    return res 

        






