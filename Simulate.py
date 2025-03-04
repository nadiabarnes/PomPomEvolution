from World import PomPomWorld
from Graphics import Visualize
import pygame
from config import values

"""
This will actually run a simulation
"""

def main():
    pygame.init()
    #TODO make bush cooldown modifiable

    world, screen, graphics = initialize()
    
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if world.update() == False:  #If simulation ends, restart
            world, screen, graphics = initialize()
        else:
            graphics.draw(screen) 
            pygame.display.flip()
            clock.tick(values.GAME_SPEED)

    pygame.quit()



def initialize():
    """
    Begins a new simulation
    """
    pygame.init()
    world = PomPomWorld() 
    screen = pygame.display.set_mode((values.SCREEN_WIDTH, values.SCREEN_HEIGHT))  # Set the updated screen size
    graphics = Visualize(world)
    pygame.display.set_caption("PomPom Evolution")
    return world, screen, graphics


#-----------------------------------
if __name__ == "__main__":
    main()
