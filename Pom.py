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
        self.directions = ['N','E','S','W']
        self.facing = random.choice(self.directions)
        self.visableTiles = []
        


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
        moves = {'N': (0, -1),
                 'E': (-1, 0),
                 'S': (0, 1),
                 'W': (1, 0)}

        moveChoice = random.choice(list(moves.items()))  # Pick a (key, value) pair
        facing, (dx, dy) = moveChoice  # Extract direction and movement tuple
        self.facing = facing  # Store the chosen direction

        new_x, new_y = self.x + dx, self.y + dy
        # Ensure movement stays within bounds
        if 0 <= new_x < width and 0 <= new_y < height:
            self.x, self.y = new_x, new_y
        else: self.move(width, height) #don't run into walls
    


    def vision(self, size):
        """
        Updates the visableTiles list of grid spots that the PomPom can currently see.
        Size should ALWAYS be an odd number.
        """
        visableTiles = []  # List of visible tiles
        visCenter = size // 2 + 1  #Finding the center
        visCenterExp = size // 2   #Finding the corner
        visCenterDirections = {
            'N': (0, -visCenter),
            'E': (-visCenter, 0), 
            'S': (0, visCenter), 
            'W': (visCenter, 0)
        }
        dx, dy = visCenterDirections[self.facing]
        # Top-left corner of vision rectangle
        corner_x, corner_y = self.x + dx - visCenterExp, self.y + dy - visCenterExp
        for i in range(size):
            for j in range(size):
                visableTiles.append((corner_x + i, corner_y + j))
        self.visableTiles = visableTiles


    def eat(self):
        """
        when the pom encounters food, increase it's energy
        """
        self.energy = self.energy + 10 #change value?