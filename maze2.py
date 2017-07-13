import piconzero as pz
import hcsr04 as dist
import sensorlibs as sideDist
from time import sleep, time

pz.init()
dist.init()

# speed variables
spinSpeed = 60
forwardSpeed = 12
reverseSpeed = 40

# time variables
spinTime = 0.05
forwardTime = 0.05
reverseTime = 0.05

# distance variables
leftMax = 12
frontStop = 25
rightMax = 12

# last known dist
lastFront = 0
lastLeft = 0
lastRight = 0

# start camera
# picamera start recording now...

try:
    lastFront = int(dist.getDistance())
    while lastFront > frontStop: # go forward to the first wall
        print "head to first wall"
        pz.forward(forwardSpeed)
        sleep(forwardTime)
        lastFront = int(dist.getDistance())
        print str(lastFront)

    pz.stop()

    leftTurn = True
    # measure rhs dist
    currentRight = sideDist.DistSensor(17, 18)
    # assume this to be largest and smallest reading
    largeRight = currentRight
    smallRight = currentRight

    while leftTurn:
        pz.spinRight(spinSpeed)
        sleep(spinTime)
        pz.stop()
        currentRight = sideDist.DistSensor(17, 18)
        if currentRight > largeRight:
            print "larger"
            largeRight = currentRight
        elif currentRight < largeRight:
            print "smaller"
            smallRight = currentRight
        elif currentRight > smallRight:
            leftTurn = False
        
    
    # execute first left
    # take right dist
    #currentRight = sideDist.DistSensor(17, 18)
    #sleep(0.5)
    #currentFront = int(dist.getDistance())
    #print "Cur Right " + str(currentRight) + " Cur Front " + str(currentFront)
    #while currentRight > lastRight:
        # turn left
        #pz.spinRight(spinSpeed)
        #sleep(spinTime)
        #pz.stop()
        #currentRight = sideDist.DistSensor(17, 18)
        #print str(currentRight)
        #sleep(0.5)
        
    lastFront = int(dist.getDistance())
    print "start forward loop.  last = " + str(lastFront) + " stop = " + str(frontStop)
    lastRight = sideDist.DistSensor(17, 18)
    sleep(1)
    lastLeft = sideDist.DistSensor(27, 22)
    sleep(1)

    while lastFront > frontStop: # we have turned left, so drive forwards a bit
        print "Front " + str(lastFront)
        print "Right " + str(lastRight)
        print "Left " + str(lastLeft)

        if lastRight < rightMax: # too close to rhs wall, turn
            print "turn left"
            pz.spinRight(spinSpeed)
            sleep(spinTime)
            lastRight = sideDist.DistSensor(17, 18)
        elif lastLeft < leftMax: # too close to lhs wall, turn
            print "turn right"
            pz.spinLeft(spinSpeed)
            sleep(spinTime)
            lastLeft = sideDist.DistSensor(27, 22)
        else:
            print "drive forwards a bit"
            pz.forward(forwardSpeed)
            sleep(forwardTime)
        lastFront = int(dist.getDistance())
        sleep(1)
        lastRight = sideDist.DistSensor(17, 18)
        sleep(1)
        lastLeft = sideDist.DistSensor(27, 22)
        sleep(1)
        print "Front " + str(lastFront)
        print "Right " + str(lastRight)
        print "Left " + str(lastLeft)
    
    #while lastFront > frontStop: # go forward to second wall
    #    print "head to second wall"
    #    lastRight = sideDist.DistSensor(17, 18)
    #    lastLeft = sideDist.DistSensor(27, 22)
    #    if lastRight < rightMax: # turn left away from right wall
    #        print "turning left"
    #        print "lastRight: " + str(lastRight)
    #        pz.spinRight(spinSpeed)
    #        sleep(spinTime)
    #    elif lastLeft < leftMax: # turn right away from left wall
    #        print "turning right"
    #        print "lastLeft: " + str(lastLeft)
    #        pz.spinLeft(spinSpeed)
    #        sleep(spinTime)
    #    pz.forward(forwardSpeed)
    #    lastFront = int(dist.getDistance())
    #    print str(lastFront)
    #    sleep(forwardTime) 
    pz.stop() # stop the motors
except KeyboardInterrupt:
    print "cleaning up and exiting"
finally:
    dist.cleanup()
    pz.cleanup()
    sideDist.cleanup()
