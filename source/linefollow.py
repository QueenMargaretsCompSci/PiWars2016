import piconzero as pz
from time import sleep, time
import RPi.GPIO as GPIO
import sensorlibs as sl
from picamera import PiCamera

# setup our camera
cam = PiCamera()

# set the variables for the line followers
lineLeft = sl.GPIOtoBoard(27)
lineCentre = sl.GPIOtoBoard(18)
lineRight = sl.GPIOtoBoard(17)

# setup our followers as inputs
GPIO.setup(lineLeft, GPIO.IN)
GPIO.setup(lineCentre, GPIO.IN)
GPIO.setup(lineRight, GPIO.IN)

# initialise the piconzero
pz.init()

# speed constants
FORWARD = 10
TURN = 60
STURN = 60

# time constants
fTime = 0.01
sTime = 0.01

# Search for the black line
def SeekLine(SeekSpeed, SeekSize):
    print("Seeking the line")
    # The direction the robot will turn - True = Left
    Direction = True

    #SeekSize = 0.25 # Turn for 0.25s
    SeekCount = 1 # A count of times the robot has looked for the line
    MaxSeekCount = 3 # The maximum time to seek the line in one direction

    # Turn the robot left and right until it finds the line
    # Or it has been searched for long enough
    while SeekCount <= MaxSeekCount:
        # Set the seek time
        SeekTime = SeekSize * SeekCount

        # Start the motors turning in a direction
        if Direction:
            print("Seeking - Looking left")
            pz.spinRight(SeekSpeed)
            sl.neoPixelLight("left")
            sleep(SeekSize/50)
        else:
            print("Seeking - Looking Right")
            pz.spinLeft(SeekSpeed)
            sl.neoPixelLight("right")
            sleep(SeekSize/50)

        # Save the time it is now
        StartTime = time()

        # While the robot is turning for SeekTime seconds,
        # check to see whether the line detector is over black
        while time()-StartTime <= SeekTime:
            if GPIO.input(lineCentre)==1:
                pz.stop()
                # Exit the SeekLine() function returning
                # True - the line was found
                return True

        # The robot has not found the black line yet, so stop
        pz.stop()
        sl.neoPixelLight("off")

        # Increase the seek count
        SeekCount += 1

        # Change direction
        Direction = not Direction
    # The line wasn't found, so return False
    return False

# start recording
ts = str(time())
cam.vflip = True
cam.hflip = True
cam.start_recording("/home/pi/qmpiwars/videos/line-" + ts + ".h264")

try:
    while True:
        if GPIO.input(lineRight)==1:
            print("Line Right is seeing black. Turn Right")
            pz.spinLeft(TURN)
            sl.neoPixelLight("right")
            sleep(sTime)
        elif GPIO.input(lineLeft)==1:
            print("Line Left is seeing black. Turn Left")
            pz.spinRight(TURN)
            sl.neoPixelLight("left")
            sleep(sTime)
        elif GPIO.input(lineCentre)==1:
            print("Line Centre is seeing black. Drive Forwards")
            pz.forward(FORWARD)
            sl.neoPixelLight("forward")
            sleep(fTime)
        else:
            print("Everything is seeing white. Seak left and right")
            SeekLine(STURN, sTime)
except KeyboardInterrupt:
    GPIO.cleanup()
    sl.neoPixelLight("off")
    pz.cleanup()
    cam.stop_recording()

