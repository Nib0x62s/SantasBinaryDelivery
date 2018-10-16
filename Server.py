#!/usr/bin/python
# -*- coding: utf-8 -*-
import multiprocessing
from time import sleep
from threading import Thread
import sys
import socket
import thread
import random
import time

#Pins List
pins = []

#house number counter
houseNumber = 1

#Booleans
timesUP = False

# Colors
HEADER = '\033[37m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def menu(clientsocket):
    clientsocket.send(OKGREEN + '| Main Menu\n' + ENDC 
            + OKBLUE + '| Press the respected character + Enter to continue to the following options:\n' + ENDC 
            + HEADER + ' - [R]ead Challenge\n' 
            + ' - [D]eliver presents\n' 
            + ' - [P]ractice delivering presents\n' 
            + ' - [Q]uit\n' 
            + ' > ')
    while True: 
        command = str(clientsocket.recv(4096)).strip()
        if len(command) > 0:
            print(str(clientsocket.getpeername()) + ' >> ' + str(command))
        if(command == 'R'):
            displayChallenge(clientsocket)
            break
        elif command == 'D':
            deliverPresents(clientsocket)
            break
        elif command == 'P':
            practiceDelivery(clientsocket)
            break
        elif(command == 'Q'):
            clientsocket.close()
        else:
            clientsocket.send(WARNING + "\n| Command not recognized\n\n")
            break

def initMessage(clientsocket):
    clientsocket.send(OKGREEN \
        + """\t                                                           __.  .--,
\t                                                    _.-.=,{\/ _/  /`)
\t ~0  (_|  . - ' - . _ . - ' - . VS . - ' - .  _..-'`-(`._(_.;`   /
\t|(_~|^~~|                                          (__\_________/___,
\tTT/_ T\"T                                          (_____Y_____Y___,jgs\n\n""")
    clientsocket.send('       L33T H4CK3R                                                SANTA\n\n')
    clientsocket.send('\t\t  Welcome to Santas Binary Delivery challenge!\n\n' + ENDC)

def displayChallenge(s):
    s.send(FAIL + '\n +----------------------------------------------------------------------------------------------------------------------+\n ')
    s.send('\n\tThe challenge is to deliver presents to one city equal to or less than santas fastest time.\n')
    s.send('\n\tDetails:\n')
    s.send('\t\t 1) Santa delivers presents to 2160 cities where he spends an equal amount of time in each city.\n')
    s.send('\t\t 2) Each city contains 4 houses and each house has a 5 digit numerical pin.\n')
    s.send('\t\t 3) Santa is letting you borrow his list of pins he has to every house called pins.txt\n')
    s.send('\t\t 4) Santa\'s fastest time to visit all 2160 cities is 6 hours.\n')
    s.send('\n\tGood Luck!\n')
    s.send('\tSincerely, Nib0x62s\n\n')
    s.send(' +----------------------------------------------------------------------------------------------------------------------+ \n\n' + ENDC)
    

def deliverPresents(s):
    global Thread
    s.send(OKGREEN + '\n| Deliver Presents Menu\n' 
            + '| To deliver presents enter in the 5 digit pin of the house and the elves will take care of the rest!\n' + ENDC 
            + '| The PIN readers are slow and can only process a pin every one and a half decisecond.\n' 
            + '| Any non 5-digit pin will trigger the security and end the delivery process.\n' 
            + '| Type Q into a PIN reader to inform santa that you give up.\n' + ENDC 
            + HEADER + ' - [S]tart\n' 
            + ' - [R]eturn to main menu\n' + 
            ' > ')
    while True:
        command = str(s.recv(4096)).strip()
        print(str(s.getpeername()) + ' >> ' + str(command))
        if not command:
            break;
        if(command=='S'):
            print("S Entered")
            t = Thread(target = startTimer)
            t.start()
            startDelivering(s)
            t.join()
            s.send("\n")
            break
        else:
            s.send("\n")
            break
    
   
