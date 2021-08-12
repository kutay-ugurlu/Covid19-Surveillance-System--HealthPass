from gpiozero import Button
import time
from time import sleep 
from screen import screen 
from four_choice import four_choice
smell_ok = None
IF_SMELL = None
SMELL_CHOICES = None
choices = None
selected_smell = None

def set_choices():
    global choices
    choices = four_choice(SMELL_CHOICES,True)
    
def f_yellow1():
    print("sari1")
    global IF_SMELL
    global selected_smell
    selected_smell = choices[0]
    if smell_ok == choices[0]:
        IF_SMELL = True
        screen([10],[20],["Smell ok."])
        sleep(2)
        four_choice(SMELL_CHOICES, False)
    else:
        screen([10],[20],["Smell wrong."])
        IF_SMELL = False
def f_yellow2():
    print("sari2")
    global IF_SMELL
    global selected_smell
    selected_smell = choices[1]
    if smell_ok == choices[1]:
        IF_SMELL = True
        screen([10],[20],["Smell ok."])
        sleep(2)
        four_choice(SMELL_CHOICES,False)
    else:
        screen([10],[20],["Smell wrong."])
        IF_SMELL = False
def f_yellow3():
    print("sari3")
    global IF_SMELL
    global selected_smell
    selected_smell = choices[2]
    if smell_ok == choices[2]:
        IF_SMELL = True
        screen([10],[20],["Smell ok."])
        sleep(2)
        four_choice(SMELL_CHOICES,False)
    else:
        screen([10],[20],["Smell wrong."])
        IF_SMELL = False
# def f_yellow4():
#     global IF_SMELL
#     global selected_smell
#     selected_smell = choices[3]
#     if smell_ok == choices[3]:
#         IF_SMELL = True
#         screen([10],[20],["Smell ok."])
#         sleep(2)
#         four_choice(SMELL_CHOICES,False)
#     else:
#         screen([10],[20],["Smell wrong."])
#         IF_SMELL = False
def f_green1():
    print("yesil1")
    global smell_ok
    smell_ok = correct1
def f_green2():
    print("yesil2")
    global smell_ok
    smell_ok = correct2


yellow1 = Button(26, bounce_time=0.1)
yellow2 = Button(27, bounce_time=0.1)
yellow3 = Button(17, bounce_time=0.1)
yellow4 = Button(13, bounce_time=0.1)
green1 = Button(22, bounce_time=0.1)
green2 = Button(19, bounce_time=1)

green1.when_pressed = f_green1
green2.when_pressed = f_green2
yellow1.when_pressed = f_yellow1
yellow2.when_pressed = f_yellow2
yellow3.when_pressed = f_yellow3
yellow4.when_pressed = f_green2

def ret_if_smell():
    return IF_SMELL

def smell_test(wait_for_user=120):
    global IF_SMELL
    while smell_ok == None:
        sleep(0.1)
    t1 = time.time()
    print("SMELL OK:",smell_ok, flush=True)
    IF_SMELL = None
    set_choices()
    while IF_SMELL == None and time.time()-t1 < wait_for_user:
        time.sleep(0.1)
    print("selected smell:", selected_smell, flush=True)
    return (IF_SMELL, smell_ok, selected_smell)
    
