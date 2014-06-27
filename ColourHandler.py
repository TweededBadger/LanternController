import sqlite3 as lite
import sys
import time
import math

current_milli_time = lambda: int(round(time.time() * 1000))

class ColourHandler:
    def __init__(self):
        self.con = lite.connect("colours.db")
        self.index = 0
        self.test = "hello again"
        self.refreshColourArray()
        self.startMilli = current_milli_time()

    def refreshColourArray(self):
        self.colourarray = self.getAllColours()
    def createTables(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("CREATE TABLE Colours(id INTEGER PRIMARY KEY, red INT, green INT, blue INT)")

    def insertColour(self,r,g,b):
        with self.con:
            cur = self.con.cursor()
            cur.execute("INSERT INTO Colours(red,green,blue) VALUES({0},{1},{2});".format(r,g,b))


    def getNextColour(self):
        #colarray = self.getAllColours()
        colarray = self.colourarray
        returncol = colarray[self.index]
        self.index += 1
        if self.index > len(colarray)-1:
            self.index = 0
        return colarray[self.index]

    def getColourByTime(self):
        currentm = current_milli_time() - self.startMilli

        multi = float(currentm)*float(0.0001)
        r = int(((math.sin(multi)+1)/2)*255)
        if r < 10:
            r = 10

        g = int(((math.cos(multi)+1)/2)*255)
        if g < 10:
            g = 10

        colour = {}
        colour['red'] = r
        colour['blue'] = 0
        colour['green'] = g
        return colour


    def getAllColours(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT * FROM Colours")
            rows = cur.fetchall()
            colarray = []
            for row in rows:
                colarray.append(
                    {
                        'id':row[0],
                        'red':row[1],
                        'green':row[2],
                        'blue':row[3]
                     }
                )

            return colarray