def startTimer():
    global houseNumber
    global timesUP

    myTime = time.time()
    timeElapsed = 0
    while timeElapsed != 10:
        timeElapsed = time.time() - myTime 
    print("Setting timesUP to TRUE time: " + str(timeElapsed))    
    timesUP = True

def startDelivering(s):
    global houseNumber
    global timesUP
    global pins
    attempts = 0
    location = random.randint(0,8639)
    message = "not"
    pinset = False
    timesUP = False
    houseNumber = 1

    print(str(timesUP) + " : " + str(houseNumber))
    while(timesUP == False and houseNumber < 5):
        housepin = pins[location]
        #housepin = 44444
        print(housepin)
        s.send(HEADER + '\n Enter the 5 digit pin of the house #' + str(houseNumber) + ': ' + ENDC)
        pin = str(s.recv(4096)).strip()
        print(str(s.getpeername()) + ' >> ' + str(pin))
        if(timesUP == True):
            break
        if(pin == str(housepin)  and timesUP == False):
            s.send(OKGREEN + '| Access Granted! Presents Delivered!\n' + ENDC)
            houseNumber += 1
            attempts += 1
            location = random.randint(0,8639)
        elif(pin == ''):
            s.send(WARNING + "| Nothing was entered, attempt not recorded. Stopping delivery.\n" + ENDC)
            break
        elif(str(pin).isdigit() and len(str(pin))==5):
            loc = 0
            pinLoc = -1
            housepinLoc = -1
            for x in pins:
                 if(x==pin):
                     pinLoc = loc
                 if(x==housepin):
                     housepinLoc = loc
                 loc += 1
            print(str(pinLoc) + " : " + str(housepinLoc))
            if(pinLoc != -1 and housepinLoc != -1):
                if(pinLoc < housepinLoc):
                    message = "lower"
                if(pinLoc > housepinLoc):
                    message = "higher"
            else:
                message = "non exisitent"
            s.send(FAIL \
                    + '| The Pin: '
                    + pin
                    + '\'s location in pins.txt is ' + message + ' compared to the location of the correct pin!'
                    + ' Attempt #' 
                    + str(attempts)
                    + "\n"
                    + ENDC)
            attempts += 1
        elif(str(pin) == 'Q'):
            s.send(WARNING + "| [Q]uitting\n" + ENDC)
            break
        else:
            s.send(WARNING + "| " + pin + " is not a valid attempt, try using an exisitng pin inside pins.txt? Stopping delivery.\n" + ENDC)
            break
        
        sleep(0.15)

    if(houseNumber == 5):
        s.send(OKGREEN + "\nCongrats!, You deliverd presents to: " + str(houseNumber - 1) + " house(s) out of 5 in ____ seconds with " + str(attempts) + " attempts!\n" + ENDC)
        printFlag(s)
    elif(timesUP == True):
        print(str(timesUP))
        print('Sending fail...')
        s.send(WARNING + "\n| Too slow!, You're going to have to be faster than that to beat Santa!\n" + ENDC 
                + "\nYou delivered presents to: " + str(houseNumber - 1) + " house(s) out of 5 in ___ seconds with " + str(attempts) + " attempts.\n" 
                + "All house pins are being changed.\n")
    else:
        print("no")
        #s.send("And error happened in transmission :(")


