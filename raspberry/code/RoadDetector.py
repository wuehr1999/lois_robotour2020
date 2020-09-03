from Camera import Camera
import numpy as np
import cv2
from matplotlib import pyplot as plt
import time

class RoadDetector:

    def __init__(self, camera, computeResolution = (66, 66), trainareaSizeX = 0.2, trainareaSizeY = 0.2, trainareaCenter = (0.5, 0.8), damping = 0.5, thresholdmultiplier = 1.0, maxHSVCompares = 30, horizonLine = 0.4, unwarpPixels = 0.1, mapDimensions = (150, 200), visualize = True):
        self.cam = camera
        self.resolution = computeResolution
        self.horizon = (int)(self.resolution[1] * horizonLine)
        self.trainareaStartX = (int)(trainareaCenter[0] * self.resolution[0] - trainareaSizeX / 2 * self.resolution[0])
        self.trainareaStopX = (int)(trainareaCenter[0] * self.resolution[0] + trainareaSizeX / 2 * self.resolution[0])
        self.trainareaStartY = (int)(trainareaCenter[1] * self.resolution[1] - trainareaSizeY / 2 * self.resolution[1])
        self.trainareaStopY = (int)(trainareaCenter[1] * self.resolution[1] + trainareaSizeY / 2 * self.resolution[1])
        self.D = damping
        self.thresholdFactor = thresholdmultiplier
        self.show = visualize

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

        self.dimensions = mapDimensions
        self.unwarpSrc = np.float32([[0, self.resolution[1]], [(self.resolution[0] / 2 - self.resolution[0] * unwarpPixels), self.horizon], [self.resolution[0], self.resolution[1]], [(self.resolution[0] / 2 + self.resolution[0] * unwarpPixels), self.horizon]])
        self.unwarpDst = np.float32([[0, self.dimensions[1]], [0, 0], [self.dimensions[0], self.dimensions[1]], [self.dimensions[0], 0]])
        self.transformMat = cv2.getPerspectiveTransform(self.unwarpSrc, self.unwarpDst)
        #print(self.unwarpSrc, self.unwarpDst)
        self.map = np.zeros((self.dimensions[0], self.dimensions[1], 3), np.uint8)

        self.objects = []

    def detect(self):
        self.fetchHSV()
        self.analyzeTrainArea()
        self.checkImage()
        self.unwarpImage()
        if self.show:
            self.visualize()
        return self.objects

    def visualize(self):
        #self.win.clear()
        #self.win.plot(self.hueCounts)
        #self.win.plot([0, 180], [self.countThreshold, self.countThreshold])
        #self.fig.savefig("histogram.png")
        self.createRGB()
        self.image = cv2.line(self.image, (0, self.horizon), (self.resolution[0], self.horizon), (0, 0, 255), 2)
        self.image = cv2.rectangle(self.image, (self.trainareaStartX, self.trainareaStartY), (self.trainareaStopX, self.trainareaStopY), (255, 0, 0), 2)
        cv2.namedWindow('Road', cv2.WINDOW_NORMAL)
        cv2.imshow('Road', self.image)
        #cv2.namedWindow('Birdeye', cv2.WINDOW_NORMAL)
        #cv2.imshow('Birdeye', self.map)
        #histogram = cv2.imread('histogram.png')
        #cv2.namedWindow('Histogram', cv2.WINDOW_NORMAL)
        #cv2.imshow('Histogram', histogram)
        cv2.waitKey(1)

    def fetchHSV(self):
        self.image = None
        self.image = self.cam.getFrame()
        self.image = cv2.resize(self.image, self.resolution)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

    def createRGB(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_HSV2BGR)
        self.map = cv2.cvtColor(self.map, cv2.COLOR_HSV2BGR)

    def analyzeTrainArea(self):
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

        #if len(self.hValues) > self.valuesMax:
        #    self.hValues.clear()
        self.hValues.clear()

        #print(self.hValues)
        for hue in range(0, 180):
            if self.hueCounts[hue] > self.countThreshold:
                #if not hue in self.hValues:
                #    self.hValues.append(hue)
                self.hValues.append(hue)

    def checkImage(self):
        for x in range(0, self.resolution[0]):
            for y in range(self.horizon, self.resolution[1]):
                pixel = self.image[y, x]
                hue = pixel[0]
                if hue in self.hValues:
                    self.image[y, x] = [60, 255, 255]

    def unwarpImage(self):
        self.map = np.zeros((self.dimensions[0], self.dimensions[1], 3), np.uint8)
        self.map = cv2.warpPerspective(self.image, self.transformMat, self.dimensions)

        self.objects.clear()
        for x in range(0, self.dimensions[0]):
            for y in range(0, self.dimensions[1]):
                pixel = self.map[y, x]
                if not (pixel[0] == 60 and pixel[1] == 255 and pixel[2] ==255):
                    tmpX = x - self.dimensions[0] / 2
                    tmpY = self.dimensions[1] - y
                    #print(tmpX, x)
                    self.objects.append((int(tmpX), int(tmpY)))
        #print(self.notDriveables)

if __name__ == '__main__':
    cam = Camera()
    detector = RoadDetector(camera = cam, visualize = True)
    while(True):
        detector.detect()
