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
        
    def update(self):
        """
        Handles PomPom's behavior per turn
        """
        self.energy -= 1  # Loses energy each turn
        if self.energy <= 0:
            return False  # Dies if energy reaches 0
        return True
    
    def move(self):
        """
        Moves the PomPom to a random adjacent tile or stays in place.
        Ensures it does not move out of bounds.
        """
        directions = [
            (0, 0),  # Stay in place
            (-1, 0), (1, 0),  # Left, Right
            (0, -1), (0, 1),  # Up, Down
            (-1, -1), (1, 1),  # Diagonal Top Left, Bottom Right
            (-1, 1), (1, -1)   # Diagonal Bottom Left, Top Right
        ]
        
        dx, dy = random.choice(directions)  # Pick a random direction
        new_x, new_y = self.x + dx, self.y + dy

        # Ensure movement stays within bounds
        if 0 <= new_x < width and 0 <= new_y < height:
            self.x, self.y = new_x, new_y