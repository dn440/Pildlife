import shutil
import signal                   
import sys
import os
import time
from datetime import datetime
from datetime import time as t 
from picamera import PiCamera
import RPi.GPIO as GPIO

# set up GPIO
GPIO.setwarnings(False)
# set mode to position numbering
GPIO.setmode(GPIO.BOARD)
GPIO_filter = 33
GPIO_PIR = 18
GPIO_MOSFET = 16
GPIO_switch = 37

# variable definitions
dest = "/mnt/logger/pictures/"
# set up camera
camera = PiCamera()
camera.resolution = (2592, 1944)
camera.framerate = 15
camera.exposure_mode = 'night'

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def sensor_callback(channel):
    if GPIO.input(GPIO_PIR):
        print("motion detected!")
        GPIO.output(GPIO_MOSFET, 1) # turn on LEDs
        time.sleep(0.2)
        # define image name by using time
        now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        camera.annotate_text = str(now)
        camera.capture(dest + str(now) + '.jpg') # take image
        time.sleep(2)
    else:
        print("no motion")
        GPIO.output(GPIO_MOSFET, 0) # turn off LEDs
        time.sleep(0.1)

def shutdown(channel):
    print("Shutting Down")
    time.sleep(5)
    os.system("sudo shutdown -h now")

if __name__ == '__main__':
    # pull down PIR motion sensor
    GPIO.setup(GPIO_PIR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # this pin will control the IR-CUT filter (low = 0 = filter off)
    GPIO.setup(GPIO_filter, GPIO.OUT)
    if is_time_between(t(22,0), t(06,31)):
        GPIO.output(GPIO_filter, 0) # toggle IR filter off
    else:
        GPIO.output(GPIO_filter, 0) # toggle IR filter off

    # this pin controls the MOSFET gating power to IR LEDs
    GPIO.setup(GPIO_MOSFET, GPIO.OUT)
    GPIO.add_event_detect(GPIO_PIR, GPIO.BOTH, callback=sensor_callback, bouncetime=100)

    # this pin responds to a switch to shut down the pi
    GPIO.setup(GPIO_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(GPIO_switch, GPIO.FALLING, callback=shutdown, bouncetime=2000)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()

GPIO.cleanup()
