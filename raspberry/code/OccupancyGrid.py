import numpy as np
import cv2
import imutils

class OccupancyGrid:

    def __init__(self, sizeCm, scale):

        self.scale = scale
        self.sizeCm = sizeCm
        self.size = (int)(sizeCm * self.scale)
        self.occupancyGrid = np.zeros((self.size, self.size, 3), np.uint8)

    def insertObstacle(self, coordinates = (0, 0), format = 'cartesian', color = (0, 0, 255), rad = 1):

        if(format == 'polar'):
            coordinates = (coordinates[0], coordinates[1] - np.pi)
            coordinates = self.pol2cart(coordinates)
        coords = (coordinates[0] * (int)(1 / self.scale), coordinates[1] * (int)(1 / self.scale))
        rad *= (int)(1 / self.scale)

        if(coords[0] < self.size and coords[0] > 0 and coords[1] < self.size and coords[1] > 0):
            self.occupancyGrid = cv2.circle(self.occupancyGrid, coords, rad, color, -1)

    def scroll(self, y):
        translationMatrix = np.float32([[1, 0, 0], [0, 1, y * (1 / self.scale)]])
        self.occupancyGrid=cv2.warpAffine(self.occupancyGrid, translationMatrix, (self.size, self.size))

    def rotate(self, angle):
        angle = (int)(angle / np.pi * 180)
        self.occupancyGrid = imutils.rotate(self.occupancyGrid, angle)

    def save(self, name):
        cv2.imwrite(name, self.occupancyGrid);

    def cart2pol(self, coordinates):
        coords = (coordinates[0] - self.size / 2, coordinates[1] - self.size / 2)
        rho = (int)(np.sqrt(coords[0] ** 2 + coords[1] ** 2))
        phi = (int)(np.arctan2(coords[1], coords[0]))
        return (rho, phi)

    def pol2cart(self, coordinates):
        x = (int)(coordinates[0] * np.cos(coordinates[1]) + self.sizeCm / 2)
        y = (int)(coordinates[0] * np.sin(coordinates[1]) + self.sizeCm / 2)
        return (x, y)

    def flush(self):
        self.occupancyGrid[0:(int)(self.size / 2), 0:self.size] = (0, 0, 0)

    def getGrid(self):
        grid = self.occupancyGrid.copy()
        return grid

if __name__ == '__main__':
    g = OccupancyGrid(400, 1)
    g.insertObstacle(coordinates = (20,np.pi), format= 'polar', color = (0, 0, 255), rad = 10)
    g.save("map.jpg")
    g.scroll(60);
    g.save("map1.jpg")
    g.rotate(np.pi / 2)
    g.save("map2.jpg")