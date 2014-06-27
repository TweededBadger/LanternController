import serial
#import randint
import random

class ArduinoConnection():
    def __init__(self):
        self.ser = serial.Serial("COM3", 115200,timeout=1.0,writeTimeout=1.0)   # open serial port that Arduino is using
        # print self.ser                        # print serial config
        # self.ser.close()
        pass




    def test(self):
        self.ser.write("0,0,0,255")


    def sendRandomColours(self):

        sendstring = "4,"
        for x in range(0, 9):
            sendstring += str(random.randint(0,254))
            sendstring += ","
            sendstring += str(random.randint(0,254))
            sendstring += ","
            sendstring += str(random.randint(0,254))
            sendstring += ","
        print sendstring
        self.ser.write(sendstring)

    def reconnect(self):
        self.ser.close()
        self.ser.open()
    def sendmultiColour(self,mode,values,r,g,b):
        try:
            self.ser.write(str(mode)+","+str(values[0])+","+str(values[1])+","+str(values[2])+","+str(values[3])+","+str(values[4])+","+str(values[5])+","+str(values[6])+","+str(values[7])+","+str(values[8])+","+str(r)+","+str(g)+","+str(b)+",")
        except:
            print "writefail"
            self.reconnect()
            self.sendmultiColour(mode,values,r,g,b)
    def sendSingleColour(self,mode,r,g,b):
        # self.ser = serial.Serial("COM3", 115200)
        # self.ser.open()
        try:
            self.ser.write(str(mode)+","+str(r)+","+str(g)+","+str(b)+",")
        except:
            print "writefail"
            self.reconnect()
            self.sendSingleColour(mode,r,g,b)
        # self.ser.close()

    def sendColour(self,type,r,g,b,r2,g2,b2):
        self.ser.write(str(type)+","+r+","+g+","+b+","+r2+","+g2+","+b2+",")