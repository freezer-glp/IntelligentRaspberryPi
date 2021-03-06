#!/usr/bin/python
import os
import time
import FanController
import traceback

StartFanTemp = 45
StopFanTemp = 34
ISOTIMEFORMAT="[%Y-%m-%d %X]"
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return float(res.replace("temp=","").replace("'C\n",""))
    
def fanScheduler():
    try:
        temp = int(round(getCPUtemperature()))
        print  time.strftime( ISOTIMEFORMAT)+" CPU temp:" + str(temp) 
        if temp >= StartFanTemp :
            FanController.startFan()
            print "Start fan."
        elif temp <= StopFanTemp :
            FanController.stopFan()
            print "Stop fan."
    except:
        traceback.print_exc()
        
if __name__ == "__main__":
    fanScheduler()
