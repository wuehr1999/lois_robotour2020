from Camera import Camera
import numpy as np
import cv2
from matplotlib import pyplot as plt
import time

class RoadDetector:

    def __init__(self, camera, computeResolution = (100, 100), trainareaSizeX = 0.2, trainareaSizeY = 0.2, trainareaCenter = (0.5, 0.8), damping = 1.0, thresholdmultiplier = 10.0, maxHSVCompares = 30, horizonLine = 0.5):
        self.cam = camera
        self.resolution = computeResolution
        self.horizon = (int)(self.resolution[1] * horizonLine)
        self.trainareaStartX = (int)(trainareaCenter[0] * self.resolution[0] - trainareaSizeX / 2 * self.resolution[0])
        self.trainareaStopX = (int)(trainareaCenter[0] * self.resolution[0] + trainareaSizeX / 2 * self.resolution[0])
        self.trainareaStartY = (int)(trainareaCenter[1] * self.resolution[1] - trainareaSizeY / 2 * self.resolution[1])
        self.trainareaStopY = (int)(trainareaCenter[1] * self.resolution[1] + trainareaSizeY / 2 * self.resolution[1])
        self.D = damping
        self.thresholdFactor = thresholdmultiplier

        self.trainPixels = None

        if self.trainareaStartX in range(0, self.resolution[0]) and self.trainareaStopX in range(0, self.resolution[0])\
            and self.trainareaStartY in range(0, self.resolution[1]) and self.trainareaStopY in range(0, self.resolution[1]):
            self.trainPixels = (self.trainareaStopY - self.trainareaStartY) * (self.trainareaStopX - self.trainareaStartX)
            print("Started road detector with a training area of %i pixels..." % self.trainPixels)

        self.hueCounts = np.zeros(180, dtype = int)
        self.countThreshold = 0
        self.hValues = []
        self.valuesMax = maxHSVCompares

        self.image = None

        self.fig = plt.figure()
        self.win = self.fig.add_subplot(1, 1, 1)

    def detect(self):
        self.fetchHSV()
        self.analyzeTrainArea()
        self.checkImage()
        self.win.clear()
        self.win.plot(self.hueCounts)
        self.win.plot([0, 180], [self.countThreshold, self.countThreshold])
        self.fig.savefig("histogram.png")
        self.createRGB()
        self.image = cv2.rectangle(self.image, (self.trainareaStartX, self.trainareaStartY), (self.trainareaStopX, self.trainareaStopY), (0, 255, 0), 2)
        cv2.namedWindow('Camera', cv2.WINDOW_NORMAL)
        cv2.imshow('Camera', self.image)
        cv2.waitKey(1)

    def fetchHSV(self):
        self.image = cam.getFrame()
        self.image = cv2.resize(self.image, self.resolution)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

    def createRGB(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_HSV2BGR)

    def analyzeTrainArea(self):
        #trainArea = self.image[self.trainareaStartX:self.trainareaStopX, self.trainareaStartY:self.trainareaStopY]
        #color = ('b')#, 'g', 'r')
        #for i, col in enumerate(color):
        #    histogram = cv2.calcHist([self.image], [i], None, [256],[0, 256])
        #    plt.plot(histogram, color = col)
        #    plt.xlim([0, 256])
        #plt.show()
        #self.hueCounts = np.zeros(180, dtype = float)

        newCount = np.zeros(180, dtype = int)

        for x in range(self.trainareaStartX, self.trainareaStopX):
            for y in range(self.trainareaStartY, self.trainareaStopY):
                pixel = self.image[y, x]
                hue = pixel[0]
                newCount[hue] += 1

        self.countThreshold = 0

        for i in range(0, 180):
            self.hueCounts[i] = (1.0 - self.D) * self.hueCounts[i] + self.D * newCount[i]
            self.countThreshold += self.hueCounts[i]

        self.countThreshold = self.countThreshold / 180 * self.thresholdFactor

        if len(self.hValues) > self.valuesMax:
            self.hValues.clear()

        #print(self.hValues)
        for hue in range(0, 180):
            if self.hueCounts[hue] > self.countThreshold:
                if not hue in self.hValues:
                    self.hValues.append(hue)

    def checkImage(self):
        for x in range(0, self.resolution[0]):
            for y in range(self.horizon, self.resolution[1]):
                pixel = self.image[y, x]
                hue = pixel[0]
                if hue in self.hValues:
                    self.image[y, x] = [60, 100, 100]


if __name__ == '__main__':
    cam = Camera()
    detector = RoadDetector(camera = cam)
    while(True):
        detector.detect()
        histogram = cv2.imread('histogram.png')
        cv2.namedWindow('Histogram', cv2.WINDOW_NORMAL)
        cv2.imshow('Histogram', histogram)
        cv2.waitKey(1)
