from time import sleep
from random import shuffle
from screen import screen
     
     
def four_choice(choices, if_screen):

     
#      spi = busio.SPI(board.SCK, MOSI=board.MOSI)
#      dc = digitalio.DigitalInOut(board.D6) # data/command
#      cs = digitalio.DigitalInOut(board.CE0) # Chip select
#      reset = digitalio.DigitalInOut(board.D5) # reset
#       
#      display = adafruit_pcd8544.PCD8544(spi, dc, cs, reset)
#      display.bias = 4
#      display.contrast = 60
#      display.fill(1)
#         
#         
#      display.text("1)"+choices[0],1,0,0)
#      display.text("2)"+choices[1],1,9,0)
#      display.text("3)"+choices[2],1,18,0)
#      display.text("4)"+choices[3],1,27,0)
#      display.show()

    shuffle(choices)
       
    ordered_choices = [str(i+1) + ")" + choices[i] for i in range(len(choices))]
    
    if if_screen:
        screen([1,1,1],[9, 18, 27],ordered_choices)

     
    return choices
    
    
    