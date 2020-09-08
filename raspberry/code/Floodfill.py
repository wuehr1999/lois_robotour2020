import numpy as np
import cv2
import queue

class Floodfill:

    def __init__(self, fieldNr = 49, driveableThreshold = 0.5, visualize = True, trajectoryPart = 0.5):

        self.fieldNr = fieldNr
        self.threshold = driveableThreshold
        if (self.fieldNr % 2) == 0:
            fieldNr += 1
        self.obstacleColor = None
        self.waypointColor = None
        self.show = visualize
        self.fields = np.zeros((self.fieldNr, self.fieldNr, 3), np.uint8)
        start = (int)((self.fieldNr -1) / 2 + 1)
        self.startPos =(start, start)
        #print(self.fields)
        self.trajectoryPart = trajectoryPart
        self.trajectory = 0


    def planRoute(self, robotMap, obstacleThreshold = 0.5):
        grid = robotMap.getGrid()
        self.fields = cv2.resize(grid, (self.fieldNr, self.fieldNr))
        self.obstacleColor = robotMap.obstacleColor
        self.waypointColor = robotMap.waypointColor

        path = self.fill(self.startPos)

        #print(self.fields)

        #self.fill(self.startPos, 0)
        if self.show:
            cv2.namedWindow('floodfill', cv2.WINDOW_NORMAL)
            cv2.imshow('floodfill', self.fields)
            cv2.waitKey(1)

        if len(path) > 0:
            part = (int)(len(path) * self.trajectoryPart)
            xSum = 0
            ySum = 0
            #print(part)
            for i in range(0, part):
                #print(i)
                coord = path.pop()
                #print(coord)
                xSum += coord[0]
                ySum += coord[1]
            xAvg = float(xSum) / part - self.startPos[0]
            yAvg = self.startPos[1] - float(ySum) / part
            #print(xAvg, yAvg)
            self.trajectory = np.pi / 2.0 - np.arctan2(yAvg, xAvg)
            #print(self.trajectory * 180.0 / np.pi)
        return self.trajectory


    def fill(self, startPos):
        destinationFound = False
        stack = []
        fifo = queue.Queue()
        values = np.full((self.fieldNr, self.fieldNr), self.fieldNr * self.fieldNr)

        pixel = self.fields[startPos[1], startPos[0]]
        pixel[0] = self.waypointColor[0]
        pixel[1] = self.waypointColor[1]
        pixel[2] = self.waypointColor[2]
        self.fields[startPos[1], startPos[0]]= pixel

        #pixel = self.fields[5, 11]
        #pixel[0] = self.waypointColor[0]
        #pixel[1] = self.waypointColor[1]
        #pixel[2] = self.waypointColor[2]
        #self.fields[5, 11] = pixel

        #stack.append((self.startPos[0], self.startPos[1], 0))
        fifo.put((self.startPos[0], self.startPos[1], 0))

        destPos = None

        #while len(stack) > 0:
        while not fifo.empty():
            #print(len(stack))
            #print(stack)
            #field = stack.pop()
            field = fifo.get()
            x = field[0]
            y = field[1]
            fieldValue = field[2]
            if x >= 0 and x < self.fieldNr and y >= 0 and y < self.fieldNr:
                pixel = self.fields[y, x]
                #print(pixel)
                driveable = True
                if pixel[1] >= self.obstacleColor[1] * self.threshold and pixel[2] >= self.obstacleColor[2] * self.threshold :
                    driveable = False
                    #print(pixel)
                elif pixel[1] == self.waypointColor[1] and pixel[2] == self.waypointColor[2] and not (x == self.startPos[0] and y == self.startPos[1]):
                    destPos = (x, y)
                    driveable = False
                    destinationFound = True

                if driveable and not destinationFound:
                    value = values[x, y]
                    #print(lastValue)
                    if fieldValue < value and value == self.fieldNr * self.fieldNr:
                        #pixel[0] = 255#(int)(newValue * 127 / (self.fieldNr * self.fieldNr)) + 127
                        #self.fields[y, x] = pixel
                        values[x, y] = fieldValue
                        #print(self.fields[y, x])

                        #stack.append((x - 1, y, fieldValue + 1))
                        #stack.append((x + 1, y, fieldValue + 1))
                        #stack.append((x, y + 1, fieldValue + 1))
                        #stack.append((x, y - 1, fieldValue + 1))

                        fifo.put((x - 1, y, fieldValue + 1))
                        fifo.put((x + 1, y, fieldValue + 1))
                        fifo.put((x, y + 1, fieldValue + 1))
                        fifo.put((x, y - 1, fieldValue + 1))

                        #stack.append((x + 1, y - 1, fieldValue + 1))
                        #stack.append((x + 1, y + 1, fieldValue + 1))
                        #stack.append((x - 1, y - 1, fieldValue + 1))
                        #stack.append((x - 1, y + 1, fieldValue + 1))

                        #fifo.put((x + 1, y - 1, fieldValue + 1))
                        #fifo.put((x + 1, y + 1, fieldValue + 1))
                        #fifo.put((x - 1, y - 1, fieldValue + 1))
                        #fifo.put((x - 1, y + 1, fieldValue + 1))

        path = []

        if destinationFound:
            x = destPos[0]
            y = destPos[1]
            #print(x, y)
            #print(values)
            while(not(x == self.startPos[0] and y == self.startPos[1])):

                if x < 1:
                    x = 1
                elif x > self.fieldNr - 2:
                    x = self.fieldNr - 2

                if y < 1:
                    y = 1
                elif y > self.fieldNr - 2:
                    y = self.fieldNr - 2

                last = values[x, y]
                valuesAround = []
                valuesAround.append(values[x, y + 1])
                valuesAround.append(values[x, y - 1])
                valuesAround.append(values[x + 1, y])
                valuesAround.append(values[x - 1, y])
                #valuesAround.append(values[x - 1, y - 1])
                #valuesAround.append(values[x + 1, y - 1])
                #valuesAround.append(values[x - 1, y + 1])
                #valuesAround.append(values[x + 1, y + 1])
                #print(x, y)
                next = valuesAround.index(min(valuesAround))
                #next = valuesAround.index(last - 1)
                #print(valuesAround)
                #print(next)

                if next == 0:
                    y += 1
                elif next == 1:
                    y -= 1
                elif next == 2:
                    x += 1
                elif next == 3:
                    x -= 1
                elif next == 4:
                    x -= 1
                    y -= 1
                elif next == 5:
                    x += 1
                    y -= 1
                elif next == 6:
                    x -= 1
                    y += 1
                elif next == 7:
                    x += 1
                    y += 1

                pixel = self.fields[y, x]
                pixel[0] = 255
                self.fields[y, x] = pixel
                path.append((x, y))
            #print(path)
        return path

if __name__ == '__main__':
    ff = Floodfill()
