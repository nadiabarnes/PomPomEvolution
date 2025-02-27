2/26/2024

Hello! This file explains the current behavior of the simulation.
This will allow for easy comparison between versions of the sim,
and help me track progress!
-Nadia Barnes

WORLD LOGIC:
The world starts with a grid of size width x height,
and populates with a specified number of bushes and pompoms.
You can also specify what % of the spawned pompoms are carns/herbs.

The world is turn based, so every turn the pompoms calculate their next
move and update themselves.

When the world initializes it populates with bushes and pompoms.
They are placed in the grid with basic logic - it selects a random
spot, and if that spot isn't populated, places the bush/pompom.

When the world starts, the poms start with random traits.


BUSH LOGIC:
Really simple. When a pom "eats" one, they gain a cooldown of 10.
They only can be eaten/drawn when they have a cooldown of 0.


POMPOM LOGIC:
Simplest way is describe their global variables and update method.

----------------------------------------------------------------------------
 def __init__(self, x, y, grid, movePattern=None, foodType=None):
        self.grid = grid
 1      self.energy = 20
        directions = ['N','E','S','W']
 2      self.facing = random.choice(directions)
        self.vis = pygame.Rect(x, y, 3, 3)
 3      self.visableTiles = []
        self.rect = pygame.Rect(x, y, 1, 1)
        if movePattern == None:
 4          movePatterns = ["random","roomba"]
            self.movePattern = random.choice(movePatterns)
        else:
            self.movePattern = movePattern
        if foodType == None:
 5          foodTypes = ["herb","carn"]
            self.foodType = random.choice(foodTypes)
        else:
            self.foodType = foodType
 6      self.mateReady = False
 7      self.cooldown = 20
        self.adjacentTiles = [None for _ in range(9)]
        self.updateAdjacentTiles(len(self.grid), len(self.grid))
        self.vision(3)
        self.visionTilesUpdate(3)
        

 8  def update(self, grid):
        self.grid = grid
        self.energy -= 1
        self.cooldown -= 1
        if self.energy <= 0:
            return self.grid
    
        self.isMateReady()
        self.findMate(len(self.grid), len(self.grid)) 
        self.findFood(len(self.grid), len(self.grid))
        self.updateAdjacentTiles(len(self.grid), len(self.grid))
        self.vision(5)
        self.visionTilesUpdate(5)

        return self.grid
-------------------------------------------------------------------

1) The pompoms start with 20 energy. This decreases by 1 every round
2) They start facing a random direction, N E S or W
3) The poms can see a square in the direction they face, the length of one side can be changed to any odd num
4) The poms have a generic move pattern that they default too when they can't see anything interesting.
    Random moves them to a random adjacent tile, roomba moves them straight until they run into something.
5) The poms are either an herb or a carn. They can only mate with their same foodType.
    Herbs eat bushes, and gain 10 energy for each bush.
    Carns eat herbs, and gain 50 energy for each herb.
6) mateReady happens when a pom has enough surplus energy, and lasts until they mate or get low enough on energy.
    Herbs get horny at 50 energy, and get hungry at 30.
    Carns get horny at 120 energy, and get hungry at 70.
7) poms can't breed if their cooldown is above 0. They are born with a cooldown of 20, so they can't
    breed for a bit. After a mating successfully, herbs gain a cooldown of 20 while carns gain 50.
8) Generally the poms look for mates if they are horny and food if they are hungry (or in cooldown).
    If they don't see what they are looking for, they do their generic move pattern.
    After they move, they update what they can see and the tiles around then.
    If their energy is more than 120, they do their generic move and don't try to eat.
    ^This tries to prevent greedy carns from eradicating the herbs while they are in cooldown.


CURRENT BEHAVIOR
All of the integer values above can be changed easily. Currently what happens
is there is an early on herb explosion, then a carn explosion which wipes
out every herb, then the carns die off from lack of food. 

potential balancing:
1) Have the carns hunt eachother for food, not just herbs
2) Herbs run away from carns
3) Small chance that a baby has different foodtype from parents
    This might help with total extinction

NEXT TO ADD:
Omnivores that only hunt when they are low energy - easy
Balancing changes above - moderate
Spawn poms more intentionally - difficult