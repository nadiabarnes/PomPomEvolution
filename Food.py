import pygame

class Bush:
    
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 1, 1)
        self.cooldown = 0
        
    def eaten(self):
        """ PomPom eats the bush, triggering cooldown. """
        self.cooldown = 5  # Goes on a 5-turn cooldown

    def update(self):
        """ Regenerates after cooldown expires. """
        if self.cooldown > 0:
            self.cooldown -= 1  # Countdown per turn