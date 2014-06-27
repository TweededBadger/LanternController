import serial
import time
import webservice
import threading
from twisted.internet import task
from twisted.internet import reactor
import urllib2

# Reminder to close the connection when finished

# def startLoopNonThreaded():
#     l = task.LoopingCall(loop)
#     l.start(5.0)
#     reactor.run()
# def loop():
#     print "loop"
#     urllib2.urlopen('http://localhost:8099/loop')
#     pass
#
# class WebServiceThread(threading.Thread):
#     def __init__(self,threadID):
#         threading.Thread.__init__(self)
#     def run(self):
#         self.ws = webservice.webserver()
#         self.ws.start()
#
# wsThread = WebServiceThread(2)
# wsThread.start()
# startLoopNonThreaded()

ws = webservice.webserver()
ws.start()


# while True:
#     print ser.readline()
#
#
# if(ser.isOpen()):
#     print "Serial connection is still open."