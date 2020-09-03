import numpy as np
import cv2

class Floodfill:

    def __init__(self, fieldNr = 49, driveableThreshold = 0.25):

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
        destinationFound = False
        stack = []

        values = np.full((self.fieldNr, self.fieldNr), self.fieldNr * self.fieldNr)

        pixel = self.fields[startPos[1], startPos[0]]
        pixel[0] = self.waypointColor[0]
        pixel[1] = self.waypointColor[1]
        pixel[2] = self.waypointColor[2]
        self.fields[startPos[1], startPos[0]]= pixel

        pixel = self.fields[10, 22]
        pixel[0] = self.waypointColor[0]
        pixel[1] = self.waypointColor[1]
        pixel[2] = self.waypointColor[2]
        self.fields[10, 22] = pixel

        stack.append((self.startPos[0], self.startPos[1], 0))

        destPos = None

        while len(stack) > 0:
            #print(len(stack))
            #print(stack)
            field = stack.pop()
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

                        stack.append((x - 1, y, fieldValue + 1))
                        stack.append((x + 1, y, fieldValue + 1))
                        stack.append((x, y + 1, fieldValue + 1))
                        stack.append((x, y - 1, fieldValue + 1))
                        #stack.append((x + 1, y - 1, fieldValue + 1))
                        #stack.append((x + 1, y + 1, fieldValue + 1))
                        #stack.append((x - 1, y - 1, fieldValue + 1))
                        #stack.append((x - 1, y + 1, fieldValue + 1))

        path = []

        x = destPos[0]
        y = destPos[1]
        #print(x, y)
        #print(values)
        while(not(x == self.startPos[0] and y == self.startPos[1]) and destinationFound):

            if x < 1:
                x = 1
            elif x > self.fieldNr - 2:
                x = self.fieldNr - 2

            if y < 1:
                y = 1
            elif y > self.fieldNr - 2:
                y = self.fieldNr - 2

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

if __name__ == '__main__':
    ff = Floodfill()