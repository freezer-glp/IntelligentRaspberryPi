#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys
import Font
#from grafix import *

#gpio's :
SCLK = 32
DIN = 22
DC = 18
RST = 16
CE = 7

SPACEWIDTH = 3

def main():
    begin(0xbc) # contrast - may need tweaking for each display
    gotoxy(0, 0)
    #text(sys.argv[1])
    text("I Love U")
#    for i in xrange(85):
#        lcd_data(0xff)
    #lcd_data(0xff)
    #lcd_data(0xff)
#    text("HELLO")
#    gotoxy(8,2)
#    text("RASPBERRY PI")
#    gotoxy(6,4)
#    text("FORUM MEMBERS")

def gotoxy(x,y):
    lcd_cmd(x+128)
    lcd_cmd(y+64)

def text(words):
    for i in range(len(words)):
        print "words["+str(i) + "]:"+ words[i]
        display_char(words[i])

def display_char(char):
    index=(ord(char)-32)*6
    if ord(char) > 32 and ord(char) <= 122:
        for i in range(6):
            #print (index+i)
            lcd_data(Font.font[index+i])
        #lcd_data(0xff) # space inbetween characters
    elif ord(char) == 32:
        for i in xrange(SPACEWIDTH):
            lcd_data(0x00)

def cls():
    gotoxy(0,0)
    for i in range(84):
        for j in range(6):
            lcd_data(0)

def setup():
# set pin directions
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(DIN, GPIO.OUT)
    GPIO.setup(SCLK, GPIO.OUT)
    GPIO.setup(DC, GPIO.OUT)
    GPIO.setup(RST, GPIO.OUT)
    GPIO.setup(CE, GPIO.OUT)

def begin(contrast):
    setup()

    # toggle RST low to reset
    GPIO.output(RST, False)
    time.sleep(0.500)
    GPIO.output(RST, True)
    time.sleep(0.5)

    #GPIO.output(CE, True)
    #time.sleep(0.5)
    #GPIO.output(CE, False)
    #time.sleep(0.5)

    lcd_cmd(0x21) # extend mode
    lcd_cmd(0x13) # bias 1:65
    lcd_cmd(0xc4) # vop

    lcd_cmd(0x20) # basic mode
    lcd_cmd(0x0c) # nomal mode display D = 1, E = 0
    
    cls()


def SPI(c):
    # data = DIN
    # clock = SCLK
    # MSB first
    # value = c
    GPIO.output(CE, False)
    for i in xrange(8):
        GPIO.output(DIN, (c & (1 << (7-i))) > 0)
        GPIO.output(SCLK, False)
        GPIO.output(SCLK, True)
    GPIO.output(CE, True) 

def lcd_cmd(c):
    print "lcd_cmd sent :"+hex(c)
    GPIO.output(DC, False)
    SPI(c)

def lcd_data(c):
    print "data sent :"+hex(c)
    GPIO.output(DC, True)
    SPI(c)

if __name__ == "__main__":
    main()
