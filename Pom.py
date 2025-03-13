import random
import pygame
import numpy
from Food import Bush
from config import values

class PomPom(object):
    """
    This will track an individual pompom and it's behavior
    """

    def __init__(self, x, y, grid, movePattern=None, foodType=None):
        #import the world grid
        self.grid = grid
        self.width = values.WIDTH
        self.height = values.HEIGHT
        #energy increases when food is eaten, decreases by 1 each turn
        self.age = 0
        self.energy = 20
        #What tiles the pom can see, changes direction as it moves
        directions = ['N','E','S','W']
        self.facing = random.choice(directions)
        self.vis = pygame.Rect(x, y, 3, 3)
        self.visableTiles = []
        #the pom's tile
        self.rect = pygame.Rect(x, y, 1, 1)
        #set the body bits
        #set the pom's generic move pattern
        if movePattern == None:
            movePatterns = ["random", "roomba", "wander"] 
            self.movePattern = random.choice(movePatterns)
        else:
            self.movePattern = movePattern
        self.turnCount = 0 #for move the extendedrandom move pattern
        #What the pom considers food
        if foodType == None:
            foodTypes = ["herb","carn"] #removed omnivore temp
            self.foodType = random.choice(foodTypes)
        else:
            self.foodType = foodType
        #the pom's mating availability
        self.mateReady = False
        self.cooldown = 40
        #the pom's flee counter
        self.flee = 0
        #tiles surrounding the pom
        self.adjacentTiles = [None for _ in range(9)]
        self.foodTypeSpecificSetup()
        #initiate vision and adjacency
        self.herbSize = values.HERB_VISION_SIZE
        self.carnSize = values.CARN_VISION_SIZE
        self.foodTypeVision()
        self.updateAdjacentTiles()


    def foodTypeSpecificSetup(self):
        if self.foodType == "herb":
            self.energy = values.HERB_START_ENERGY
            self.herbStartCooldown = values.HERB_START_COOLDOWN
        if self.foodType == "carn":
            self.energy = values.CARN_START_ENERGY
            self.carnStartCooldown = values.CARN_START_COOLDOWN
    

    def foodTypeVision(self):
        if self.foodType == "herb":
            self.vision(self.herbSize)
            self.visionTilesUpdate(self.herbSize)
        if self.foodType == "carn":
            self.vision(self.carnSize)
            self.visionTilesUpdate(self.carnSize)
        

    def update(self, grid):
        """
        Handles PomPom's behavior per turn
        """
        self.grid = grid #match pom's grid to current grid
        self.age = self.age+1
        self.energy -= 1  # Loses energy each turn
        self.cooldown -= 1
        if self.energy <= 0:
            return self.grid  # don't do anyhthing if dead
        
        self.isMateReady()
        #self.runFromCarn()  #TODO not working
        if self.mateReady:
            self.findMate() 
        else:
            self.findFood()
        self.updateAdjacentTiles()
        self.foodTypeVision()
        #self.bodyBitInteraction()
        return self.grid
    

    def updateAdjacentTiles(self):
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
            if 0 <= new_x < self.width and 0 <= new_y < self.height:  # Ensure within bounds
                self.adjacentTiles.append((new_x, new_y))

    #TODO make sure bits are on correct tiles
    def calcBodyBitTiles(self):
        """
        Returns a dictionary with coordinates of each body bit relative to the pom's position.
        """
        x, y = self.rect.x, self.rect.y  # Get pom's current position
        # Define coordinate shifts for each direction
        direction_offsets = {
            'N': [(0, -1), (1, 0), (0, 1), (-1, 0)],  # Front, right, back, left
            'W': [(1, 0), (0, 1), (-1, 0), (0, -1)],  # Front, right, back, left
            'S': [(0, 1), (-1, 0), (0, -1), (1, 0)],  # Front, right, back, left
            'E': [(-1, 0), (0, -1), (1, 0), (0, 1)]   # Front, right, back, left
        }
        # Get the correct offsets for the current facing direction
        offsets = direction_offsets[self.facing]
        # Create a dictionary of body bit positions
        body_bit_positions = {
            "bodyBit1": (x + offsets[0][0], y + offsets[0][1]),  # Front
            "bodyBit2": (x + offsets[1][0], y + offsets[1][1]),  # Right
            "bodyBit3": (x + offsets[2][0], y + offsets[2][1]),  # Back
            "bodyBit4": (x + offsets[3][0], y + offsets[3][1])   # Left
        }
        return body_bit_positions


    def bodyBitInteraction(self):
        positionsList = self.calcBodyBitTiles()

        for bitName, position in positionsList.items():
            x, y = position
            bodyBit = None
            if self.isValid((x,y)): 
                if isinstance(self.grid[x][y], PomPom):
                    pom = self.grid[x][y]
                    if bitName == "bodyBit1":
                        bodyBit = self.bodyBit1
                        bodyBit.collision(pom)
                    if bitName == "bodyBit2":
                        bodyBit = self.bodyBit2
                        bodyBit.collision(pom)
                    if bitName == "bodyBit3":
                        bodyBit = self.bodyBit3
                        bodyBit.collision(pom)
                    if bitName == "bodyBit4":
                        bodyBit = self.bodyBit4
                        bodyBit.collision(pom)


    def vision(self, size):
        if size > max(values.HERB_VISION_SIZE, values.CARN_VISION_SIZE):
            print("Something is terribly wrong: "+str(size))
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
        grid_width = self.width
        grid_height = self.height if grid_width > 0 else 0

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


    def genericMove(self):
        """
        moves the pompom determined by = it's heritable move pattern
        """
        if self.movePattern == "random":
            self.randomMove()
        elif self.movePattern== "roomba":
            self.moveForward()
        elif self.movePattern == "wander":
            self.randomExtended()
        else: pass

    
    def randomExtended(self):
        """
        Move 3-10 steps then turn a random direction.
        """
        moves = {'N': (0, -1),
                    'E': (-1, 0),
                    'S': (0, 1),
                    'W': (1, 0)}
        if self.turnCount <= 0:
            self.turnCount = random.randint(3,10)
            moveChoice = random.choice(list(moves.items()))  # Pick a (key, value) pair
            facing, (dx, dy) = moveChoice  # Extract direction and movement tuple
            self.facing = facing  # Store the chosen direction #TODO use self.updateFacing
        else:
            moveChoice = moves[self.facing]
            (dx, dy) = moveChoice
            self.turnCount -= 1
        new_rect = self.rect.move(dx, dy)
        # Ensure movement stays within bounds
        if 0 <= new_rect.x < self.width and 0 <= new_rect.y < self.height:
            self.rect = new_rect
        else:
            self.randomMove()
    

    def randomMove(self):
        """
        aka "random"
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
        if 0 <= new_rect.x < self.width and 0 <= new_rect.y < self.height:
            self.rect = new_rect
        else:
            self.randomMove()
    

    def moveForward(self):
        """
        aka "roomba"
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
        if 0 <= new_rect.x < self.width and 0 <= new_rect.y < self.height:
            self.rect = new_rect
        else:
            self.randomMove()
    
    #TODO test this
    def runFromCarn(self):
        """
        herbs move away from carns if they see them
        """
        closest_pom = None
        min_distance = float('inf')
        dx, dy = 0, 0  #Default movement direction (no movement)

        if self.foodType != "herb":
            #only herbs run away
            return
        for tile in self.visableTiles:
            x, y = tile #coords of current tile
            if self.grid[x][y] and isinstance(self.grid[x][y], PomPom): #if pompom visable
                pom = self.grid[x][y] #save the pom
                if pom is not self and self.grid[x][y].rect.colliderect(self.vis): #maybe remove grid collision?
                        distance = abs(self.rect.centerx - pom.rect.centerx) + abs(self.rect.centery - pom.rect.centery)
                        if pom.foodType == "carn" and distance < min_distance:
                            min_distance = distance
                            closest_pom = pom #closest visable carn

        if closest_pom:
            #if there is a carn, move away from it in one direction for x rounds
            self.flee = values.FLEE_TIME
            #only do something if you see a carn
            pomx, pomy = closest_pom.rect.x, closest_pom.rect.y  # Closest poms's coordinates

            x_dist = self.rect.x - pomx
            y_dist = self.rect.y - pomy

            if abs(x_dist) > abs(y_dist):  # Prioritize horizontal movement
                dx = numpy.sign(x_dist)
            else:  # Otherwise, move vertically
                dy = numpy.sign(y_dist)

            # Move the PomPom
            new_rect = self.rect.move(dx, dy)
            if 0 <= new_rect.x < self.width and 0 <= new_rect.y < self.height:
                self.updateFacing(self.rect.x, self.rect.y, new_rect.x, new_rect.y)
                self.rect = new_rect
        else:
            self.moveForward()


    def findFood(self):
        if self.foodType == "herb":
            self.seekBushes()
        elif self.foodType == "omnivore":
            self.seekBushes()
        elif self.foodType == "carn":
            self.seekPomPoms()
    

    def seekPomPoms(self):
        """
        carns look for pompoms to eat
        only hunts other carns if no herbs available
        if they have energy over cap, generic move
        """
        if self.energy > values.CARN_ENERGY_CAP:
            #if you have enough energy, only move around
            self.genericMove()
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
                        if pom.foodType == "carn":
                            distance = distance + 10 #will only hunt carns if herbs not available
                        if distance < min_distance:
                            min_distance = distance
                            closest_pom = pom

        if closest_pom:
            pomx, pomy = closest_pom.rect.x, closest_pom.rect.y  # Closest poms's coordinates

            # If the pom is adjacent, stay still, pom, and enter cooldown
            if (pomx, pomy) in self.adjacentTiles:
                dx, dy = 0, 0
                closest_pom.takeDamage(values.CARN_DAMAGE)
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
            if 0 <= new_rect.x < self.width and 0 <= new_rect.y < self.height:
                self.updateFacing(self.rect.x, self.rect.y, new_rect.x, new_rect.y)
                self.rect = new_rect
            else:
                self.genericMove()  # If pathfinding leads outside, move randomly
        else:
            self.genericMove()  # If no pom is found, move randomly


    def seekBushes(self):
        """
        herb pompoms move towards bushes
        If bush isn't in sight, then do generic move
        """
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
                if 0 <= new_rect.x < self.width and 0 <= new_rect.y < self.height:
                    self.updateFacing(self.rect.x, self.rect.y, new_rect.x, new_rect.y)
                    self.rect = new_rect
                else:
                    self.genericMove()  # If pathfinding leads outside, move randomly
        else:
            self.genericMove()  # If no bush found, move randomly
    

    def eat(self):
        """
        when the pom encounters food, increase it's energy
        """
        if self.foodType == "herb":
            self.energy = self.energy + values.HERB_EAT_ENERGY
        if self.foodType == "carn":
            self.energy = self.energy + values.CARN_EAT_ENERGY
    
    
    def takeDamage(self, damage):
        """
        when another pom attacks
        """
        self.energy = self.energy - damage


    def isMateReady(self):
        if self.foodType == "herb":
            if self.energy > values.HERB_START_MATE:
                self.mateReady = True
            if self.energy < values.HERB_END_MATE or self.cooldown > 0:
                self.mateReady = False
        elif self.foodType == "carn":
            if self.energy > values.CARN_START_MATE:
                self.mateReady = True
            if self.energy < values.CARN_END_MATE or self.cooldown > 0:
                self.mateReady = False


    def findMate(self):
        """
        If the PomPom has enough energy, try to reproduce
        """
        closest_pom = None
        min_distance = float('inf')
        dx, dy = 0, 0  # Default movement direction (no movement)

        # Check all PomPoms in the visible area
        for tile in self.visableTiles:
            x, y = tile #coords of current tile
            if self.grid[x][y] and isinstance(self.grid[x][y], PomPom): #if pompom visable
                pom = self.grid[x][y] #save the pom
                if pom is not self and self.grid[x][y].rect.colliderect(self.vis): #maybe remove grid collision?
                    if pom.mateReady and (pom.foodType == self.foodType):
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
            if 0 <= new_rect.x < self.width and 0 <= new_rect.y < self.height:
                self.updateFacing(self.rect.x, self.rect.y, new_rect.x, new_rect.y)
                self.rect = new_rect
            else:
                self.genericMove()  # If pathfinding leads outside, move randomly
        else:
            self.genericMove()  # If no mate is found, move randomly


    def successfulMate(self, mate):
        if self.foodType == "herb":
            self.energy -= values.HERB_MATE_LOSS  # Reduce energy
            self.cooldown = values.HERB_MATE_COOLDOWN
        if self.foodType == "carn":
            self.energy -= values.CARN_MATE_LOSS
            self.cooldown = values.CARN_MATE_COOLDOWN
        self.spawnBabies(mate)


    def gotMated(self):
        """
        when a different pompom mates with you, you still loose then energy and cooldown
        """
        if self.foodType == "herb":
            self.energy -= values.HERB_MATE_LOSS  # Reduce energy
            self.cooldown = values.HERB_MATE_COOLDOWN
        if self.foodType == "carn":
            self.energy -= values.CARN_MATE_LOSS
            self.cooldown = values.CARN_MATE_COOLDOWN


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
        food = random.choice([self.foodType, mate.foodType])
        pattern = random.choice([self.movePattern, mate.movePattern])
    
        return PomPom(x, y, self.grid, pattern, food)

