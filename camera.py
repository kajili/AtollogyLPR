#!/usr/bin/env python

from picamera import PiCamera
from time import sleep
import sys

camera = PiCamera()
camera.start_preview()
sleep(5)
file_name = sys.argv[1] 
camera.capture(file_name)
camera.stop_preview()



