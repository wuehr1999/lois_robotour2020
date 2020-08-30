from Camera import Camera
from QrDecoder import QrDecoder
from RoadDetector import RoadDetector
import threading
import time

class CameraProcessor:

    def __init__(self, visualize = True):
        self.cam = Camera(showImage = True)

        self.show = visualize

        self.MODE_QRDECODE = 0
        self.MODE_ROADDETECT = 1

        self.mode = self.MODE_QRDECODE

        self.qrDecoder = QrDecoder(camera = self.cam, visualize = self.show)
        self.roadDetector = RoadDetector(camera = self.cam, visualize = self.show)

        self.threadRunning = True
        self.thread = threading.Thread(target = self.run)
        self.thread.start()

        self.data = None
        self.copy = None
        self.available = False

    def setMode(self, processingMode):
        self.mode = processingMode

    def run(self):
        while (self.threadRunning):

            if self.mode == self.MODE_ROADDETECT:
                self.data = self.roadDetector.detect()
                #print(len(self.data))

            elif self.mode == self.MODE_QRDECODE:
                self.data = self.qrDecoder.getCoordinates()

            if self.data is not None:
                self.copy = self.data.copy()
                self.available = True

    def getData(self):
        av = self.available
        self.available = False
        return av, self.copy


if __name__ == "__main__":

    proc = CameraProcessor()
    while(True):
        proc.setMode(proc.MODE_QRDECODE)
        print("switching to Qr detecting mode...")
        time.sleep(10)
        proc.setMode(proc.MODE_ROADDETECT)
        print("switching to road detecting mode...")
        time.sleep(10)