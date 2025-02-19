import random
import pygame
import numpy
import math
import Food

class PomPom(object):
    """
    This will track an individual pompom and it's behavior
    """

    def __init__(self, x, y):
        #start with randomized genetic traits unless created from evolution
        #also cotains energy level and xy position
        self.energy = 10
        self.directions = ['N','E','S','W']
        self.facing = random.choice(self.directions)
        self.visableTiles = []
        self.vis = pygame.Rect(x, y, 3, 3) #possibly initiate this better
        self.rect = pygame.Rect(x, y, 1, 1)
        

    def update(self):
        """
        Handles PomPom's behavior per turn
        """
        self.energy -= 1  # Loses energy each turn
        if self.energy <= 0:
            return False  # Dies if energy reaches 0
        return True
    

    def randomMove(self, width, height):
        """
        Moves the PomPom towards food (if found), or makes a random move if no food is visible.
        Ensures it does not move out of bounds and updates the facing direction correctly.
        Updates facing.
        """
        moves = {'N': (0, -1),
                    'E': (-1, 0),
                    'S': (0, 1),
                    'W': (1, 0)}
        moveChoice = random.choice(list(moves.items()))  # Pick a (key, value) pair
        facing, (dx, dy) = moveChoice  # Extract direction and movement tuple
        self.facing = facing  # Store the chosen direction #TODO use self.updateFacing
        new_rect = self.rect.move(dx, dy)
        # Ensure movement stays within bounds
        if 0 <= new_rect.x < width and 0 <= new_rect.y < height:
            self.rect = new_rect
        else:
            self.randomMove(width, height)
    


    def moveForward(self, width, height):
        moves = {'N': (0, -1),
                    'E': (-1, 0),
                    'S': (0, 1),
                    'W': (1, 0)}
        moveChoice = moves[self.facing]
        (dx, dy) = moveChoice
        new_rect = self.rect.move(dx, dy)
        # Ensure movement stays within bounds
        if 0 <= new_rect.x < width and 0 <= new_rect.y < height:
            self.rect = new_rect
        else:
            self.randomMove(width, height)



    def seekBushes(self, width, height, bushes):
        closest_bush = None
        min_distance = float('inf')
        dx, dy = 0, 0  # Default movement direction (no movement)

        # Check all bushes to see if they are within the PomPom's visible tiles
        for bush in bushes:
            bush_rect = bush.rect  #call
            if bush_rect.colliderect(self.vis):  #Check if bush is in visible area #haha
                distance = self.rect.centerx - bush_rect.centerx + self.rect.centery - bush_rect.centery
                if (abs(distance) < min_distance) and (bush.cooldown == 0):
                    min_distance = abs(distance)
                    closest_bush = bush

        if closest_bush:
            bushx, bushy = closest_bush.rect.x, closest_bush.rect.y #cloesest bush coords
            #xory is positive if the bush is closer on the x axis, negative for y
            xory = abs(self.rect.x - bushx) - abs(self.rect.y - bushy)
            if (self.rect.x - bushx) != 0 and (xory>1): #if bush is not lined up on x axis with pom
                dx = numpy.sign(self.rect.x - bushx)*(-1) #move closer on x axis
            elif self.rect.y - bushy != 0: #same for ys
                dy = numpy.sign(self.rect.y - bushy)*(-1)
            else: dx = numpy.sign(self.rect.x - bushx)*(-1)
            
            # Move the PomPom
            new_rect = self.rect.move(dx, dy)

            if 0 <= new_rect.x < width and 0 <= new_rect.y < height:
                self.updateFacing(self.rect.x, self.rect.y, new_rect.x, new_rect.y)
                self.rect = new_rect
            else:
                self.moveForward(width, height)  # If pathfinding leads outside, move randomly

        else:
            self.moveForward(width, height)  # If no bush found, move randomly
    


    def updateFacing(self, oldx, oldy, newx, newy):
        """
        Import original and updated coordinates, updates the pompom's facing variable
        """
        dx = oldx-newx
        dy = oldy - newy
        if dx > 0:
            self.facing = 'E'
        elif dx < 0:
            self.facing = 'W'
        elif dy > 0:
            self.facing = 'N'
        elif dy < 0:
            self.facing = 'S'



    def vision(self, size):
        """
        Creates a rectangle that act's as the pompom's range of sight
        size is how long one edge of the pom pom's vision is
        size should always be odd
        """
        visCenter = size // 2

        visCenterDirections = {
            'N': (0, -visCenter),    # North
            'E': (-visCenter, 0),    # East
            'S': (0, visCenter),     # South
            'W': (visCenter, 0)      # West
        }
        # Directional offset (dx, dy) for the current facing
        dx, dy = visCenterDirections[self.facing]
        # Create vision rectangle centered on PomPom's current position
        self.vis = pygame.Rect(
            self.rect.x - visCenter + dx,
            self.rect.y - visCenter + dy,
            size,
            size
        )



    def eat(self):
        """
        when the pom encounters food, increase it's energy
        """
        self.energy = self.energy + 10 #change value?