def practiceDelivery(s):
    s.send(OKGREEN + '\n| Practice Menu\n'
            + '| To deliver presents enter the exisitng 5 digit pin of the house and the elves will do the rest!\n'
            + '| The pin readers are slow and can only process a pin every one and a half decisecond\n' 
            + '| Any non 5 digit pin will trigger the security and end the delivery process.\n' 
            + '| Type Q into a pin reader to inform santa that you give up\n' 
            + '| Hint: Heres the practice pins.txt file contents {22303, 99219, 33440, 31033}\n')
    pins = ['22303', '99219', '33440', '31033']
    houseNumber = 1
    attempts = 0
    location = random.randint(0,3)
    while houseNumber < 5:
        s.send(HEADER + '\n Enter the 5 digit pin of the house #' + str(houseNumber) + ': ' + ENDC)
        pin = str(s.recv(1024).strip())
        housepin = pins[location]
        if pin == housepin:
            s.send(OKGREEN + 'Access Granted, Presents Delivered\n' + ENDC)
            attempts += 1
            houseNumber += 1
            location = random.randint(0,3)
        elif(pin == ''):
            s.send(WARNING + "| Nothing was entered, attempt not recorded. Stopping delivery.\n" + ENDC)
            break
        elif(str(pin).isdigit() and len(str(pin))==5):
            loc = 0
            housepinLoc = -1
            pinLoc = -1
            for x in pins:
                print(str(x) + " : " + str(pin) + " : " + str(housepin))
                if(x==pin):
                    pinLoc = loc
                if(x==housepin):
                    housepinLoc = loc
                loc += 1
            print(str(pinLoc) + " : " + str(housepinLoc))
            if(pinLoc != -1 and housepinLoc != -1):
                if(pinLoc < housepinLoc):
                    message = "lower"
                if(pinLoc > housepinLoc):
                    message = "higher"
            else:
                message = "non exisitent"
            
            s.send(FAIL \
                    + '| The Pin: '
                    + pin
                    + '\'s location in pins.txt is ' + message + ' compared to the location of the correct pin!'
                    + ' Attempt #'
                    + str(attempts)
                    + "\n"
                    + ENDC)
            attempts += 1
        elif(str(pin) == 'Q'):
            s.send(WARNING + "| [Q]uitting\n" + ENDC)
            break
        else:
            s.send(WARNING + "| " + pin + " is not a valid attempt, try using an exisitng pin inside pins.txt? Stopping delivery.\n" + ENDC)
            break

        sleep(0.15)
    if(houseNumber == 5):
        s.send(OKGREEN + "\nCongrats!, You deliverd presents to: " + str(houseNumber - 1) + " house(s) out of 5 in ____ seconds with " + str(attempts) + " attempts!\n" + ENDC)
        printFlagMeh(s)
    s.send("\n")
  

def printFlag(s):
    s.send(". -------------------------------------------------------------------.\n"        
+ "| [Esc] [F1][F2][F3][F4][F5][F6][F7][F8][F9][F0][F10][F11][F12] o o o|\n"        
+ "|                                                                    |\n"        
+ "| [`][1][2][E][4][5][6][7][8][9][0][-][=][_<_] [I][H][U] [N][/][*][-]|\n"        
+ "| [|-]" + OKGREEN + "[Q][W][3][R][T][Y]" + ENDC + "[U][I][O][P][{][}] | | [D][E][D] [7][8][9]|+||\n"        
+ "| [CAP][A][S][D][F][G][H][J][K][L][;]['][#]|_|           [4][5][6]|_||\n"        
+ "| [^][\][Z][X][C][V][B][N][M][,][.][/] [__^__]    [^]    [1][2][3]| ||\n"
+ "| [c]   [a][________________________][a]   [c] [<][V][>] [ 0  ][.]|_||\n"
+ "`--------------------------------------------------------------------'")

def printFlagMeh(s):
    s.send("\nFlag: Meh go get a real flag\n")

def serverSetup():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #host = socket.gethostname()
    port = 57777
    print('Settig up server... ')
    s.bind(('206.189.233.228', port))
    s.listen(5)
    print('Waiting for clients... ')
    while True:
        c, addr = s.accept()
        print("New connection from: ", addr)
        thread.start_new_thread(new_client,(c,addr))
    s.close()

def new_client(clientsocket, addr):
    initMessage(clientsocket)
    while True:
        menu(clientsocket)

def setupPins():
    global pins
    pins = [line.rstrip('\n') for line in open("pins.txt")]
    
setupPins()
serverSetup()
