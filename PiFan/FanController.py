#!/usr/bin/python
import sys
import RPi.GPIO as GPIO
import time
import traceback

FanPowerPin = 12 # use pin 12 to give fan power

# run 60min and sleep 10 min
FanSleepTime = 10 * 60
FanRunTime = 60 * 60

def usage():
    print "Usage: python fanController.py [start|stop]"

# init the GPIO
def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(FanPowerPin, GPIO.OUT)

def startFan():
    try:
        init()
        GPIO.output(FanPowerPin, GPIO.HIGH)
    except:
        GPIO.cleanup(FanPowerPin)
        traceback.print_exc()

def stopFan():
    try:
        init()
        GPIO.output(FanPowerPin, GPIO.LOW)
    except:
        GPIO.cleanup(FanPowerPin)
        traceback.print_exc()
        
def defaultRun():
    try:
        while True:
            startFan()
            time.sleep(FanRunTime)
            stopFan()
            time.sleep(FanSleepTime)
    except:
        GPIO.cleanup(FanPowerPin)
        traceback.print_exc()
    
def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == "start":
            startFan()
        elif sys.argv[1] == "stop":
            stopFan() 
    elif len(sys.argv) == 1: 
        defaultRun() 
    else: 
        usage() 
       
if __name__ == "__main__": 
    main()
