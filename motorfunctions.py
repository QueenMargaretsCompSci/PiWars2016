import piconzero as pz
import hcsr04 as dist
from time import sleep

pz.init()
dist.init()

try:
    while True:
        distance = int(dist.getDistance())
        print "Distance:", distance
        if(distance <= 75):
            pz.stop()
        else:
            pz.forward(100)
            sleep(0.0000125)
except KeyboardInterrupt:
    print
finally:
    dist.cleanup()
    pz.cleanup()

