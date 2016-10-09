#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys
#from grafix import *

#gpio's :
SCLK = 32
DIN = 22
DC = 18
RST = 16
CE = 7

font =[
    0x7E, 0x11, 0x11, 0x11, 0x7E, # A
    0x7F, 0x49, 0x49, 0x49, 0x36, # B
    0x3E, 0x41, 0x41, 0x41, 0x22, # C
    0x7F, 0x41, 0x41, 0x22, 0x1C, # D
    0x7F, 0x49, 0x49, 0x49, 0x41, # E
    0x7F, 0x09, 0x09, 0x09, 0x01, # F
    0x3E, 0x41, 0x49, 0x49, 0x7A, # G
    0x7F, 0x08, 0x08, 0x08, 0x7F, # H
    0x00, 0x41, 0x7F, 0x41, 0x00, # I
    0x20, 0x40, 0x41, 0x3F, 0x01, # J
    0x7F, 0x08, 0x14, 0x22, 0x41, # K
    0x7F, 0x40, 0x40, 0x40, 0x40, # L
    0x7F, 0x02, 0x0C, 0x02, 0x7F, # M
    0x7F, 0x04, 0x08, 0x10, 0x7F, # N
    0x3E, 0x41, 0x41, 0x41, 0x3E, # O
    0x7F, 0x09, 0x09, 0x09, 0x06, # P
    0x3E, 0x41, 0x51, 0x21, 0x5E, # Q
    0x7F, 0x09, 0x19, 0x29, 0x46, # R
    0x46, 0x49, 0x49, 0x49, 0x31, # S
    0x01, 0x01, 0x7F, 0x01, 0x01, # T
    0x3F, 0x40, 0x40, 0x40, 0x3F, # U
    0x1F, 0x20, 0x40, 0x20, 0x1F, # V
    0x3F, 0x40, 0x38, 0x40, 0x3F, # W
    0x63, 0x14, 0x08, 0x14, 0x63, # X
    0x07, 0x08, 0x70, 0x08, 0x07, # Y
    0x61, 0x51, 0x49, 0x45, 0x43, # Z
] # yapf: disable

def main():
    begin(0xbc) # contrast - may need tweaking for each display
    gotoxy(0, 0)
   # text(sys.argv[1])
    text("I LOVE U")
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
    index=(ord(char)-65)*5
    if ord(char) >=65 and ord(char) <=90:
        for i in range(5):
            #print (index+i)
            lcd_data(font[index+i])
        lcd_data(0) # space inbetween characters
    elif ord(char)==32:
        for i in xrange(5):
            lcd_data(0)
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

    GPIO.output(CE, True)
    time.sleep(0.5)
    GPIO.output(CE, False)
    time.sleep(0.5)

    lcd_cmd(0x21) # extend mode
    lcd_cmd(0x12) # bias 1:65
    lcd_cmd(0xc8) # vop

    lcd_cmd(0x20) # basic mode
    lcd_cmd(0x0c) # nomal mode display D = 1, E = 0
    
    cls()


def SPI(c):
    # data = DIN
    # clock = SCLK
    # MSB first
    # value = c
    for i in xrange(8):
        GPIO.output(DIN, (c & (1 << (7-i))) > 0)
       # GPIO.output(SCLK, True)
        GPIO.output(SCLK, False)
        GPIO.output(SCLK, True)

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
