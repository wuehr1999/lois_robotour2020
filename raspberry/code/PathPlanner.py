from RobotMap import RobotMap
from RpLidar import RpLidar
from OsmRouter import OSMRouter
from GPSReceiver import GPSReceiver
from ControlUnit import ControlUnit
import threading
import numpy as np
import cv2
import time

class PathPlanner:

    def __init__(self, robotMap, rpLidar, gpsReceiver, osmRouter, controlUnit, waypointSwitchCM = 400, framesToFlush = 100, visualize = True):
        self.map = robotMap
        self.lidar = rpLidar
        self.gps = gpsReceiver
        self.osm = osmRouter
        self.ecu = controlUnit
        self.waypointSwitch = waypointSwitchCM

        self.show = visualize

        self.flushTicks = framesToFlush

        self.destination = None
        self.flushCounter = 0

        self.threadRunning = True
        self.thread = threading.Thread(target = self.run)
        self.thread.start()

    def run(self):
        '''Worker thread for measuring and visualisation'''
        while (self.threadRunning):
            #while self.destination is None:
                #pass
            self.flushCounter += 1
            if self.flushTicks < self.flushCounter:
                self.map.flush()
                self.flushCounter = 0

            self.insertPosition((49.001102, 12.828288), self.ecu.compassHeading * np.pi / 180.0)
            self.insertLidarData()
            self.insertSonarData()

    def insertLidarData(self):
        data = self.lidar.getScan()
        for i in range(360):
            heading = i + 45
            if(heading >= 360):
                heading -= 360

            heading = heading * np.pi / 180.0

            dist = data[i]
            if dist > 0 and i > 15 and i < 60:
                self.map.setObstacle((dist, heading))
                #print(dist)
        #self.map.grid.save(("lidar.jpg"))
        #self.map.flush()

    def insertSonarData(self):
        for i in range(30, 70):
            heading = i * np.pi / 180.0
            self.map.setObstacle(((self.ecu.sonarLeft), heading))

        for i in range(70, 110):
            heading = i * np.pi / 180.0
            self.map.setObstacle(((self.ecu.sonarMiddle), heading))

        for i in range(110, 150):
            heading = i * np.pi / 180.0
            self.map.setObstacle(((self.ecu.sonarRight), heading))

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
    robotMap = RobotMap(800, 1, (49.001102, 12.828288), 130 * np.pi / 180.0);
    lidar = RpLidar("/dev/ttyUSB0")
    osm = None#OSMRouter("/home/jonas/Documents/englmardorf.osm", "car")
    gps = None #GPSReceiver("/dev/ttyACM0")
    ecu = ControlUnit("/dev/ttyACM0", 9600)

    time.sleep(10)

    planner = PathPlanner(robotMap, lidar, gps, osm, ecu)

    while(True):
        cv2.namedWindow('map', cv2.WINDOW_NORMAL)
        cv2.imshow('map', planner.map.getGrid())
        time.sleep(0.1)
        cv2.waitKey(1)

