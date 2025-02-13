from Evo import Evolution
from Pom import PomPom
import random
import pygame


class PomPomWorld:
    """
    This will handle the board/world for PomPomEvolution
    """
    def __init__(self, width=20, height=20, cell_size=20):
        """
        board variables
        """
        self.width = width #grid width
        self.height = height #grid height
        self.cell_size = cell_size #pop up window size
        self.grid = [[None for _ in range(height)] for _ in range(width)] #creates an empty grid

        for _ in range(10):  #num of starting pompoms
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
            self.grid[x][y] = PomPom(x, y)

    def update(self):
        """
        move the pompoms one turn
        """
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y] and not self.grid[x][y].update():
                    self.grid[x][y] = None  # Remove dead PomPom

    def draw(self, screen):
        """
        Draw the grid and PomPoms
        """
        screen.fill((0, 0, 0))  # Clear screen with black
        font = pygame.font.Font(None, self.cell_size - 2)  #Create a font, size slightly smaller than cell
        text_color = (0, 0, 0)
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y]: #if there is a pompom in this spot
                    pompom = self.grid[x][y]
                    pygame.draw.rect(
                        screen,
                        (0, 255, 0),  # Green for living PomPoms
                        (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                    )
                    energy_text = font.render(str(pompom.energy), True, text_color)
                    text_rect = energy_text.get_rect(center=(
                        x * self.cell_size + self.cell_size // 2,
                        y * self.cell_size + self.cell_size // 2
                    ))
                    screen.blit(energy_text, text_rect)
        pygame.display.flip() #update the screen