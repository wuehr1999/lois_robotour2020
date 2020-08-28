from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import threading
import time

class Camera:

    def __init__(self, imageResolution = (640, 480), frameRate = 10, undistort = True, kVector = None, dVector = None, showImage = False):
        self.camera = PiCamera()
        self.resolution = imageResolution
        self.camera.resolution = (self.resolution[0], self.resolution[1])
        self.camera.framerate = frameRate
        self.rawCapture = PiRGBArray(self.camera, size=(self.resolution[0], self.resolution[1]))

        self.doUndistort = undistort
        self.k = kVector
        self.d = dVector
        if self.doUndistort and self.k is None and self.d is None:
            self.k = np.array([[131.0591747399141, 0.0, 325.6109942005655], [0.0, 130.9877981959816, 226.6276936355103], [0.0, 0.0, 1.0]])
            self.d = np.array([[0.09204057484647465], [-0.002797311299513488], [-0.019530859116416315], [0.004186341796441087]])

        self.show = showImage

        self.image = None
        self.copy = None

        self.threadRunning = True
        self.thread = threading.Thread(target = self.run)
        self.thread.start()

        time.sleep(2)
        print("Camera started...")

    def run(self):
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            if not self.threadRunning:
                break

            self.image = frame.array
            self.rawCapture.truncate(0)

            if self.doUndistort:
                map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.k, self.d, np.eye(3), self.k, self.resolution, cv2.CV_16SC2)
                self.image = cv2.remap(self.image, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

            self.copy = self.image.copy()
            if self.show:
                cv2.namedWindow('camera', cv2.WINDOW_NORMAL)
                cv2.imshow("camera", self.image)
                key = cv2.waitKey(1)

    def getFrame(self):
        return self.copy

if __name__ == '__main__':
    cam = Camera(showImage=True)

