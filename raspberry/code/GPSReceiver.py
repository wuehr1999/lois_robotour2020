import serial
import threading
import time

class GPSReceiver:

    def __init__(self, port, baud):

        self.ser = serial.Serial(port, baud, timeout = 1)

        self.time = None
        self.coordinates = None

        self.threadRunning = True
        self.thread = threading.Thread(target = self.run)
        self.thread.start()

    def run(self):
        while (self.threadRunning):
            line = self.ser.readline()
            rawString = line.decode("ISO-8859-1")
            rawString.translate("ascii")
            pos = rawString.find("$G", 0, len(rawString) - 1)
            if pos > -1:
                NMEAString = rawString[pos: len(rawString) - 1]
                self.decode(NMEAString)

    def decode(self, NMEAString):
        stringList = NMEAString.split(",")
        #print(stringList)
        if stringList[0] == "$GNRMC" or stringList[0] == "$GPRMC":
            #print(stringList)
            self.decodeRMC(stringList)

    def decodeRMC(self, stringList):
        timeField = stringList[1]
        latField = stringList[3]
        nsField = stringList[4]
        lonField = stringList[5]
        weField = stringList[6]
        dateField = stringList[9]

        #print(timeField, latField, nsField, lonField, weField, dateField)

        hoursStr = timeField[0] + timeField[1]
        minutesStr = timeField[2] + timeField[3]
        secondsStr = timeField[4] + timeField[5]

        latDegStr = latField[0] + latField[1]
        latMinStr = latField[2] + latField[3] + latField[4] + latField[5] + latField[6] + latField[7] + latField[8]

        lonDegStr = lonField[0] + lonField[1] + lonField[2]
        lonMinStr = lonField[3] + lonField[4] + lonField[5] + lonField[6] + lonField[7] + lonField[8] + lonField[9]

        dayStr = dateField[0] + dateField[1]
        monthStr = dateField[2] + dateField[3]
        yearStr = dateField[4] + dateField[5]

        year = 2000 + int(yearStr)
        mon = int(monthStr)
        day = int(dayStr)
        hour = 2 + int(hoursStr)
        min = int(minutesStr)
        sec = int(secondsStr)

        self.time = time.struct_time((year, mon, day, hour, min, sec, -1, -1, -1))
        print(self.time)

        lat = float(latDegStr) + float(latMinStr) / 60
        if 'S' == nsField[0]:
            lat = -lat

        lon = float(lonDegStr) + float(lonMinStr) / 60
        if 'W' == weField[0]:
            lon = -lon

        self.coordinates = (lat, lon)
        print(self.coordinates)

if __name__ == "__main__":
    gps = GPSReceiver("/dev/ttyACM3", 9600)