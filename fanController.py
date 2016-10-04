#!/bin/python
import RPi.GPIO as GPIO
import time
import traceback

FanPowerPin = 12 # use pin 12 to give fan power
FanGNDPin = 14   # use pin 14 as ground 

# run 15min and sleep 5 min
FanSleepTime = 10 * 60
FanRunTime = 60 * 60

# init the GPIO
def init():
    #print "PP is:" + str(FanPowerPin)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(FanPowerPin, GPIO.OUT)


def fanControl():
    try:
        while True:
            #print "running on" + str(FanPowerPin)
            GPIO.output(FanPowerPin, GPIO.HIGH)
            time.sleep(FanRunTime)
            #print "stop"
            GPIO.output(FanPowerPin, GPIO.LOW)
            time.sleep(FanSleepTime)
    except:
        GPIO.cleanup(FanPowerPin)
        traceback.print_exc()
    
def main():
#    print "welcome to fan contoller"
    init()
    fanControl()

if __name__ == "__main__": 
    main()
