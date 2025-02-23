from Evo import Evolution
from Pom import PomPom
from Food import Bush
import random
import pygame


class PomPomWorld:
    """
    This will handle the board/world for PomPomEvolution
    """
    def __init__(self, width=20, height=20, cell_size=20, pomNumber = 2, bushNumber = 20):
        """
        board variables
        """
        self.width = width #grid width
        self.height = height #grid height
        self.cell_size = cell_size #pop up window size
        self.grid = [[None for _ in range(height)] for _ in range(width)] #creates an empty grid
        self.bushes = []
        self.pompoms = []

        #spawn in pompoms
        for _ in range(pomNumber):  #rough num of starting pompoms
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
            if not self.grid[x][y]:
                self.grid[x][y] = PomPom(x, y, self.grid)
                self.pompoms.append(self.grid[x][y])

        #spawn in bushes
        for _ in range(bushNumber):  #rough Starting num bushes
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
            if not self.grid[x][y]:
                self.grid[x][y] = Bush(x, y)
                self.bushes.append(self.grid[x][y])


    def update(self):
        """
        The most important method.
        """
        self.updateFood()
        self.updatePomPoms()


    def updateFood(self):
        for bush in self.bushes:
            bush.update()


    def updatePomPoms(self):
        #TODO add safeguard from pompoms going onto same tile
        #TODO this logic should be in the pom file
        new_grid = [[None for _ in range(self.height)] for _ in range(self.width)]
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y] and isinstance(self.grid[x][y], PomPom):  # If there's a PomPom in this position
                    pompom = self.grid[x][y]
                    pompom.updateAdjacentTiles(self.width, self.height)
                    pompom.findMate(self.width, self.height, self.pompoms)
                    pompom.seekBushes(self.width, self.height, self.bushes)  # Move the PomPom
                    pompom.vision(5)
                    #pompom.randomMove(self.width,self.height) #move randomly
                    # Check if the PomPom lands on a Bush
                    for bush in self.bushes:
                        if pompom.rect.x == bush.rect.x and pompom.rect.y == bush.rect.y and bush.cooldown == 0:
                            pompom.eat()  # Gain energy from eating
                            bush.eaten()  # Put bush on cooldown
                    # PomPom loses energy per turn
                    if not pompom.update():  # If it dies, don't add to the new grid
                        continue
                    # Place PomPom in new grid
                    new_grid[pompom.rect.x][pompom.rect.y] = pompom
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

        self.drawVisableTiles(screen)
        self.drawBushes(screen)
        self.drawPomPomsMating(screen,font,text_color)
        
        pygame.display.flip() #update the screen

    
    def drawBushes(self, screen):
        for bush in self.bushes:
            if bush.cooldown == 0:  # Only draw if active
                pygame.draw.rect(
                    screen,
                    (65, 255, 110),  # Brown for Bushes
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
                if self.grid[x][y]:  # If there is a PomPom in this spot
                    pompom = self.grid[x][y]
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



    