import cherrypy
import os.path
import json
import ColourHandler
from ArduinoConnection import ArduinoConnection
import threading
from datetime import datetime
import time

from twisted.internet.task import  LoopingCall
from twisted.internet import reactor

#import dataservice
from ConfigParser import SafeConfigParser
import logging
current_dir = os.path.dirname(os.path.abspath(__file__))+"/www"


class webserver():
    def __init__(self):

        pass
    def start(self):

        cherrypy.config.update({'server.socket_port': 8072})
        cherrypy.config.update({'server.socket_host': '0.0.0.0'})
        self.server = Server()
        cherrypy.quickstart(self.server,config="prod.conf")



        #cherrypy.quickstart(ImageServer(),config="prod.conf")

    def loop(self):
        self.server.loop()
        print "hello again"

class ImageServer():
    # _cp_config = {'tools.staticdir.on' : True,
    #               'tools.staticdir.dir' : imagepath,
    #               'tools.staticdir.index' : 'index.html',
    #               }

    #@cherrypy.expose
    pass

class Server(object):

#0 flash
#1 fade
#2 pulse
#3 instant change

    def __init__(self):
        self.ardConnection = ArduinoConnection()
        self.col = ColourHandler.ColourHandler()
        self.currentcolour = self.col.getNextColour()
        self.looping = True
        self.loopmode = 2
        self.looptime = 0.5
        self.count = 0
        self.lights = 0
        self.forward = True
        # self.lc = LoopingCall(self.loop)
        # self.lc.start(0.5)
        # reactor.run()
        self.startTimer()
        pass

    def startTimer(self):
        # self.timer = cherrypy.process.plugins.Monitor(cherrypy.engine,self.loop,self.looptime)
        self.timer = cherrypy.process.plugins.BackgroundTask(self.looptime,self.loop)

        # self.timer.subscribe()
        self.timer.start()
        # tasks = threading.Thread(target = self.loopThread)
        # tasks.start()


    def loopThread(self):
        import time
        while 1:
            time.sleep(self.looptime)
            self.loop()

    def loop(self):
        if (self.looping):
            if self.loopmode == 1:
                newcolour = self.col.getNextColour()
                self.currentcolour = newcolour
                print newcolour
                #print self.col.colourarray
                self.ardConnection.sendSingleColour(1,newcolour['red'],newcolour['green'],newcolour['blue'])
                #self.ardConnection.sendSingleColour(1,2,43,123)
                #self.ardConnection.sendRandomColours()
                # print "hello there"
            if self.loopmode == 2:
                self.lights += 1
                if self.lights == 10:
                    self.lights = 9
                    self.count += 1
                    if self.count > 10:
                        self.count = 0
                        self.lights = 0
                        self.forward = (self.forward == False)
                        self.currentcolour = self.col.getNextColour()

                values = [0,0,0,0,0,0,0,0,0]
                for x in range(0, self.lights):
                    if self.forward:
                        values[x] = 1
                    else:
                        values[8-x] = 1

                newcolour = self.currentcolour



                self.ardConnection.sendmultiColour(4,values,newcolour['red'],newcolour['green'],newcolour['blue'])

                # newcolour = self.col.getNextColour()
                print newcolour
                #print self.col.colourarray
                # self.ardConnection.sendSingleColour(3,newcolour['red'],newcolour['green'],newcolour['blue'])
                #self.ardConnection.sendSingleColour(1,2,43,123)
                #self.ardConnection.sendRandomColours()
                # print "hello there"
            if self.loopmode == 3:
                newcolour = self.currentcolour
                # print newcolour
                #print self.col.colourarray
                self.ardConnection.sendSingleColour(0,newcolour['red'],newcolour['green'],newcolour['blue'])
                #self.ardConnection.sendSingleColour(1,2,43,123)
                #self.ardConnection.sendRandomColours()
                # print "hello there"



    print current_dir
    _cp_config = {'tools.staticdir.on' : True,
                  'tools.staticdir.dir' : current_dir,
                  'tools.staticdir.index' : 'index.html',
                  }

    @cherrypy.expose
    def test(self):
        #reactor.run()
        self.timer.cancel()
        self.looptime = 2
        self.startTimer()
        # self.timer.stop()
        # self.timer.frequency = 2
        # self.timer.start()
        #elf.ardConnection.sendColour(2,r,g,b,r2,g2,b2)
        return "1"
    def changeColour(self,mode=1,r=0,g=0,b=0):
        self.ardConnection.sendSingleColour(mode,r,g,b)
        return "1"
    def getColours(self):
        col = ColourHandler.ColourHandler()
        colours = col.getAllColours()
        return json.dumps(colours)
    def addColour(self,r=0,g=0,b=0):
        col = ColourHandler.ColourHandler()
        col.insertColour(r,g,b)
        return "1"
    def setLoopMode(self,mode=1):
        print mode
        if int(mode) == 1:
            print "loop time 1"
            self.loopmode = 1;
            self.looptime = 60.0*5.0;
            # self.looptime = 5.0;
        if int(mode) == 2:
            print "loop time 2"
            self.loopmode = 2;
            self.looptime = 0.3;
        if int(mode) == 3:
            print "loop time 3"
            self.loopmode = 3;
            self.looptime = 1;
        self.timer.cancel()
        self.timer = cherrypy.process.plugins.BackgroundTask(self.looptime,self.loop)
        self.timer.start()
        time.sleep(1)
        self.loop()
        # self.timer.interval = self.looptime

    # def index(self):
    #     return "Hello World"
    #def service(self,d='',m='',y=''):
        #ds = dataservice.dataservice()
        #files = ds.getFileList(d,m,y)
        #print cherrypy.request.params
        #return json.dumps(files)

    test.exposed = True
    changeColour.exposed = True
    getColours.exposed = True
    addColour.exposed = True
    loop.exposed = True
    setLoopMode.exposed = True
