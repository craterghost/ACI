class Coordinate(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def getX(self):
        # Getter method for a Coordinate object's x coordinate.
        # Getter methods are better practice than just accessing an attribute directly
        return self.x

    def getY(self):
        # Getter method for a Coordinate object's y coordinate
        return self.y

    #Coordinates as String
    def __str__(self):
        return '<' + str(self.getX()) + ',' + str(self.getY()) + '>'

    #Are Both Coordinates equal?
    def __eq__(self, other):
        return self.y == other.y and self.x == other.x

    #Method to print Coordinates
    def __repr__(self):
        return "Coordinate(%d, %d)" % (self.x, self.y)