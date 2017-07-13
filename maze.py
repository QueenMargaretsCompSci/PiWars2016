import piconzero as pz
import hcsr04 as dist
import sensorlibs as sideDist
from time import sleep, time
from picamera import PiCamera

# setup our camera
cam = PiCamera()

pz.init()
dist.init()

# speed variables
spinSpeed = 100
forwardSpeed = 12
reverseSpeed = 12

# time variables
spinTime = 0.01
forwardTime = 0.0005
reverseTime = 0.0008

# distance variables
leftMax = 13
frontStop = 15
rightMax = 40

# start recording
ts = str(time())
cam.vflip = True
cam.hflip = True
cam.start_recording("/home/pi/qmpiwars/videos/maze-" + ts + ".h264")

try:
    while True:
        distance = int(dist.getDistance())
        LeftDist = sideDist.DistSensor(27, 22) #Left
        RightDist = sideDist.DistSensor(17, 18) #Right
        print "----------------------------------"
        print "Front Distance:", distance
        print "Left Distance:", LeftDist
        print "Right Distance:", RightDist
        print "----------------------------------"
        if(distance <= frontStop): # too close - Reverse
           print "reverse"
           pz.reverse(reverseSpeed)
           sleep(reverseTime)
           sideDist.neoPixelLight("backward")
        elif(LeftDist >= leftMax): # heading right - turn left
           print "turning left"
           pz.spinRight(spinSpeed)
           sleep(spinTime)
           sideDist.neoPixelLight("left")
           if(LeftDist > leftMax): # still too far move forward a bit more
               pz.forward(forwardSpeed)
               sleep(forwardTime)
               sideDist.neoPixelLight("forward")
        elif(LeftDist < leftMax - 7): # turn right
           print "turning right"
           pz.spinLeft(spinSpeed)
           sleep(spinTime)
           sideDist.neoPixelLight("right")
        else:
           print "going forward"
           pz.forward(forwardSpeed)
           sleep(forwardTime)
           sideDist.neoPixelLight("forward")
except KeyboardInterrupt:
    print "cleaning up and exiting"
finally:
    dist.cleanup()
    sideDist.neoPixelLight("off")
    pz.cleanup()
    sideDist.cleanup()
    cam.stop_recording()
