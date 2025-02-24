import random
import pygame
import numpy
import math
from Food import Bush

class PomPom(object):
    """
    This will track an individual pompom and it's behavior
    """

    def __init__(self, x, y, grid):
        #import the world grid
        self.grid = grid
        #energy increases when food is eaten, decreases by 1 each turn
        self.energy = 10
        #What tiles the pom can see, changes direction as it moves
        directions = ['N','E','S','W']
        self.facing = random.choice(directions)
        self.vis = pygame.Rect(x, y, 3, 3)
        self.visableTiles = []
        #the pom's tile
        self.rect = pygame.Rect(x, y, 1, 1)
        #What the pom's generic move pattern is
        movePatterns = ["random","roomba"]
        self.movePattern = random.choice(movePatterns)
        #What the pom considers food
        foodTypes = ["herbavore","carnivore","omnivore"]
        self.foodType = random.choice(foodTypes)
        #the pom's mating availability
        self.mateReady = False
        self.cooldown = 0
        #tiles surrounding the pom
        self.adjacentTiles = [None for _ in range(9)]

        #initiate vision and adjacency
        self.updateAdjacentTiles(len(self.grid), len(self.grid))
        self.vision(5)
        self.visionTilesUpdate(5)
        

    def update(self, grid):
        """
        Handles PomPom's behavior per turn
        """
        self.grid = grid #match pom's grid to current grid
        self.energy -= 1  # Loses energy each turn
        self.cooldown -= 1
        if self.energy > 50:
            self.mateReady = True
        if self.energy < 30 or self.cooldown > 0:
            self.mateReady = False
        if self.energy <= 0:
            return False  # Dies if energy reaches 0
        
        self.findMate(len(self.grid), len(self.grid)) 
        self.seekBushes(len(self.grid), len(self.grid))
        self.updateAdjacentTiles(len(self.grid), len(self.grid))
        self.vision(5)
        self.visionTilesUpdate(5)

        return True
    

    def updateAdjacentTiles(self, width, height):
        #TODO test this
        """
        Populates a list with the coordinates of the 8 tiles surrounding the PomPom.
        """
        self.adjacent_tiles = []  # Reset adjacent tiles list
        directions = [(-1, -1), (0, -1), (1, -1),  # Top-left, Top, Top-right
                    (-1, 0), (1, 0),  # Left, Right
                    (-1, 1), (0, 1), (1, 1)]  # Bottom-left, Bottom, Bottom-right

        for dx, dy in directions:
            new_x, new_y = self.rect.x + dx, self.rect.y + dy
            if 0 <= new_x < width and 0 <= new_y < height:  # Ensure within bounds
                self.adjacent_tiles.append((new_x, new_y))

    
    def findMate(self, width, height):
        """
        If the PomPom has enough energy, try to reproduce
        """
        if not self.mateReady:
            return

        closest_pom = None
        min_distance = float('inf')
        dx, dy = 0, 0  # Default movement direction (no movement)

        # Check all PomPoms in the visible area
        for tile in self.visableTiles:
            x, y = tile #coords of current tile
            if self.grid[x][y] and isinstance(self.grid[x][y], PomPom): #if pompom visable
                pom = self.grid[x][y] #save the pom
                if pom is not self and self.grid[x][y].rect.colliderect(self.vis) and pom.mateReady: #maybe remove grid collision?
                    distance = abs(self.rect.centerx - pom.rect.centerx) + abs(self.rect.centery - pom.rect.centery)
                    if distance < min_distance:
                        min_distance = distance
                        closest_pom = pom

        if closest_pom:
            pomx, pomy = closest_pom.rect.x, closest_pom.rect.y  # Closest mate's coordinates

            # If the mate is adjacent, stay still, mate, and enter cooldown
            if (pomx, pomy) in self.adjacent_tiles:
                dx, dy = 0, 0
                self.energy -= 20  # Reduce energy
                self.cooldown = 10  # 10-round cooldown
                closest_pom.gotMated()
                return  # Exit function after mating

            # Move towards the mate if not adjacent
            x_dist = self.rect.x - pomx
            y_dist = self.rect.y - pomy

            if abs(x_dist) > abs(y_dist):  # Prioritize horizontal movement
                dx = -numpy.sign(x_dist)
            else:  # Otherwise, move vertically
                dy = -numpy.sign(y_dist)

            # Move the PomPom
            new_rect = self.rect.move(dx, dy)
            if 0 <= new_rect.x < width and 0 <= new_rect.y < height:
                self.updateFacing(self.rect.x, self.rect.y, new_rect.x, new_rect.y)
                self.rect = new_rect
            else:
                self.genericMove(width, height)  # If pathfinding leads outside, move randomly

        else:
            self.genericMove(width, height)  # If no mate is found, move randomly
    

    def gotMated(self):
        """
        when a different pompom mates with you, you still loose then energy and cooldown
        """
        self.energy -= 20  # Reduce energy
        self.cooldown = 10  # 10-round cooldown


    
    def seekBushes(self, width, height):
        """
        herbavore pompoms move towards bushes
        If bush isn't in sight, then do generic move
        """
        if self.mateReady == True:
            return
        closest_bush = None
        min_distance = float('inf')
        dx, dy = 0, 0  # Default movement direction (no movement)

        # Check all bushes to see if they are within the PomPom's visible tiles
        for tile in self.visableTiles:
            x, y = tile #coords of current tile
            if self.grid[x][y] and isinstance(self.grid[x][y], Bush): #if bush visable
                bush = self.grid[x][y] #save the bush
                if bush.cooldown == 0: #maybe remove grid collision?
                    distance = abs(self.rect.centerx - bush.rect.centerx) + abs(self.rect.centery - bush.rect.centery)
                    if distance < min_distance:
                        min_distance = distance
                        closest_bush = bush

        if closest_bush:
            if self.rect.x == closest_bush.rect.x and self.rect.y == closest_bush.rect.y and closest_bush.cooldown == 0:
                #if on top of closest bush, eat it
                self.eat()  # Gain energy from eating
                closest_bush.eaten()
                return
            else:
                #otherwise, move towards bush
                bushx, bushy = closest_bush.rect.x, closest_bush.rect.y #cloesest bush coords
                #xory is positive if the bush is closer on the x axis, negative for y
                x_dist = self.rect.x - bushx
                y_dist = self.rect.y - bushy

                if abs(x_dist) > abs(y_dist):  # Prioritize horizontal movement
                    dx = -numpy.sign(x_dist)
                else:  # Otherwise, move vertically
                    dy = -numpy.sign(y_dist)

                # Move the PomPom
                new_rect = self.rect.move(dx, dy)
                if 0 <= new_rect.x < width and 0 <= new_rect.y < height:
                    self.updateFacing(self.rect.x, self.rect.y, new_rect.x, new_rect.y)
                    self.rect = new_rect
                else:
                    self.genericMove(width, height)  # If pathfinding leads outside, move randomly
        else:
            self.genericMove(width, height)  # If no bush found, move randomly
    

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


    def visionTilesUpdate(self, size):
        """
        Updates the visible tiles list, ensuring only valid grid tiles are included.
        """
        self.visableTiles = []  # Reset
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

        # Get grid dimensions
        grid_width = len(self.grid)
        grid_height = len(self.grid[0]) if grid_width > 0 else 0

        # Top-left corner of the vision rectangle
        corner_x = self.rect.x + dx
        corner_y = self.rect.y + dy

        # Iterate over the vision area
        for i in range(size):
            for j in range(size):
                # Calculate tile coordinates
                tile_x = corner_x + i - visCenter
                tile_y = corner_y + j - visCenter

                # Check if tile is within grid bounds
                if 0 <= tile_x < grid_width and 0 <= tile_y < grid_height:
                    visibleTiles.append((tile_x, tile_y))

        self.visableTiles = visibleTiles




    def genericMove(self, width, height):
        """
        moves the pompom determined by = it's heritable move pattern
        """
        if self.movePattern == "random":
            self.randomMove(width, height)
        elif self.movePattern== "roomba":
            self.moveForward(width,height)
        else: pass
    

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


    def eat(self):
        """
        when the pom encounters food, increase it's energy
        """
        self.energy = self.energy + 10 #change value?

    


