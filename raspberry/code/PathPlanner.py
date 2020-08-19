from RobotMap import RobotMap
from RpLidar import RpLidar
from osmRouter import OSMRouter
from GPSReceiver import GPSReceiver
import threading
import numpy as np
import cv2

class PathPlanner:

    def __init__(self, robotMap, rpLidar, gpsReceiver, osmRouter, waypointSwitchCM):
        self.map = robotMap
        self.lidar = rpLidar
        self.gps = gpsReceiver
        self.osm = osmRouter
        self.waypointSwitch = waypointSwitchCM

        self.destination = None

        self.threadRunning = True
        self.thread = threading.Thread(target = self.run)
        self.thread.start()

    def run(self):
        '''Worker thread for measuring and visualisation'''
        while (self.threadRunning):
            while self.destination is None:
                pass
            self.insertLidarData()

    def insertLidarData(self):
        data = self.lidar.getScan()
        for i in range(360):
            heading = i + 45
            if(heading >= 360):
                heading -= 360

            heading = heading * np.pi / 180.0

            dist = data[i]
            if dist > 0: #and i > 15 and i < 60:
                self.robotMap.setObstacle((dist, heading))
                #print(dist)
        #self.robotMap.grid.save(("lidar.jpg"))
        self.robotMap.flush()

        def insertPosition(self, coordinatesGPS, heading):
            self.map.updatePosition(coordinatesGPS, heading)

        def insertDestination(self, destCoordsGPS):
            self.destination = destCoordsGPS
            self.planRoute()

        def planRoute(self):
            osm.planRoute(self.map.getPosition(), self.destination)

        def insertNextWaypoint(self):
            waypoint, arrived = osm.getNextWaypoint()
            if not arrived:
                self.map.setNextWaypoint(waypoint)

if __name__ == "__main__":
    robotMap = RobotMap(800, 1, (49.001102, 12.828288), 0);
    lidar = RpLidar("/dev/ttyUSB0")
    osm = OSMRouter("/home/jonas/Documents/englmardorf.osm", "car")
    gps = GPSReceiver("/dev/ttyACM0")

    planner = PathPlanner(robotMap, lidar, gps, osm)
    planner.set

    while(True):
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.imshow('image', planner.robotMap.getGrid())
        cv2.waitKey(1)

