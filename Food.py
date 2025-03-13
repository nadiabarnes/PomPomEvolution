import pygame
import random
from config import values

class Bush:
    
    def __init__(self, x, y, grid):
        self.rect = pygame.Rect(x, y, 1, 1)
        self.x = x
        self.y = y
        self.cooldown = 0
        self.version = random.randint(1,3)
        
    def eaten(self):
        """ PomPom eats the bush, triggering cooldown. """
        self.cooldown = values.BUSH_COOLDOWN  # Goes on a 5-turn cooldown

    def update(self, grid):
        """ Regenerates after cooldown expires. """
        if self.cooldown > 0:
            self.cooldown -= 1  # Countdown per turn