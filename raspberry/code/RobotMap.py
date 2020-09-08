from OccupancyGrid import OccupancyGrid
import numpy as np
from pyroutelib3 import Router

class RobotMap:

    def __init__(self, gridSize, gridScale, initialPositionGPS, robotHeading):
        self.grid = OccupancyGrid(gridSize, gridScale)
        self.size = gridSize

        self.waypointColor = (0, 0, 255);
        self.obstacleColor = (0, 255, 0);

        self.position = initialPositionGPS;
        self.heading = robotHeading
        self.currentWaypoint = None

        self.updateIteration = 0;

    def setInitialPosition(self, positionGPS):
        self.position = positionGPS

    def updatePosition(self, positionGPS, robotHeading):

        coords = (positionGPS[0], positionGPS[1])
        dist = self.gpsDist(coords)

        gpsHeading = self.gpsHeading(coords)
        #print(gpsHeading * 180.0 / np.pi)
        #self.grid.rotate(gpsHeading)
        self.grid.rotate(robotHeading - self.heading);
        self.heading = robotHeading
        #print(dist)
        self.grid.scroll(dist)

        self.position = positionGPS

        #self.grid.save(("%i.jpg" % self.updateIteration))
        self.updateIteration += 1

    def getPosition(self):
        return self.position

    def gpsDist(self, coordinatesGPS):
        la1 = self.position[0]
        la2 = coordinatesGPS[0]
        lo1 = self.position[1]
        lo2 = coordinatesGPS[1]

        latitude1R = (la1 * np.pi) / 180.0
        longitude1R = (lo1 * np.pi) / 180.0
        latitude2R = (la2 *  np.pi) / 180.0
        longitude2R = (lo2 * np.pi)/ 180.0

        dlat = latitude2R - latitude1R;
        dlong = longitude2R - longitude1R;

        a = np.sin(dlat / 2.0) * np.sin(dlat / 2.0) + np.cos(latitude1R) * np.cos(latitude2R) * np.sin(dlong / 2.0) * np.sin(dlong / 2.0)

        return 6371000 * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)) * 100;

    def gpsHeading(self, coordinatesGPS):
        la1 = self.position[0]
        la2 = coordinatesGPS[0]
        lo1 = self.position[1]
        lo2 = coordinatesGPS[1]

        latitude1R = (la1 * np.pi) / 180.0
        longitude1R = (lo1 * np.pi) / 180.0
        latitude2R = (la2 *  np.pi) / 180.0
        longitude2R = (lo2 * np.pi)/ 180.0

        y = np.sin(longitude2R - longitude1R) * np.cos(latitude2R)
        x = np.cos(latitude1R) * np.sin(latitude2R) - np.sin(latitude1R) * np.cos(latitude2R) * np.cos(longitude2R - longitude1R);

        return np.arctan2(y, x);

    def setObstacle(self, coordinates, coordinatesFormat, radius = 10):
        self.grid.insertObstacle(coordinates = coordinates, format = coordinatesFormat, color = self.obstacleColor, rad = radius)

    def setNextWaypoint(self, coordinatesGPS):
        self.currentWaypoint = coordinatesGPS
        dist = self.gpsDist(coordinatesGPS)
        if dist >= self.size:
            dist = self.size / 2 - 1
        heading = self.gpsHeading(coordinatesGPS)
        coords = (dist, heading)
        #print(coords)
        self.grid.insertObstacle(coordinates = coords, format = 'polar', color = self.waypointColor, rad = 10)

    def getWaypointDist(self):
        return self.gpsDist(self.currentWaypoint)

    def flush(self):
        self.grid.flush()
        #self.setNextWaypoint(self.currentWaypoint)

    def getGrid(self):
        return self.grid.getGrid()

    def copy(self):
        map = RobotMap(1, 1, 1, 1)
        map.size = self.size
        map.waypointColor = self.waypointColor
        map.obstacleColor = self.obstacleColor
        map.position = self.position
        map.heading = self.heading
        map.currentWaypoint = self.currentWaypoint
        map.updateIteration = self.updateIteration
        map.grid = OccupancyGrid(self.grid.sizeCm, self.grid.scale)
        map.grid.occupancyGrid = self.grid.occupancyGrid.copy()

        return map

if __name__ == '__main__':
    r = RobotMap(400, 1, (49.001102, 12.828288), 0);
    r.updatePosition((49.001167, 12.828470), 0)
    r.updatePosition((49.001219, 12.828049), 2.3)
    r.updatePosition((49.001241, 12.827968), 0)
    r.setObstacle((100, 0))
    r.setNextWaypoint((49.001241, 12.827968))
