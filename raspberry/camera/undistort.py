from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
 
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(640, 480))

DIM=(640, 480)
K=np.array([[131.0591747399141, 0.0, 325.6109942005655], [0.0, 130.9877981959816, 226.6276936355103], [0.0, 0.0, 1.0]])
D=np.array([[0.09204057484647465], [-0.002797311299513488], [-0.019530859116416315], [0.004186341796441087]])

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        img = frame.array
        rawCapture.truncate(0)  
        h,w = img.shape[:2]
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
        undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        cv2.namedWindow('camera', cv2.WINDOW_NORMAL)
        cv2.imshow("camera", undistorted_img)

        key = cv2.waitKey(1)

