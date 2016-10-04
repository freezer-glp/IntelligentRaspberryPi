#!/usr/bin/python
import os
import fanController
import traceback

StartFanTemp = 40
StopFanTemp = 35

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return float(res.replace("temp=","").replace("'C\n",""))
    
def fanScheduler():
    try:
        temp = round(getCPUtemperature())
        if temp > StartFanTemp :
            fanController.startFan()
        elif temp < stopFanTemp :
            fanController.stopFan()
    except:
        traceback.print_exc()
        
if __name__ == "__main__":
    fanScheduler()
