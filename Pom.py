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