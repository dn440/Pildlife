from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
camera.exposure_mode = 'night'
sleep(10)
camera.stop_preview()

