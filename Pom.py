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
        foodTypes = ["herbavore","carnivore"] #removed omnivore temp
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
        #TODO death doesn't work properly
        self.grid = grid #match pom's grid to current grid
        self.energy -= 1  # Loses energy each turn
        self.cooldown -= 1
        if self.energy <= 0:
            return self.grid  # don't do anyhthing if dead
        
        self.isMateReady()
        self.findMate(len(self.grid), len(self.grid)) 
        self.findFood(len(self.grid), len(self.grid))
        self.updateAdjacentTiles(len(self.grid), len(self.grid))
        self.vision(5)
        self.visionTilesUpdate(5)

        return self.grid
    

    def updateAdjacentTiles(self, width, height):
        #TODO test this
        """
        Populates a list with the coordinates of the 8 tiles surrounding the PomPom.
        """
        self.adjacentTiles = []  # Reset adjacent tiles list
        directions = [(-1, -1), (0, -1), (1, -1),  # Top-left, Top, Top-right
                    (-1, 0), (1, 0),  # Left, Right
                    (-1, 1), (0, 1), (1, 1)]  # Bottom-left, Bottom, Bottom-right

        for dx, dy in directions:
            new_x, new_y = self.rect.x + dx, self.rect.y + dy
            if 0 <= new_x < width and 0 <= new_y < height:  # Ensure within bounds
                self.adjacentTiles.append((new_x, new_y))


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
        """
        Roomba Style Movement. move in direction pom is facing,
        turn a random direction if cannot move forward
        """
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
    

    def findFood(self, width, height):
        if self.foodType == "herbavore":
            self.seekBushes(width, height)
        elif self.foodType == "omnivore":
            self.seekBushes(width, height)
        elif self.foodType == "carnivore":
            self.seekPomPoms(width, height)
    

    def seekPomPoms(self, width, height):
        if self.mateReady == True:
            return

        closest_pom = None
        min_distance = float('inf')
        dx, dy = 0, 0  # Default movement direction (no movement)

        # Check all PomPoms in the visible area
        for tile in self.visableTiles:
            x, y = tile #coords of current tile
            if self.grid[x][y] and isinstance(self.grid[x][y], PomPom): #if pompom visable
                pom = self.grid[x][y] #save the pom
                if pom is not self and self.grid[x][y].rect.colliderect(self.vis): #maybe remove grid collision?
                    distance = abs(self.rect.centerx - pom.rect.centerx) + abs(self.rect.centery - pom.rect.centery)
                    if distance < min_distance:
                        min_distance = distance
                        closest_pom = pom

        if closest_pom:
            pomx, pomy = closest_pom.rect.x, closest_pom.rect.y  # Closest poms's coordinates

            # If the pom is adjacent, stay still, pom, and enter cooldown
            if (pomx, pomy) in self.adjacentTiles:
                dx, dy = 0, 0
                closest_pom.takeDamage()
                if closest_pom.energy <= 0:
                    self.eat()
                return  # Exit function after mating

            # Move towards the pom if not adjacent
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
            self.genericMove(width, height)  # If no pom is found, move randomly


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
    

    def eat(self):
        """
        when the pom encounters food, increase it's energy
        """
        if self.foodType == "herbavore":
            self.energy = self.energy + 10 #change value?
        if self.foodType == "carnivore":
            self.energy = self.energy + 50
    
    
    def takeDamage(self):
        self.energy = self.energy - 30


    def isMateReady(self):
        if self.foodType == "herbavore":
            if self.energy > 50:
                self.mateReady = True
            if self.energy < 30 or self.cooldown > 0:
                self.mateReady = False
        elif self.foodType == "carnavore":
            if self.energy > 120:
                self.mateReady = True
            if self.energy < 70 or self.cooldown > 0:
                self.mateReady = False


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
            if (pomx, pomy) in self.adjacentTiles:
                dx, dy = 0, 0
                self.successfulMate(closest_pom)
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
    

    def successfulMate(self, mate):
        self.energy -= 20  # Reduce energy
        self.cooldown = 10
        self.spawnBabies(mate)


    def gotMated(self):
        """
        when a different pompom mates with you, you still loose then energy and cooldown
        """
        self.energy -= 20  # Reduce energy
        self.cooldown = 10  # 10-round cooldown


    def spawnBabies(self, mate):
        num = random.randint(1, 3)  # Number of babies
        available_spots = [pos for pos in self.adjacentTiles if pos is not None]
        #available_spots = [pos for pos in spawnPoints if self.isValid(pos)]
        random.shuffle(available_spots)  # Shuffle to randomize placement
        for i in range(min(num, len(available_spots))):  # Only place babies in valid spots
            x, y = available_spots[i]
            baby = self.createPom(mate, x, y)  #Assign position
            self.grid[baby.rect.x][baby.rect.y] = baby  #Place in grid


    def isValid(self, pos):
        """Check if the position is within bounds and empty."""
        x, y = pos
        return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0]) and self.grid[x][y] is None


    def createPom(self, mate, x, y):
        """
        Will look at the two parents and make a new pom
        with randomized genes from them.
        """
        baby = PomPom(x, y, self.grid)  # Create a new instance
        return baby


    


