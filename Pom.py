import random
import pygame

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
        self.facing = facing  # Store the chosen direction
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
            bush_rect = pygame.Rect(bush.rect.x, bush.rect.y, 1, 1)  # Create a Rect for the bush
            if bush_rect.colliderect(self.rect):  # Check if bush is in visible area
                distance = self.rect.centerx - bush_rect.centerx + self.rect.centery - bush_rect.centery
                if abs(distance) < min_distance:
                    min_distance = abs(distance)
                    closest_bush = bush

            # Move the PomPom
            new_rect = self.rect.move(dx, dy)

            if 0 <= new_rect.x < width and 0 <= new_rect.y < height:
                self.rect = new_rect
            else:
                self.randomMove(width, height)  # If pathfinding leads outside, move randomly
        else:
            self.randomMove(width, height)  # If no bush found, move randomly



    def vision(self, size):
        """
        Updates the visibleTiles list of grid spots that the PomPom can currently see.
        Size should ALWAYS be an odd number.
        """
        visibleTiles = []  # List of visible tiles
        visCenter = size // 2  # Center offset (size is odd, so center will be exact middle)
        
        # Direction offsets for N, E, S, W based on the facing direction
        visCenterDirections = {
            'N': (0, -visCenter),    # North
            'E': (-visCenter, 0),    # East
            'S': (0, visCenter),     # South
            'W': (visCenter, 0)      # West
        }
        
        # Directional offset (dx, dy) for the current facing
        dx, dy = visCenterDirections[self.facing]
        
        # Top-left corner of the vision rectangle
        corner_x = self.rect.x + dx
        corner_y = self.rect.y + dy
        
        # Iterate over the vision area
        for i in range(size):
            for j in range(size):
                # Calculate tile coordinates
                tile_x = corner_x + i - visCenter
                tile_y = corner_y + j - visCenter
                visibleTiles.append((tile_x, tile_y))
        
        self.visableTiles = visibleTiles



    def eat(self):
        """
        when the pom encounters food, increase it's energy
        """
        self.energy = self.energy + 10 #change value?