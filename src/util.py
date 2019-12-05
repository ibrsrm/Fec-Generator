from time import time
from datetime import datetime

def getCurretTime() :
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    return time

def getCurrentTimeMs() : 
    return int(round(time() * 1000))    
