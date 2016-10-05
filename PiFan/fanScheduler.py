#!/usr/bin/python
import os
import fanController
import traceback

StartFanTemp = 45
StopFanTemp = 34

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return float(res.replace("temp=","").replace("'C\n",""))
    
def fanScheduler():
    try:
        temp = int(round(getCPUtemperature()))
        print "CPU temp:" + str(temp)
        if temp >= StartFanTemp :
            fanController.startFan()
            print "Start fan."
        elif temp <= StopFanTemp :
            fanController.stopFan()
            print "Stop fan."
    except:
        traceback.print_exc()
        
if __name__ == "__main__":
    fanScheduler()
