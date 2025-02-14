import random

class PomPom(object):
    """
    This will track an individual pompom and it's behavior
    """

    def __init__(self, x, y):
        #start with randomized genetic traits unless created from evolution
        #also cotains energy level and xy position
        self.x = x
        self.y = y
        self.energy = 10
        directions = {'N': (0, -1),'NE': (-1, -1),
                      'E': (-1, 0),'SE': (-1, 1),
                      'S': (0, 1),'SW': (1, 1),
                      'W': (1, 0),'NW': (1, -1)}
        #self.facing = random.choice(directions) #start facing a random direction
        self.facing = 'N'
        


    def update(self):
        """
        Handles PomPom's behavior per turn
        """
        self.energy -= 1  # Loses energy each turn
        if self.energy <= 0:
            return False  # Dies if energy reaches 0
        return True
    


    def move(self, width, height):
        """
        Moves the PomPom to a random adjacent tile or stays in place.
        Ensures it does not move out of bounds.
        """
        moves = [
            (0, 0),  # Stay in place
            (-1, 0), (1, 0),  # Left, Right
            (0, -1), (0, 1),  # Up, Down
            (-1, -1), (1, 1),  # Diagonal Top Left, Bottom Right
            (-1, 1), (1, -1)   # Diagonal Bottom Left, Top Right
        ]

        dx, dy = random.choice(moves)  # Pick a random direction
        new_x, new_y = self.x + dx, self.y + dy

        # Ensure movement stays within bounds
        if 0 <= new_x < width and 0 <= new_y < height:
            self.x, self.y = new_x, new_y
        else: self.move(width, height) #don't run into walls
    


    def vision(self, size):
        """
        returns a list of grid spots that the pompom can currently see
        Size should ALWAYS be an odd number
        """
        visableTiles = [] #list of visable tiles
        #find the center of the vision rectangle relative to the pom pom
        visCenter = int(size/2)+1 #for finding the center
        visCenterExp = int(size/2) #for finding the corner
        visCenterDirections = {'N': (0, -(visCenter)),'NE': (-(visCenter), -(visCenter)),
                      'E': (-(visCenter), 0),'SE': (-(visCenter), visCenter),
                      'S': (0, visCenter),'SW': (visCenter, visCenter),
                      'W': (visCenter, 0),'NW': (visCenter, -visCenter)}
        dx, dy = visCenterDirections[self.facing]
        #top left corner of vision rectangle values, true to grid
        corner_x, corner_y = self.x + dx + visCenterExp, self.y + dy + visCenterExp
        for i in range(size):
            for j in range(size):
                visableTiles.add((corner_x+i,corner_y+j))
        return visableTiles
        
    

    def eat(self):
        """
        when the pom encounters food, increase it's energy
        """
        self.energy = self.energy + 10 #change value?