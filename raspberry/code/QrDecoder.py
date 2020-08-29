from Camera import Camera
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import re

class QrDecoder:

    def __init__(self, camera, visualize = True):
        self.cam = camera
        self.show = visualize

    def decode(self):
        im = self.cam.getFrame()

        available = False
        latitude = None
        longitude = None

        decodedObjects = pyzbar.decode(im)

        for decodedObject in decodedObjects:
            points = decodedObject.polygon
            if len(points) > 4:
                hull = cv2.convexHull(np.array([point for point in points], dtype = np.float32))
                hull = list(map(tuple, np.squeeze(hull)))
            else:
                hull = points

            n = len(hull)

            for j in range(0, n):
                cv2.line(im, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

            if decodedObject.type == 'QRCODE':
                data = decodedObject.data.decode("ISO-8859-1")
                if 'geo' in data:
                    fields = re.split('[, :]', data)
                    available = True
                    latitude = float(fields[1])
                    longitude = float(fields[2])

        if self.show:
            cv2.namedWindow('qrdecoder', cv2.WINDOW_NORMAL)
            cv2.imshow('qrdecoder', im)
            cv2.waitKey(1)

        return im, available, latitude, longitude

if __name__ == '__main__':
    cam = Camera()
    dec = QrDecoder(cam)

    while(True):
        im, available, latitude, longitude = dec.decode()
        if available:
            print(latitude, longitude)
