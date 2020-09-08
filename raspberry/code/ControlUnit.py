import serial
import sys
import threading
import numpy as np
import time
import queue

OPCODE_READ = 0x02
OPCODE_WRITE = 0x04
ERROR_FORMAT = ':e00000000\n'
ERROR_ACCESS = ':e00000001\n'

REG_STATE = 0x00
REG_VERSION = 0x01
REG_MOTOR_LEFT = 0x0011
REG_EMERGENCY_STOP = 0x0012
REG_MOTOR_RIGHT = 0x0021
REG_COMPASS_HEADING = 0x31
REG_AVG_SPEED = 0x41
REG_DEST_HEADING = 0x42
REG_SONAR_LEFT = 0x50
REG_SONAR_MIDDLE = 0x51
REG_SONAR_RIGHT = 0x52
REG_BARREL = 0x60

STATE_JOYDRIVE = 0x0000
STATE_HEADINGDRIVE = 0x0001

class ControlUnit:

    def __init__(self, port, baud):

        self.state = None
        self.version = None
        self.dutycycleLeft = None
        self.dutycycleRight = None
        self.emergencyStop = None
        self.compassHeading = None
        self.avgSpeed = None
        self.destHeading = None
        self.sonarLeft = None
        self.sonarMiddle = None
        self.sonarRight = None
        self.barrel = None

        self.commandQueue = queue.Queue()

        self.ser = serial.Serial(port, baud, timeout = 1)

        self.threadRunning = True
        self.thread = threading.Thread(target = self.run)
        self.thread.start()

    def run(self):
        while (self.threadRunning):
            #print(100*"*")
            while not self.commandQueue.empty():
                command = self.commandQueue.get()
                #print(command)
                self.sendCommand(OPCODE_WRITE, command[0], command[1])
                self.commandQueue.task_done()
            self.update()
            #time.sleep(0.5)
            #print(100*"*")

    def sendCommandStr(self, commandStr):
        self.ser.write(commandStr.encode("utf-8"))
        #time.sleep(0.1)
        data = self.ser.readline(15).decode("ISO-8859-1")
        #time.sleep(0.1)
        return data

    def sendCommand(self, opcode, address, data = 0x0000):

        str = ""
        if(OPCODE_READ == opcode):
            str = (":%02x%04x\n" % (opcode, address))
        elif(OPCODE_WRITE == opcode):
            str = (":%02x%04x%04x\n" % (opcode, address, data))

        rec = self.sendCommandStr(str)
        #print(rec)

        retval = False

        if ERROR_ACCESS in rec:
            pass
        elif ERROR_FORMAT in rec:
            pass
        elif(len(rec) > 9):
            addrStr = rec[1 : 5]
            dataStr = rec[5 : 9]

            recAddress = np.uint16(int(addrStr, 16))
            recData = np.int16(int(dataStr, 16))

            retval = (recAddress, recData)

        return retval

    def read(self, address, oldValue):
        rec = self.sendCommand(OPCODE_READ, address)
        value = oldValue
        #print(rec)
        if rec is None or rec is False:
            pass
        else:
            value = rec[1]
        #print(value)
        return value

    def update(self):
        self.state = self.read(REG_STATE, self.state)
        self.version = self.read(REG_VERSION, self.version)
        self.dutycycleLeft = self.read(REG_MOTOR_LEFT, self.dutycycleLeft)
        self.dutycycleRight = self.read(REG_MOTOR_RIGHT, self.dutycycleRight)
        self.emergencyStop = self.read(REG_EMERGENCY_STOP, self.emergencyStop)
        self.compassHeading = self.read(REG_COMPASS_HEADING, self.compassHeading)
        self.avgSpeed = self.read(REG_AVG_SPEED, self.avgSpeed)
        self.destHeading = self.read(REG_DEST_HEADING, self.destHeading)
        self.sonarLeft = self.read(REG_SONAR_LEFT, self.sonarLeft)
        self.sonarMiddle = self.read(REG_SONAR_MIDDLE, self.sonarMiddle)
        self.sonarRight = self.read(REG_SONAR_RIGHT, self.sonarRight)
        self.barrel = self.read(REG_BARREL, self.barrel)

    def driveByDutycycle(self, leftDutycycle, rightDutycycle):
        self.commandQueue.put((REG_STATE, STATE_JOYDRIVE))
        self.commandQueue.put((REG_MOTOR_LEFT, np.int16(leftDutycycle)))
        self.commandQueue.put((REG_MOTOR_RIGHT, np.int16(rightDutycycle)))
        self.commandQueue.join()

    def driveByHeading(self, heading, avgSpeed):
        print(heading, avgSpeed)
        self.commandQueue.put((REG_STATE, STATE_HEADINGDRIVE))
        self.commandQueue.put((REG_AVG_SPEED, np.int16(avgSpeed)))
        self.commandQueue.put((REG_DEST_HEADING, np.int16(heading)))

if __name__ == "__main__":
    ecu = ControlUnit("/dev/ttyACM0", 9600)
    while(True):
        print(ecu.sonarLeft, ecu.sonarMiddle, ecu.sonarRight, ecu.compassHeading)
