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
spinSpeed = 95
forwardSpeed = 32

# time variables
spinTime = 0.009
forwardTime = 0.0005

# stop variables
sideStop = 21
frontStop = 100

# start recording
ts = str(time())
cam.vflip = True
cam.hflip = True
cam.start_recording("/home/pi/qmpiwars/videos/straight-" + ts + ".h264")

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
        pz.forward(forwardSpeed)
        sleep(forwardTime)
        sideDist.neoPixelLight("forward")
        if(distance <= frontStop): # too close - STOP!
            print "Stop!"
            #pz.stop()
            sideDist.neoPixelLight("off")
        elif(LeftDist <= sideStop): # heading left - turn right
           print "turning right"
           pz.spinLeft(spinSpeed)
           sleep(spinTime)
           sideDist.neoPixelLight("right")
           pz.forward(forwardSpeed)
           sleep(forwardTime)
           sideDist.neoPixelLight("forward")
           if(LeftDist < sideStop): # still too close move forward a bit more
               pz.forward(forwardSpeed)
               sleep(spinTime)
               sideDist.neoPixelLight("forward")
        elif(RightDist <= sideStop): # heading right - turn left
           print "turning left"
           pz.spinRight(spinSpeed)
           sleep(spinTime)
           sideDist.neoPixelLight("left")
           pz.forward(forwardSpeed)
           sleep(forwardTime)
           sideDist.neoPixelLight("forward")
           if(RightDist < sideStop): # still too close move forward a bit
               pz.forward(forwardSpeed)
               sleep(spinTime)
               sideDist.neoPixelLight("forward")
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
    stop_recording()
