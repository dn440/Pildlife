from picamera import PiCamera
import RPi.GPIO as GPIO
import time
from datetime import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor

camera = PiCamera()
camera.resolution = (2592, 1944)
camera.framerate = 15

while True:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    camera.annotate_text = str(now)
    i=GPIO.input(11)
    if i==0:                 #When output from motion sensor is LOW
        print "No intruders",i
        time.sleep(0.1)
    elif i==1:               #When output from motion sensor is HIGH
        print "Intruder detected",i
        time.sleep(5)
        camera.capture('/home/pi/Pictures/' + str(now) + '.jpg')
        time.sleep(0.1)
