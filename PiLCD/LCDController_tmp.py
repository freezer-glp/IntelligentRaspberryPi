#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import Font

# gpio's :
SCLK = 32
DIN = 22
DC = 18
RST = 16
CE = 7

SPACE_WIDTH = 3
WRITE_DATA = True
WRITE_CMD = False


def main():
    initLCD()
    # text(sys.argv[1])
    displayText("I Love U", 28, 0)


def gotoxy(x, y):
    """
    Set the cursor to (x,y)
    :param x: 0 <= x <= 83
    :param y: 0 <= y <= 5
    :return:
    """
    if 0 <= x <= 83 and 0 <= y <= 5:
        writeByte(x + 128, WRITE_CMD)
        writeByte(y + 64, WRITE_CMD)
    else:
        print "Error (x,y):" + str(x) + str(y)


def displayText(words, x=-1, y=-1):
    """
    Display words(string) on LCD5110 [start at (x, y) ]
    :param words: the words noly contain ASCII chars
    :return: None
    """
    if x != -1 and y != -1:
        gotoxy(x, y)
    for i in range(len(words)):
        print "words[" + str(i) + "]:" + words[i]
        displayChar(words[i])


def displayChar(char):
    """
    Display a char on LCD5110
    :param char:
    :return: None
    """
    index = (ord(char) - 32) * 6
    if ord(char) > 32 and ord(char) <= 122:
        for i in range(6):
            writeByte(Font.font[index + i], WRITE_DATA)
    elif ord(char) == 32:
        for i in xrange(SPACE_WIDTH):
            writeByte(0x00, WRITE_DATA)


def clearScreen():
    gotoxy(0, 0)
    for i in range(84):
        for j in range(6):
            writeByte(0x00, WRITE_DATA)


def setup():
    """
    Set GPIO mode and pin direct
    :return:
    """
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(DIN, GPIO.OUT)
    GPIO.setup(SCLK, GPIO.OUT)
    GPIO.setup(DC, GPIO.OUT)
    GPIO.setup(RST, GPIO.OUT)
    GPIO.setup(CE, GPIO.OUT)


def initLCD():
    """
    Initialize the LCD5110
    :return:
    """

    setup()

    # toggle RST low to reset
    GPIO.output(RST, False)
    time.sleep(0.500)
    GPIO.output(RST, True)
    time.sleep(0.5)

    writeByte(0x21, WRITE_CMD)  # extend mode
    writeByte(0x13, WRITE_CMD)  # bias 1:65
    writeByte(0xc4, WRITE_CMD)  # vop

    writeByte(0x20, WRITE_CMD)  # basic mode
    writeByte(0x0c, WRITE_CMD)  # nomal mode display D = 1, E = 0

    clearScreen()


def SPI(c):
    """
    Write byte to LCD and each clock a bit
    :param c: the byte
    :return: None
    """
    GPIO.output(CE, False)
    for i in xrange(8):
        GPIO.output(DIN, (c & (1 << (7 - i))) > 0)
        GPIO.output(SCLK, False)
        GPIO.output(SCLK, True)
    GPIO.output(CE, True)


def writeByte(c, type):
    """
    Write a Byte to LCD5110
    :param c: the byte
    :param type: an int value and 1 means data output while 0 means command output
    :return: None
    """
    GPIO.output(DC, type)
    SPI(c)


if __name__ == "__main__":
    main()
