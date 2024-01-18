import time
import numpy as np

#This module has been created to simulate a human employee hours

def current_time():
   return int(time.strftime("%H%M%S"))

def Khronos(borne1, borne2):
    #We only have two log in and two log out a day:
    #respectively morning and afternoun connections and afternoun and night unconnections 
    chrono = []
    i = 0
    for j in range(0, 4):
        #A uniform law of repartition has been choosen here to represent perfect hasard
        chrono.append(int(np.random.uniform(borne1, borne2)))
        #Then a 0 is numbers are converted to string and 0 is added before any cypher to respect 
        #current_time() format 
        if chrono[i] < 10:
           chrono[i] = f'0{chrono[i]}'
        else:
            chrono[i] = str(chrono[i])
        i+=1
    return chrono

def robotUnion(): 
    i = 0
    schedule = []
    #Hours
    H = ["7", "12", "13", "21"]
    #Minutes
    M = Khronos(30, 59)
    #Seconds
    S = Khronos(0, 59)
    for j in range(0,4):
        schedule.append(int(H[i] + M[i] + S[i]))
        i+=1
    return schedule

def time2sec(H):
    #convert to string to select numbers as list elements
    H = str(H)
    #case HHMMSS
    if len(H) == 6:
        h = int(H[0:2])*3600
        m = int(H[2:4])*60
        s = int(H[4:6])
        timeInSec = h+m+s
    #case HMMSS
    elif len(H) == 5:
        h = int(H[0])*3600
        m = int(H[1:3])*60
        s = int(H[3:5])
        timeInSec = h+m+s
    #case MMSS
    elif len(H) == 4:
        m = int(H[0:2])*60
        s = int(H[2:4])
        timeInSec = m+s
    #case MSS
    elif len(H) == 3:
        m = int(H[0])*60
        s = int(H[1:3])
        timeInSec = m+s
    #case SS and S
    else:
        s = int(H)
        timeInSec = s
    return(timeInSec)

