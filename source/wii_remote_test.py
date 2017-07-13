#!/usr/bin/python

# import our modules
import cwiid
import time
import RPi.GPIO as GPIO
import piconzero as pz
import sensorlibs as sl
from picamera import PiCamera

# setup our camera
cam = PiCamera()

# setup our constants
button_delay = 0.1
PIN_LED = sl.GPIOtoBoard(4)
GPIO.setup(PIN_LED, GPIO.OUT)
GPIO.output(PIN_LED, 0)

# prompt for Wii connection
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
  quit()

print 'Wii Remote connected...\n'
print 'Press some buttons!\n'
print 'Press PLUS and MINUS together to disconnect and quit.\n'

# connected so lets flash our LED
for x in range(0,3):
    GPIO.output(PIN_LED, 1)
    time.sleep(0.25)
    GPIO.output(PIN_LED, 0)
    time.sleep(0.25)

wii.rpt_mode = cwiid.RPT_BTN

# initialise piconzero
pz.init()

# start recording
ts = str(time.time())
cam.vflip = True
cam.hflip = True
cam.start_recording("/home/pi/qmpiwars/videos/remote-" + ts + ".h264")

while True:

  buttons = wii.state['buttons']

  # If Plus and Minus buttons pressed
  # together then rumble and quit.
  if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):  
    print '\nClosing connection ...'
    wii.rumble = 1
    time.sleep(1)
    wii.rumble = 0
    sl.neoPixelLight("off")
    pz.cleanup()
    cam.stop_recording()
    exit(wii)
  
  # Check if other buttons are pressed by
  # doing a bitwise AND of the buttons number
  # and the predefined constant for that button.
  if (buttons & cwiid.BTN_LEFT):
    print 'Left pressed'
    pz.spinRight(100)
    time.sleep(button_delay)         
    sl.neoPixelLight("left")

  if(buttons & cwiid.BTN_RIGHT):
    print 'Right pressed'
    pz.spinLeft(100)
    time.sleep(button_delay)          
    sl.neoPixelLight("right")

  if (buttons & cwiid.BTN_UP):
    print 'Up pressed'        
    pz.forward(80)
    time.sleep(button_delay)
    sl.neoPixelLight("forward")

  if (buttons & cwiid.BTN_B):
    print 'Turbo pressed'
    pz.forward(100)
    time.sleep(button_delay)
    sl.neoPixelLight("forward")          
    
  if (buttons & cwiid.BTN_DOWN):
    print 'Down pressed'      
    pz.reverse(80)
    time.sleep(button_delay) 
    sl.neoPixelLight("backward") 
    
  if (buttons & cwiid.BTN_1):
    print 'Button 1 pressed'
    time.sleep(button_delay)          

  if (buttons & cwiid.BTN_2):
    print 'Button 2 pressed'
    time.sleep(button_delay)          

  if (buttons & cwiid.BTN_A):
    print 'Button A pressed'
    pz.stop()
    sl.neoPixelLight("off")
    time.sleep(button_delay)          

##########################################
# Not using these buttons
#
#  if (buttons & cwiid.BTN_B):
#    print 'Button B pressed'
#    time.sleep(button_delay)          
#
#  if (buttons & cwiid.BTN_HOME):
#    print 'Home Button pressed'
#    time.sleep(button_delay)           
#    
#  if (buttons & cwiid.BTN_MINUS):
#    print 'Minus Button pressed'
#    time.sleep(button_delay)   
#    
#  if (buttons & cwiid.BTN_PLUS):
#    print 'Plus Button pressed'
#    time.sleep(button_delay)

