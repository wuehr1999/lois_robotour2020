import numpy as np
import cv2

class Floodfill:

    def __init__(self, fieldNr = 21, driveableThreshold = 0.5):

        self.fieldNr = fieldNr
        self.threshold = driveableThreshold
        if (self.fieldNr % 2) == 0:
            fieldNr += 1
        self.obstacleColor = None
        self.waypointColor = None
        self.fields = np.zeros((self.fieldNr, self.fieldNr, 3), np.uint8)
        start = (int)((self.fieldNr -1) / 2 + 1)
        self.startPos =(start, start)
        #print(self.fields)


    def planRoute(self, robotMap, obstacleThreshold = 0.5):
        grid = robotMap.getGrid()
        self.fields = cv2.resize(grid, (self.fieldNr, self.fieldNr))
        self.obstacleColor = robotMap.obstacleColor
        self.waypointColor = robotMap.waypointColor

        self.fill(self.startPos)

        #print(self.fields)

        #self.fill(self.startPos, 0)

        cv2.namedWindow('floodfill', cv2.WINDOW_NORMAL)
        cv2.imshow('floodfill', self.fields)
        cv2.waitKey(1)

    def fill(self, startPos):
        lastValue = 0
        destinationFound = False
        stack = []

        values = np.full((self.fieldNr, self.fieldNr), self.fieldNr * self.fieldNr)

        pixel = self.fields[startPos[1], startPos[0]]
        pixel[0] = self.waypointColor[0]
        pixel[1] = self.waypointColor[1]
        pixel[2] = self.waypointColor[2]
        self.fields[startPos[1], startPos[0]]= pixel

        pixel = self.fields[15, 5]
        pixel[0] = self.waypointColor[0]
        pixel[1] = self.waypointColor[1]
        pixel[2] = self.waypointColor[2]
        self.fields[15, 5] = pixel

        #for x in range(0, self.fieldNr):
        #    for y in range(0, self.fieldNr):
        #        pixel = self.fields[y, x]
        #        pixel[0] = 255
        #        self.fields[y, x] = pixel

        stack.append(startPos)

        destPos = self.startPos

        while len(stack) > 0:
            #print(len(stack))
            #print(stack)
            position = stack.pop()
            x = position[0]
            y = position[1]
            if x >= 0 and x < self.fieldNr and y >= 0 and y < self.fieldNr:
                pixel = self.fields[y, x]
                #print(pixel)
                driveable = True
                if pixel[1] >= self.obstacleColor[1] * self.threshold and pixel[2] >= self.obstacleColor[2] * self.threshold :
                    driveable = False
                    #print(pixel)
                elif pixel[1] == self.waypointColor[1] and pixel[2] == self.waypointColor[2] and x != self.startPos[0] and y != self.startPos[1]:
                    driveable = False
                    #print(pixel)
                    destinationFound = True
                    destPos = (x, y)
                    #print(destinationFound)

                if driveable and not destinationFound:
                    value = values[x, y]
                    newValue = lastValue + 1
                    #print(lastValue)
                    if newValue <= value:
                        lastValue = newValue
                        #pixel[0] = 255#(int)(newValue * 127 / (self.fieldNr * self.fieldNr)) + 127
                        #self.fields[y, x] = pixel
                        values[x, y] = newValue
                        #print(self.fields[y, x])
                        stack.append((x - 1, y - 1))
                        stack.append((x - 1, y + 1))
                        stack.append((x - 1, y))
                        stack.append((x + 1, y - 1))
                        stack.append((x + 1, y + 1))
                        stack.append((x + 1, y))
                        stack.append((x, y + 1))
                        stack.append((x, y - 1))

                #else:
                #    print(driveable, destinationFound, lastValue)
        path = []

        x = destPos[0]
        y = destPos[1]
        #print(values)
        while( x != self.startPos[0] and y != self.startPos[1]):
            valuesAround = []
            valuesAround.append(values[x, y + 1])
            valuesAround.append(values[x, y - 1])
            valuesAround.append(values[x + 1, y])
            valuesAround.append(values[x - 1, y])
            valuesAround.append(values[x - 1, y - 1])
            valuesAround.append(values[x + 1, y - 1])
            valuesAround.append(values[x - 1, y + 1])
            valuesAround.append(values[x + 1, y + 1])

            next = valuesAround.index(min(valuesAround))

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

        #for x in range(0, self.fieldNr):
        #    for y in range(0, self.fieldNr):
        #        pixel = self.fields[y, x]
        #        if pixel[0] == 255:
        #            pixel[0] = 0
        #        self.fields[y, x] = pixel

    #def fill(self, position, lastValue):
    #    x = position[0]
    #    y = position[1]
    #    if x > 0 and x < self.fieldNr and y > 0 and y < self.fieldNr:
    #        pixel = self.fields[y, x]
    #        driveable = True
    #        if pixel[0] >= self.obstacleColor[0] * self.threshold and pixel[1] >= self.obstacleColor[1] * self.threshold and pixel[2] >= self.obstacleColor[2] * self.threshold :
    #            driveable = False
    #        elif pixel[0] == self.waypointColor[0] and pixel[1] == self.waypointColor[1] and pixel[2] == self.waypointColor[2]:
    #            driveable = False
    #            self.destinationFound = True
    #
    #        if driveable and not self.destinationFound:
    #            value = pixel[0]
    #            newValue = lastValue + 1
    #            if newValue > value:
    #                pixel[0] = newValue
    #                self.fields[y, x] = pixel
    #                self.fill((x + 1, y), newValue)
    #                self.fill((x - 1 , y), newValue)
    #                self.fill((x, y + 1), newValue)
    #                self.fill((x, y -1), newValue)

if __name__ == '__main__':
    ff = Floodfill()