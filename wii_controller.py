# Wii controller remote control script

import RPi.GPIO as GPIO # Import the GPIO Library
import time # Import the Time library
import os

# import PiConZero stuff
import piconzero as pz
import sensorlibs as sl

# Set the GPIO modes
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Credit for this part must go to:
# Author : Matt Hawkins (adapted by Michael Horne)
# http://www.raspberrypi-spy.co.uk/?p=1101
# -----------------------
# Import required Python libraries
# -----------------------
import cwiid

PIN_LED = sl.GPIOtoBoard(4)
GPIO.setup(PIN_LED, GPIO.OUT)
GPIO.output(PIN_LED, 0)

button_delay = 0.1

print 'Press 1 + 2 on your Wii Remote now ...'
GPIO.output(PIN_LED, 1)
time.sleep(1)

# Connect to the Wii Remote. If it times out
# then quit.
try:
    wii=cwiid.Wiimote()
    GPIO.output(PIN_LED, 0)

except RuntimeError:
    print "Error opening wiimote connection"
    GPIO.output(PIN_LED, 0)
    # Uncomment this line to shutdown the Pi if pairing fails
    #os.system("sudo halt")
    quit()

print 'Wii Remote connected...\n'
print 'Press some buttons!\n'
print 'Press PLUS and MINUS together to disconnect and quit.\n'

for x in range(0,3):
    GPIO.output(PIN_LED, 1)
    time.sleep(0.25)
    GPIO.output(PIN_LED, 0)
    time.sleep(0.25)

wii.rpt_mode = cwiid.RPT_BTN

pz.init()

while True:

    buttons = wii.state['buttons']

    # If Plus and Minus buttons pressed
    # together then rumble and quit.
    if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):  
        print '\nClosing connection ...'
        wii.rumble = 1
        GPIO.output(PIN_LED, 1)
        time.sleep(1)
        wii.rumble = 0
        GPIO.output(PIN_LED, 0)
        #os.system("sudo halt")
        exit(wii)
        pz.cleanup()
  
    # Check if other buttons are pressed by
    # doing a bitwise AND of the buttons number
    # and the predefined constant for that button.
    if (buttons & cwiid.BTN_LEFT):
        print 'Left pressed'
        pz.spinLeft(100)
        time.sleep(button_delay)         

    elif(buttons & cwiid.BTN_RIGHT):
        print 'Right pressed'
        pz.spinRight(100)
        time.sleep(button_delay)          

    elif (buttons & cwiid.BTN_UP):
        print 'Up pressed' 
        pz.forward(100)
        time.sleep(button_delay)          
    
    elif (buttons & cwiid.BTN_DOWN):
        print 'Down pressed'      
        pz.reverse(100)
        time.sleep(button_delay)  
    elif (buttons & cwiid.BTN_A):
        print 'Button A pressed'
        pz.stop()
        time.sleep(button_delay)
    
    else:
        pz.cleanup()
