from World import PomPomWorld
from Graphics import Visualize
import pygame

"""
This will actually run a simulation
"""

def main():
    pygame.init()

    width = 35
    height = 35
    cellsize = 20
    pomNumber = 50
    bushNumber = 300
    percentcarn = 0.1
    gameSpeed = 20

    PANEL_WIDTH = 200  # Width of the statistics panel
    SCREEN_WIDTH = 700 + PANEL_WIDTH  # Fixed screen width (Simulation + Panel)
    SCREEN_HEIGHT = 700  # Fixed screen height

    cellsize = min((SCREEN_WIDTH - PANEL_WIDTH) // width, SCREEN_HEIGHT // height)  # Ensure grid fits
    print(cellsize * width)

    world, screen, graphics = initialize(width, height, cellsize, pomNumber, 
                                         bushNumber, percentcarn, SCREEN_WIDTH, 
                                         SCREEN_HEIGHT)
    
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if world.update() == False:  # If simulation ends, restart
            world, screen, graphics = initialize(width, height, cellsize, pomNumber, 
                                                 bushNumber, percentcarn, SCREEN_WIDTH, 
                                                 SCREEN_HEIGHT)
        else:
            graphics.draw(screen, PANEL_WIDTH)  # Pass PANEL_WIDTH to use in draw method
            pygame.display.flip()
            clock.tick(gameSpeed)

    pygame.quit()



def initialize(width, height, cellsize, pomNumber, bushNumber, percentcarn, SCREEN_WIDTH, SCREEN_HEIGHT):
    pygame.init()
    world = PomPomWorld(width, height, cellsize, pomNumber, bushNumber, percentcarn) 
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Set the updated screen size
    graphics = Visualize(world)
    pygame.display.set_caption("PomPom Evolution")
    return world, screen, graphics


#-----------------------------------
if __name__ == "__main__":
    main()
