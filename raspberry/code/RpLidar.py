from adafruit_rplidar import RPLidar
from math import cos, sin, pi, floor
import threading

class RpLidar:

    def __init__(self, port):
        self.lidar = RPLidar(None, port)

        print (100*"*")
        print ("Starting RpLidar...")
        print(self.lidar.info)
        print(self.lidar.health)
        print (100*"*")

        self.measurements = [0] * 360;

        self.threadRunning = True
        self.thread = threading.Thread(target = self.run)
        self.thread.start()

    def run(self):
        try:
            #scanData =  [0]*360
            for scan in self.lidar.iter_scans():
                if(not self.threadRunning):
                    break
                scanData = [0] * 360
                for (_, angle, distance) in scan:
                    scanData[min([359, floor(angle)])] = distance / 10
                self.measurements = scanData.copy()
                #print(scanData)
        except:
            pass
    def getScan(self):
        return self.measurements

    def stop(self):
        '''Stops RpLidar device'''

        self.threadRunning = False
        print(100 * "*")
        print("Stopping RpLidar")
        print(100 * "*")
        self.lidar.stop()
        self.lidar.stop_motor()
        self.lidar.disconnect()

if __name__ == "__main__":

    lidar = RpLidar("/dev/ttyUSB0")
    while(True):
        data = lidar.getScan()
        print(data)
