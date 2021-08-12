from screen import screen, reset_screen
reset_screen()
from mask_consecutive import classify_n_frames
from distance_n_temp import measure_temp, measuretemp
from doorlock import open_the_lock_for_n_seconds
import smell
from time import sleep
import threading
from distancesensor import count_exiting_people

# Start exiting people thread here 
t1 = threading.Thread(target=count_exiting_people)
t1.start()

# Internet Connection Test Loop (am 48 yo man from Somalia, sorry for my bed england)
if_connection = False
while not if_connection:
    try:
        from db import sendLog, sendLogIn, sendLogOut, number_of_people_inside, getOptions, setNumberofPeople
        if_connection = True
    except:
        sleep(0.5)

    
# Collect params from db
Option_dict = getOptions()
smell.correct1 = Option_dict["correct1"]
smell.correct2 = Option_dict["correct2"]
option1 = Option_dict["option1"]
option2 = Option_dict["option2"]
option3 = Option_dict["option3"]
MaxPeople = Option_dict["maxpeople"]

setNumberofPeople(9)

# First start with smell test
smell.SMELL_CHOICES = [option1,option2,option3]



#TESTs
while True:
    
    
    if number_of_people_inside() >= MaxPeople:
        screen([20,20,20],[10,20,30],["INSIDE","IS TOO","CROWDED"])
        sleep(1)
        continue
    
    smell.set_choices()
    
    screen([20,20,20],[10,20,30],["DISINFECT","YOUR","HANDS"])
    
    
    # Inıtialize smell parameters for the new user 
    smell.smell_ok = None
    smell.IF_SMELL = None
    smell.selected_smell = None
    isAllowed = None
    
    ## Tests begin, can be written in while loop
    
    if_smell,corr_smell,guess_smell = smell.smell_test(wait_for_user=20)

    if if_smell == None:
        continue
    
    if_smell = corr_smell == guess_smell
    
    # Measure Temp
    temp = measuretemp()
    print("TEMPERATURE:",temp, flush=True)
    print("maskeye giriyu")
    # Classify mask
    if_mask = classify_n_frames(10,5)
    print("IF MASK: ",if_mask, flush=True)
    
    # Get people inside of the building at that moment
    PeopleInside = number_of_people_inside()
    print("PPL INSIDE: ",PeopleInside, flush=True)

    ## Decider Unit
    if if_mask and temp<37.5 and PeopleInside<MaxPeople:
        open_the_lock_for_n_seconds(7.5)
        sendLogIn()
        isAllowed=True
    elif if_mask and temp<38 and if_smell and PeopleInside<MaxPeople:
        open_the_lock_for_n_seconds(7.5)
        sendLogIn()
        isAllowed=True
    else:
        print("You are not allowed to enter.", flush=True)
        isAllowed=False
    
    sendLog(temp, corr_smell, guess_smell, if_mask, PeopleInside, isAllowed)
    
    PeopleInside = number_of_people_inside()
    
    print(temp, corr_smell, guess_smell, if_mask, PeopleInside, isAllowed)
    
