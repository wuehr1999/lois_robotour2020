from RobotMap import RobotMap
from RpLidar import RpLidar
import threading
import numpy as np

class PathPlanner:

    def __init__(self):
        self.robotMap = RobotMap(400, 1, (49.001102, 12.828288, 0));
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
            heading = i
            if heading > 135:
                heading -= 135
            else:
                heading += 45

            heading = heading * np.pi / 180.0

            dist = data[i]
            if dist > 0 and i > 15 and i < 60:
                self.robotMap.setObstacle((dist, heading))
                #print(dist)
        self.robotMap.grid.save(("lidar.jpg"))
        self.robotMap.flush()

if __name__ == "__main__":
    planner = PathPlanner()
