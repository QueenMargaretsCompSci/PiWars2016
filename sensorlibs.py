import RPi.GPIO as GPIO
import time
import piconzero as pz

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

def neoPixelLight(direction):
   # setup neopixel output
   pz.setOutputConfig(5, 3)
   if direction == "forward":
      pz.setAllPixels(255,0,0)
   elif direction == "backward":
      pz.setAllPixels(255,255,0)
   elif direction == "left":
      pz.setAllPixels(127,127,255)
   elif direction == "right":
      pz.setAllPixels(255,255,255)
   elif direction == "off":
      pz.setAllPixels(0,0,0)

def GPIOtoBoard(GPIOpin):
   # pins available = 4, 17, 18, 27, 22
   # set Boardpin to False incase we get an incorrect GPIO pin
   Boardpin = False
   if GPIOpin == 4:
      Boardpin = 7
   elif GPIOpin == 17:
      Boardpin = 11
   elif GPIOpin == 18:
      Boardpin = 12
   elif GPIOpin == 27:
      Boardpin = 13
   elif GPIOpin == 22:
      Boardpin = 15
   return Boardpin

def DistSensor(pinTriggerGPIO, pinEchoGPIO):
   # convert our GPIO pins to Board numbering
   pinTrigger = GPIOtoBoard(pinTriggerGPIO)
   pinEcho = GPIOtoBoard(pinEchoGPIO)

   # set up our pins
   GPIO.setup(pinTrigger, GPIO.OUT)
   GPIO.setup(pinEcho, GPIO.IN)

   # Set trigger pin to low
   GPIO.output(pinTrigger, False)
   # allow module to settle
   time.sleep(0.05)
   # send 10us pulse to trigger
   GPIO.output(pinTrigger, True)
   time.sleep(0.00001)
   GPIO.output(pinTrigger, False)

   # start the timer
   StartTime = time.time()
   # reset the time until the echo pin goes high
   while GPIO.input(pinEcho)==0:
      StartTime = time.time()
   # stop when the echo pin is no longer high
   while GPIO.input(pinEcho)==1:
      StopTime = time.time()

   # calculate our times
   ElapsedTime = StopTime - StartTime
   Distance = ElapsedTime * 34326 # speed of sound cm/s
   Distance = Distance / 2 # half it - there and back
   Distance = round(Distance, 0)

   # return distance
   return Distance

def cleanup():
   GPIO.cleanup()

############################################
#
# For example this loop would return the 
# value sfor left and right sensors if they
# were connected to the stated GPIO Pins

#while True:
#   LeftDist = DistSensor(27, 22) #Left
#   RightDist = DistSensor(17, 18) #Right
#   print("Left Dist : %.4f" % LeftDist)
#   print("Right Dist : %.4f" % RightDist)
#   time.sleep(1)
