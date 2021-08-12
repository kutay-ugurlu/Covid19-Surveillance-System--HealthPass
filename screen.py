import adafruit_pcd8544
import board
import busio
import digitalio
from time import sleep
 
spi = busio.SPI(board.SCK, MOSI=board.MOSI)
dc = digitalio.DigitalInOut(board.D6) # data/command
cs = digitalio.DigitalInOut(board.CE0) # Chip select
reset = digitalio.DigitalInOut(board.D5) # reset

display = adafruit_pcd8544.PCD8544(spi, dc, cs, reset)
display.bias = 4
display.contrast = 60

def screen(rows,cols,Strings):
    

    display.fill(1)
    
    for i in range(len(cols)):
        display.text(Strings[i],rows[i],cols[i],0)
    display.show()
       
def reset_screen():
    display.fill(1)
    display.show()
