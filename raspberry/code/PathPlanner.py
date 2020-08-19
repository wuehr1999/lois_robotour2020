from RobotMap import RobotMap
from RpLidar import RpLidar
import threading
import numpy as np
import cv2

class PathPlanner:

    def __init__(self):
        self.robotMap = RobotMap(800, 1, (49.001102, 12.828288, 0));
        self.lidar = RpLidar("/dev/ttyUSB0")

        self.threadRunning = True
        self.thread = threading.Thread(target = self.run)
        self.thread.start()

    def run(self):
        '''Worker thread for measuring and visualisation'''
        while (self.threadRunning):
            lidarData = self.lidar.getScan()
            self.insertLidarData(lidarData)

    def insertLidarData(self, data):
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

if __name__ == "__main__":
    planner = PathPlanner()
    while(True):
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.imshow('image', planner.robotMap.getGrid())
        cv2.waitKey(1)

