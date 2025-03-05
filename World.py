from Pom import PomPom
from Food import Bush
import random
import pygame
from config import values


class PomPomWorld:
    """
    This will handle the board/world for PomPomEvolution
    """
    def __init__(self):
        """
        Board variables
        """
        self.width = values.WIDTH  # Grid width
        self.height = values.HEIGHT  # Grid height
        self.cell_size = values.CELLSIZE  # Pop-up window size
        self.grid = [[None for _ in range(values.HEIGHT)] for _ in range(values.WIDTH)]  # Creates an empty grid
        self.bushes = []
        self.pompoms = [] 
        self.epoch = 0

        # Define probabilities for food types
        foodTypeWeights = {"herb": 1 - values.PERCENT_CARN, "carn": values.PERCENT_CARN}

        #spawn in pompoms
        for x in range(self.width):
                for y in range(self.height):
                    temp = random.random()
                    if temp < values.POM_DENSITY:
                        food = random.choices(list(foodTypeWeights.keys()), weights=foodTypeWeights.values())[0]
                        pattern = random.choice(["random", "roomba", "wander"])
                        newPom = PomPom(x, y, self.grid, pattern, food)
                        self.grid[x][y] = newPom
                        self.pompoms.append(self.grid[x][y])

        # Spawn in bushes
        for x in range(self.width):
                for y in range(self.height):
                    temp = random.random()
                    if temp < values.BUSH_DENSITY:
                        self.grid[x][y] = Bush(x, y, self.grid)
                        self.bushes.append(self.grid[x][y])


    def update(self):
        """
        The most important method.
        """
        self.epoch += 1
        self.updateFood()
        self.updatePomPoms()

        #active is true if there are living poms
        #and at least two of them are carnivores
        active = False
        carnCount = 0
        for pom in self.pompoms:
            if pom.energy > 0:
                active = True
            if pom.foodType == "carn":
                carnCount += 1
        if carnCount >= 2:
            active = True
        else: active = False
        return active


    def updateFood(self):
        new_grid = self.grid  # Keep the current grid reference
        for bush in self.bushes:
            bush.update(new_grid)  # Update bush state
            new_grid[bush.rect.x][bush.rect.y] = bush  # Ensure bushes persist


    def updatePomPoms(self):
        # Temporary new grid to hold PomPoms
        new_grid = [[None for _ in range(self.height)] for _ in range(self.width)]
        new_pompoms = []  # To store PomPoms that are still alive

        for pompom in self.pompoms:
            pompom.update(self.grid)  # Update PomPom behavior

            if pompom.energy <= 0:  # If it dies, don't add to the new grid
                continue  # Skip dead PomPom

            # Place the alive PomPom in the new grid
            new_grid[pompom.rect.x][pompom.rect.y] = pompom

            # Add to new_pompoms list
            new_pompoms.append(pompom)

            # Add baby PomPoms to the lists if needed
            for x in range(self.width):
                for y in range(self.height):
                    if pompom.grid[x][y]:  # If there's a PomPom in this spot
                        pom = self.grid[x][y]
                        if isinstance(pom, PomPom) and pom not in self.pompoms:
                            self.pompoms.append(pom)

        # Replace the old list of PomPoms with the new list (excluding dead ones)
        self.pompoms = new_pompoms

        # Update the grid with the new positions
        self.grid = new_grid