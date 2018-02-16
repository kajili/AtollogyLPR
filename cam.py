#!/usr/bin/env python

"""
Fle: cam.py
Author: Cesar Ner <ceneri@ucsc.edu>
Date: February 12, 2018

***********!!!
NOTE: To use this module, the following libraries must be installed:

	Python 3 Libraries:
		- OpenCv as well as Numpy: https://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/
		- Pysftp: Use pip3 install pysftp
		- Picamera: http://picamera.readthedocs.io/en/release-1.10/install3.html

	Linux Apps:
		- fswebcam: Use sudo apt-get
		- fbi: Use sudo apt-get
***********!!!

Cam.py enables to take pictures from Raspberry Pi camera module and Webcam simultaneously. (For Testing)
It then sends the pictures to specified server.

First argument: 
	0 - Take a picture with raspi camera
	1 - Take a picture with webcam
	2 - Take a picture with both
Second argument:
	- Picture file name 

OPTIONAL ARGUMENTS ONLY TO TRANSFER FILES:

Third argument:
	- IP address/server
Fourth argument:
	- Username

ALTERNATIVELY TO STOP MOTION, CALL:

	bash$ python cam.py stop

"""

import numpy as np
import cv2
import sys
import pysftp
import getpass
from picamera import PiCamera
from time import sleep
from subprocess import call
from datetime import datetime

CV2_WIDTH_ID = 3
CV2_HEIGHT_ID = 4

def stop_motion():
	call(["sudo", "service", "motion", "stop"])

def capture_web(filename):
    call(["fswebcam", "-d","/dev/video1", "-r", "3280x2464", "-S", "30", "--save", filename, "-v", "--no-banner"])

def preview_images(images):

	for image in images:
		call(["fbi", image])

def main():

	if len(sys.argv) == 2 and sys.argv[1] == "stop":
		stop_motion()
		print ("Motion Stopped")
		return
	
	#Get arguments
	cam_choice = int(sys.argv[1])
	filename = sys.argv[2]
	
	#Invalid input of camera choice
	if cam_choice < 0 or cam_choice > 2:
		quit()

	#Either take picture with pi module only, or with both
	if cam_choice != 1:

		filename_picv = filename + "_picv.jpg"

		capture = cv2.VideoCapture(0)
		capture.set(CV2_WIDTH_ID, 3280)
		capture.set(CV2_HEIGHT_ID, 2464)

		frame = capture.read()[1]
		cv2.imwrite(filename_picv, frame)
		capture.release()

		#Take a picture with PiCamera library
		camera = PiCamera()
		#camera.resolution(1920,1080)
		camera.start_preview()
		sleep(5)
		filename_pilib = filename + "_pilib.jpg"
		camera.capture(filename_pilib)
		camera.stop_preview()

	#Either take picture with webcam only, or with both
	if cam_choice != 0:

			filename_webcamcv = filename + "_webcamcv.jpg"

			capture = cv2.VideoCapture(1)

			capture.set(CV2_WIDTH_ID, 3280)
			capture.set(CV2_HEIGHT_ID, 2464)

			frame = capture.read()[1]

			cv2.imwrite(filename_webcamcv, frame)
			capture.release()

			####Take picture with fswebcam
			filename_fswebcam = filename + "_fswebcam.jpg"
			capture_web(filename_fswebcam)


	#Preview images
	if cam_choice == 0:
		preview_images((filename_picv,filename_pilib))

	elif cam_choice == 1:
		preview_images((filename_webcamcv,filename_fswebcam))

	else:
		preview_images((filename_picv,filename_pilib, filename_webcamcv,filename_fswebcam))
	
	#SFTP if arguments are passed
	if len(sys.argv) > 3:

		HOST = sys.argv[3]
		UNAME =  sys.argv[4]
		PWD = getpass.getpass('Password:')

		server = pysftp.Connection(host=HOST, port=22, username=UNAME, password=PWD)

		if cam_choice == 0:

			with server.cd("Pictures"):
				server.put(filename_picv)
				server.put(filename_pilib)

		elif cam_choice == 1:

			with server.cd("Pictures"):
				server.put(filename_webcamcv)
				server.put(filename_fswebcam)

		else:
			with server.cd("Pictures"):
				server.put(filename_picv)
				server.put(filename_pilib)
				server.put(filename_webcamcv)
				server.put(filename_fswebcam)

		print ("Safe Transfer Successful")
		server.close()


if __name__ == '__main__':
	main()