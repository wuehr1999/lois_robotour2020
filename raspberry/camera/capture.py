from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
 
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(640, 480))

counter = 0
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array
	rawCapture.truncate(0)	

	cv2.namedWindow('camera', cv2.WINDOW_NORMAL)
	cv2.imshow("camera", image)

	key = cv2.waitKey(1)
	if(key == 32):
            cv2.imwrite("%i.jpg"%counter, image)
            counter += 1
            print("saved")


