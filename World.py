from Evo import Evolution
from Pom import PomPom
import random
import pygame


class PomPomWorld:
    """
    This will handle the board/world for PomPomEvolution
    """
    def __init__(self, width=20, height=20, cell_size=20):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = [[None for _ in range(height)] for _ in range(width)]

        # Initialize random PomPoms
        for _ in range(10):  # Start with 10 PomPoms
            x, y = random.randint(0, width - 1), random.randint(0, height - 1)
            self.grid[x][y] = PomPom(x, y)

    def update(self):
        """
        Update each PomPom in the world.
        """
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y] and not self.grid[x][y].update():
                    self.grid[x][y] = None  # Remove dead PomPom

    def draw(self, screen):
        """
        Draw the grid and PomPoms.
        """
        screen.fill((0, 0, 0))  # Clear screen with black

        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x][y]:
                    pygame.draw.rect(
                        screen,
                        (0, 255, 0),  # Green for living PomPoms
                        (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                    )
        pygame.display.flip()