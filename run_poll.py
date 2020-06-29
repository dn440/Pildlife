from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import shutil
from datetime import datetime

# set up GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # set mode to position numbering
# Read output from PIR motion sensor
GPIO.setup(18, GPIO.IN)
# this pin will control the IR-CUT filter (low = filter off)
GPIO.setup(33, GPIO.OUT)
# this pin controls the MOSFET gating power to IR LEDs
GPIO.setup(16, GPIO.OUT)

# variable definitions
dest = "/mnt/logger/pictures/"
# set up camera
camera = PiCamera()
camera.resolution = (2592, 1944)
camera.framerate = 15
camera.exposure_mode = 'night'

try:
    while True:
        GPIO.output(33, 0) # toggle IR filter
        now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        camera.annotate_text = str(now)
        i=GPIO.input(18)
        if i==0:                 #When output from motion sensor is LOW
            print "No intruders",i
            GPIO.output(16, 0) # turn off LEDs
            time.sleep(0.1)
        elif i==1:               #When output from motion sensor is HIGH
            print "Intruder detected",i
            GPIO.output(16, 1) # turn on LEDs
            time.sleep(5)
            # define image name by using time
            source = '/home/pi/Pictures/' + str(now) + '.jpg'
            # take image
            camera.capture(source)
            # move image to SD card
            shutil.move(source, dest)
            time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup()
