from Pom import PomPom
from Food import Bush
import random
import pygame


class PomPomWorld:
    """
    This will handle the board/world for PomPomEvolution
    """
    def __init__(self, width=20, height=20, cell_size=20, pomNumber=2, bushNumber=20, percentcarn=.2):
        """
        Board variables
        """
        self.width = width  # Grid width
        self.height = height  # Grid height
        self.cell_size = cell_size  # Pop-up window size
        self.grid = [[None for _ in range(height)] for _ in range(width)]  # Creates an empty grid
        self.bushes = []
        self.pompoms = [] 

        # Define probabilities for food types
        foodTypeWeights = {"herb": 1 - percentcarn, "carn": percentcarn}

        #TODO ensure that the pom/bush is always placed

        # Spawn in PomPoms
        for _ in range(pomNumber):  # Rough number of starting PomPoms
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
            if not self.grid[x][y]:
                food = random.choices(list(foodTypeWeights.keys()), weights=foodTypeWeights.values())[0]
                pattern = random.choice(["random", "roomba"])
                newPom = PomPom(x, y, self.grid, pattern, food)

                self.grid[x][y] = newPom
                self.pompoms.append(self.grid[x][y])

        # Spawn in bushes
        for _ in range(bushNumber):  # Rough starting number of bushes
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
            if not self.grid[x][y]:
                self.grid[x][y] = Bush(x, y, self.grid)
                self.bushes.append(self.grid[x][y])


    def update(self):
        """
        The most important method.
        """
        self.updateFood()
        self.updatePomPoms()


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

#-------------------------------------------------------------------------------


    def draw(self, screen):
        """
        Draw the grid and PomPoms
        """
        screen.fill((21, 60, 74))  # Clear screen with black
        font = pygame.font.Font(None, self.cell_size - 2)  #Create a font, size slightly smaller than cell
        text_color = (0, 0, 0)

        #self.drawVisableTiles(screen)
        self.drawBushes(screen)
        self.drawPomPomsFoodtype(screen,font,text_color)
        self.drawLivingPomPomCount(screen, font)
        
        pygame.display.flip() #update the screen
    

    def drawLivingPomPomCount(self, screen, font):
        """
        Draws the number of living PomPoms in the top-left corner of the screen.
        """
        # Count the number of living PomPoms
        living_pompoms = len([pompom for pompom in self.pompoms if pompom.energy > 0])

        # Create the text to display the count
        count_text = font.render(f"Living PomPoms: {living_pompoms}", True, (255, 255, 255))

        # Define the position and size for the box
        box_width = count_text.get_width() + 10  # Add padding
        box_height = count_text.get_height() + 10
        box_rect = pygame.Rect(10, 10, box_width, box_height)  # Box position at (10, 10) in the corner

        # Draw the box (background)
        pygame.draw.rect(screen, (0, 0, 0), box_rect)  # Black background for the box
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)  # White border for the box

        # Draw the text inside the box
        screen.blit(count_text, (box_rect.x + 5, box_rect.y + 5))  # Position the text inside the box



    def drawBushes(self, screen):
        for bush in self.bushes:  # Iterate over the bush list instead of scanning the entire grid
            if bush.cooldown == 0:  # Only draw if active
                pygame.draw.rect(
                    screen,
                    (65, 255, 110),  # Green for active bushes
                    (bush.rect.x * self.cell_size, bush.rect.y * self.cell_size, self.cell_size, self.cell_size)
                )


    def drawPomPomsMating(self, screen, font, text_color):
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y]: #if there is a pompom in this spot
                    pompom = self.grid[x][y]
                    if pompom.mateReady == True:
                        pygame.draw.rect(
                            screen,
                            (212, 30, 60),  # Green for living PomPoms
                            (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                        )
                    elif pompom.mateReady == False:
                        pygame.draw.rect(
                            screen,
                            (16, 144, 144),  # Green for living PomPoms
                            (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                        )
                    energy_text = font.render(str(pompom.energy), True, text_color)
                    text_rect = energy_text.get_rect(center=(
                        x * self.cell_size + self.cell_size // 2,
                        y * self.cell_size + self.cell_size // 2
                    ))
                    screen.blit(energy_text, text_rect)
    

    def drawPomPomsFoodtype(self, screen, font, text_color):
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y]: #if there is a pompom in this spot
                    pompom = self.grid[x][y]
                    if pompom.foodType == "herb":
                        pygame.draw.rect(
                            screen,
                            (66, 144, 88),  #Green for herb
                            (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                        )
                    elif pompom.foodType == "omnivore":
                        pygame.draw.rect(
                            screen,
                            (255, 184, 74),  #Yellow for omivore
                            (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                        )
                    elif pompom.foodType == "carn":
                        pygame.draw.rect(
                            screen,
                            (212, 30, 60),  #Red for carn
                            (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                        )
                    energy_text = font.render(str(pompom.energy), True, text_color)
                    text_rect = energy_text.get_rect(center=(
                        x * self.cell_size + self.cell_size // 2,
                        y * self.cell_size + self.cell_size // 2
                    ))
                    screen.blit(energy_text, text_rect)


    def drawPomPoms(self, screen, font, text_color):
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y]: #if there is a pompom in this spot
                    pompom = self.grid[x][y]
                    pygame.draw.rect(
                        screen,
                        (212, 30, 60),  # Green for living PomPoms
                        (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                    )
                    energy_text = font.render(str(pompom.energy), True, text_color)
                    text_rect = energy_text.get_rect(center=(
                        x * self.cell_size + self.cell_size // 2,
                        y * self.cell_size + self.cell_size // 2
                    ))
                    screen.blit(energy_text, text_rect)
    

    
    def drawVisableTiles(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y] and isinstance(self.grid[x][y], PomPom):  # Ensure it's a PomPom
                    pompom = self.grid[x][y]
                    if pompom.energy <= 0:
                        return
                    pygame.draw.rect(
                        screen,
                        (255, 255, 255),
                        pygame.Rect(
                            pompom.vis.x * self.cell_size,
                            pompom.vis.y * self.cell_size,
                            pompom.vis.width * self.cell_size,
                            pompom.vis.height * self.cell_size
                        ),
                        2
                    )




    