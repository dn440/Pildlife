from picamera import PiCamera
import RPi.GPIO as GPIO
import time
from datetime import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
# this pin will control the IR-CUT filter (low = filter off)
GPIO.setup(16, GPIO.OUT)
# this pin controls the MOSFET gating power to IR LEDs
GPIO.setup(7, GPIO.OUT)

camera = PiCamera()
camera.resolution = (2592, 1944)
camera.framerate = 15
camera.exposure_mode = 'night'

while True:
    GPIO.output(16, 0) # toggle IR filter
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    camera.annotate_text = str(now)
    i=GPIO.input(11)
    if i==0:                 #When output from motion sensor is LOW
        print "No intruders",i
        GPIO.output(7, 0) # turn off LEDs
        time.sleep(0.1)
    elif i==1:               #When output from motion sensor is HIGH
        print "Intruder detected",i
        GPIO.output(7, 1) # turn on LEDs
        time.sleep(5)
        camera.capture('/home/pi/Pictures/' + str(now) + '.jpg')
        time.sleep(0.1)
