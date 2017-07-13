import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pinTrigger = 27 # 27 for left 17 for right
pinEcho = 22 # 22 for left 18 for right

print("Measuring")

GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)

try:
   while True:
      GPIO.output(pinTrigger, False)
      time.sleep(0.5)
      GPIO.output(pinTrigger, True)
      time.sleep(0.00001)
      GPIO.output(pinTrigger, False)

      StartTime = time.time()

      while GPIO.input(pinEcho)==0:
         StartTime = time.time()

      while GPIO.input(pinEcho)==1:
         StopTime = time.time()
         #if StopTime-StartTime >= 0.0004:
            #print("too close to see!")
            #StopTime = StartTime
            #break

      ElapsedTime = StopTime - StartTime
      Distance = ElapsedTime * 34326
      Distance = Distance / 2

      print("Distance : %.4f" % Distance)

      time.sleep(0.5)

except KeyboardInterrupt:
   GPIO.cleanup()
