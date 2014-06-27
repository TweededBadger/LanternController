import ColourHandler


col = ColourHandler.ColourHandler()
try:
    col.createTables()
except:
    pass

col.insertColour(12,50,67)

colours = col.getAllColours()

#print colours
for row in colours:
    print row
