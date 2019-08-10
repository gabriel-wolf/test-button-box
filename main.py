# Trinket IO demo
# Welcome to CircuitPython 3.1.1 :)

import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogOut, AnalogIn
import touchio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
import adafruit_dotstar as dotstar
import time
import neopixel

# colors
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
PURPLE = (255,0,255)
CYAN = (0,255,255)

# One pixel connected internally!
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Analog input on D0
analog1in = AnalogIn(board.D0)

# Analog output on D1
aout = AnalogOut(board.D1)

# Digital input with pullup on D2
button = DigitalInOut(board.D2)
button.direction = Direction.INPUT
button.pull = Pull.UP

# Capacitive touch on D3
touch = touchio.TouchIn(board.D3)

# NeoPixel strip (of 16 LEDs) connected on D4
NUMPIXELS = 16
neopixels = neopixel.NeoPixel(board.D4, NUMPIXELS, brightness=0.2, auto_write=False)

# Used if we do HID output, see below
kbd = Keyboard()

######################### HELPERS ##############################

# Helper to convert analog input to voltage
def getVoltage(pin):
    return (pin.value * 3.3) / 65536

# Helper to give us a nice color swirl
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0):
        return (0, 0, 0)
    if (pos > 255):
        return (0, 0, 0)
    if (pos < 85):
        return (int(pos * 3), int(255 - (pos*3)), 0)
    elif (pos < 170):
        pos -= 85
        return (int(255 - pos*3), 0, int(pos*3))
    else:
        pos -= 170
        return (0, int(pos*3), int(255 - pos*3))

# def alarmColor(pos):
#    if (pos < 0 or pos > 255)

def setLEDColor(color, npixels, numpixels=16):
    for p in range(numpixels):
        npixels[p] = color
    npixels.show()

######################### MAIN LOOP ##############################

def wintab(kbd):
    kbd.send(Keycode.TAB,Keycode.WINDOWS)

def cad(kbd):
    kbd.send(Keycode.CONTROL,Keycode.ALT,Keycode.DELETE)

def addtrello(kbd):
    kbd.send(Keycode.CONTROL,Keycode.ALT,Keycode.SPACEBAR)

def taskmanager(kbd):
    kbd.send(Keycode.CONTROL,Keycode.SHIFT,Keycode.ESCAPE)

def f5(kbd):
    kbd.send(Keycode.f5)
    
def cortana(kbd):
    kbd.send(Keycode.WINDOWS,Keycode.C)

def wox(kbd):
    kbd.send(Keycode.CONTROL,Keycode.SPACEBAR)

def cmatrix(kbd):
    None
    # os.system('bash -c "cmatrix"')

def gamebar(kbd):
    kbd.send(Keycode.WINDOWS,Keycode.G)


i = 0
layout = KeyboardLayoutUS(kbd)
while True:    

    # setLEDColor(RED,neopixels,16)
 
    # set analog output to 0-3.3V (0-65535 in increments)
    aout.value = i * 256

    # Read analog voltage on D0
    print("D0: %0.2f" % getVoltage(analog1in))

    # use D3 as capacitive touch to turn on internal LED
    if touch.value:
        print("D3 touched!")
    led.value = touch.value
    if not button.value:
        print("Button on D2 pressed!")
        
        longpress = False
        kbd.release_all()
        
        while not button.value:
            time.sleep(0.2)
            for i in range(120):
                time.sleep(0.008)
                if button.value:
                    # if quick press
                    break
                   
                else:
                    # if not quick press
                    longpress = True
                    break
        
        while(not button.value):
            # this is executed after the button has been held down for the first execution
            longpress = True
            pass
        if longpress == True:
            # laong press execution
            # cad(kbd)
            gamebar(kbd)
        else:
            # short press execution
            addtrello(kbd)
        # this is executed once when the button is let go of


            

    i = (i+1) % 256  # run from 0 to 255
    #time.sleep(0.01) # make bigger to slow down
