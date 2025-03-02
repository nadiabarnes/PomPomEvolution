from World import PomPomWorld
from Graphics import Visualize
import pygame

"""
This will actually run a simulation
"""

def initialize(width, height, cellsize, pomNumber, bushNumber, percentcarn):
    pygame.init()
    world = PomPomWorld(width, height, cellsize, pomNumber, bushNumber, percentcarn) 
    screen = pygame.display.set_mode((world.width * world.cell_size, world.height * world.cell_size))
    graphics = Visualize(world)
    pygame.display.set_caption("PomPom Evolution")
    return world, screen, graphics  # Return both world and screen

def main():
    pygame.init()

    width = 35
    height = 35
    cellsize = 20
    pomNumber = 50
    bushNumber = 300
    percentcarn = 0.1

    world, screen, graphics = initialize(width, height, cellsize, pomNumber, 
                               bushNumber, percentcarn)  # Use the corrected function
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if world.update() == False: #if there aren't enough poms, restart the sim
            world, screen, graphics = initialize(width, height, cellsize, pomNumber, 
                                       bushNumber, percentcarn)  # Restart world and screen
        else:
            graphics.draw(screen)
            pygame.display.flip()  # Ensure the screen updates
            clock.tick(20)  # updates per second

    pygame.quit()

if __name__ == "__main__":
    main()
