import random
import pygame
import numpy
import math
from Food import Bush

class PomPom(object):
    """
    This will track an individual pompom and it's behavior
    """

    def __init__(self, x, y, grid, movePattern=None, foodType=None, herbVisionSize=3, carnVisionSize=7,
                 herbStartEnergy=10, herbStartCooldown=40, carnStartEnergy=100, carnStartCooldown=200):
        #import the world grid
        self.grid = grid
        #energy increases when food is eaten, decreases by 1 each turn
        self.energy = 20
        #What tiles the pom can see, changes direction as it moves
        directions = ['N','E','S','W']
        self.facing = random.choice(directions)
        self.vis = pygame.Rect(x, y, 3, 3)
        self.visableTiles = []
        #the pom's tile
        self.rect = pygame.Rect(x, y, 1, 1)
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
        self.foodTypeSpecificSetup(herbStartEnergy, herbStartCooldown, 
                                   carnStartEnergy, carnStartCooldown)
        #save inital values from world
        self.herbStartEnergy = herbStartEnergy
        self.carnStartEnergy = carnStartEnergy
        self.herbStartCooldown = herbStartCooldown
        self.carnStartCooldown = carnStartCooldown
        #initiate vision and adjacency
        self.herbSize = herbVisionSize
        self.carnSize = carnVisionSize
        self.foodTypeVision()
        self.updateAdjacentTiles(len(self.grid), len(self.grid))
    

    #TODO make these changable in simulate
    def foodTypeSpecificSetup(self, herbStartEnergy, herbStartCooldown,
                              carnStartEnergy, canStartCooldown):
        if self.foodType == "herb":
            self.energy = herbStartEnergy
            self.cooldown = herbStartCooldown
        if self.foodType == "carn":
            self.energy = carnStartEnergy
            self.cooldown = canStartCooldown
    

    def foodTypeVision(self):
        if self.foodType == "herb":
            self.vision(self.herbSize)
            self.visionTilesUpdate(self.herbSize)
        if self.foodType == "carn":
            self.vision(self.carnSize)
            self.visionTilesUpdate(self.carnSize)
        

    def update(self, grid, herbStartMate, herbEndMate, carnStartMate, carnEndMate,
                carnDamage, herbEatEnergy, carnEatEnergy, carnEnergyCap, herbMateCooldown,
                herbMateLoss, carnMateCooldown, carnMateLoss):
        """
        Handles PomPom's behavior per turn
        """
        self.grid = grid #match pom's grid to current grid
        self.energy -= 1  # Loses energy each turn
        self.cooldown -= 1
        if self.energy <= 0:
            return self.grid  # don't do anyhthing if dead
        
        #herb/carnStart is the energy threshold to be horny
        #herb/carnEnd is the energy threshold to be hungry
        self.isMateReady(herbStart = herbStartMate, herbEnd = herbEndMate, 
                         carnStart = carnStartMate, carnEnd = carnEndMate)

        if self.flee > 0:
            #flee time is how many turns they are frightened
            self.runFromCarn(len(self.grid), len(self.grid), fleeTime=5)

        elif self.mateReady:
            #herb/carnCooldown is how many turns until they can be horny again
            #herb/carnLoss is energy loss for mating
            self.findMate(len(self.grid), len(self.grid), herbCooldown = herbMateCooldown, 
                          herbLoss = herbMateLoss, 
                          carnCooldown = carnMateCooldown, carnLoss = carnMateLoss) 
    
        else:
            #carnDamage is the damage(energy loss) carns can deal per turn
            #herb/carnEatValue is how much energy gained from eating
            #carnEnergyCap is when carns stop hunting. Trust it's needed
            self.findFood(len(self.grid), len(self.grid), carnDamage = carnDamage, 
                          herbEatValue=herbEatEnergy, carnEatValue=carnEatEnergy, 
                          carnEnergyCap=carnEnergyCap)
        
        self.updateAdjacentTiles(len(self.grid), len(self.grid))
        self.foodTypeVision()

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
        elif self.movePattern == "wander":
            self.randomExtended(width, height)
        else: pass

    
    def randomExtended(self, width, height):
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
        if 0 <= new_rect.x < width and 0 <= new_rect.y < height:
            self.rect = new_rect
        else:
            self.randomMove(width, height)
    

    def randomMove(self, width, height):
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
        if 0 <= new_rect.x < width and 0 <= new_rect.y < height:
            self.rect = new_rect
        else:
            self.randomMove(width, height)
    

    def moveForward(self, width, height):
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
        if 0 <= new_rect.x < width and 0 <= new_rect.y < height:
            self.rect = new_rect
        else:
            self.randomMove(width, height)
    
    #TODO test this
    def runFromCarn(self, width, height, fleeTime):
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
            self.flee = fleeTime
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
            if 0 <= new_rect.x < width and 0 <= new_rect.y < height:
                self.updateFacing(self.rect.x, self.rect.y, new_rect.x, new_rect.y)
                self.rect = new_rect
        else:
            self.moveForward(width, height)


    def findFood(self, width, height, carnDamage, carnEatValue, herbEatValue, carnEnergyCap):
        if self.foodType == "herb":
            self.seekBushes(width, height, herbEatValue)
        elif self.foodType == "omnivore":
            self.seekBushes(width, height, herbEatValue)
        elif self.foodType == "carn":
            self.seekPomPoms(width, height, carnDamage, carnEatValue, carnEnergyCap)
    

    def seekPomPoms(self, width, height, carnDamage, carnEatValue, carnEnergyCap):
        """
        carns look for pompoms to eat
        only hunts other carns if no herbs available
        if they have energy over cap, generic move
        """
        if self.energy > carnEnergyCap:
            self.genericMove(width, height)
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
                closest_pom.takeDamage(carnDamage)
                if closest_pom.energy <= 0:
                    self.eat(carnEatValue = carnEatValue)
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


    def seekBushes(self, width, height, herbEatValue):
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
                self.eat(herbEatValue = herbEatValue)  # Gain energy from eating
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
    

    def eat(self, herbEatValue = 10, carnEatValue = 50):
        """
        when the pom encounters food, increase it's energy
        """
        if self.foodType == "herb":
            self.energy = self.energy + herbEatValue
        if self.foodType == "carn":
            self.energy = self.energy + carnEatValue
    
    
    def takeDamage(self, damage):
        """
        when another pom attacks
        """
        self.energy = self.energy - damage


    def isMateReady(self, herbStart, herbEnd, carnStart, carnEnd):
        if self.foodType == "herb":
            if self.energy > herbStart:
                self.mateReady = True
            if self.energy < herbEnd or self.cooldown > 0:
                self.mateReady = False
        elif self.foodType == "carn":
            if self.energy > carnStart:
                self.mateReady = True
            if self.energy < carnEnd or self.cooldown > 0:
                self.mateReady = False


    def findMate(self, width, height, herbCooldown, herbLoss, carnCooldown, carnLoss):
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
                self.successfulMate(closest_pom, herbCooldown, herbLoss, carnCooldown, carnLoss)
                closest_pom.gotMated(herbCooldown, herbLoss, carnCooldown, carnLoss)
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


    def successfulMate(self, mate, herbCooldown, herbLoss, carnCooldown, carnLoss):
        if self.foodType == "herb":
            self.energy -= herbLoss  # Reduce energy
            self.cooldown = herbCooldown
        if self.foodType == "carn":
            self.energy -= carnLoss
            self.cooldown = carnCooldown
        self.spawnBabies(mate)


    def gotMated(self, herbCooldown, herbLoss, carnCooldown, carnLoss):
        """
        when a different pompom mates with you, you still loose then energy and cooldown
        """
        if self.foodType == "herb":
            self.energy -= herbLoss  # Reduce energy
            self.cooldown = herbCooldown
        if self.foodType == "carn":
            self.energy -= carnLoss
            self.cooldown = carnCooldown


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
    
        return PomPom(x, y, self.grid, pattern, food,
                      self.herbStartEnergy, self.herbStartCooldown,
                      self.carnStartEnergy, self.carnStartCooldown)

