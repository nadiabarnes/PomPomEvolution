
from World import PomPomWorld
import pygame

"""
This will actually run a simulation
"""

def main():
    pygame.init()
    world = PomPomWorld(width=35, height=35, pomNumber = 40, bushNumber = 300, percentcarn=.1) 
    screen = pygame.display.set_mode((world.width * world.cell_size, world.height * world.cell_size))
    pygame.display.set_caption("PomPom Evolution")
    
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        world.update() 
        world.draw(screen)
        clock.tick(20)  #updates per second

    pygame.quit()

if __name__ == "__main__":
    main()

def initalize(width, height, pomNumber, bushNumber, percentcarn):
    pygame.init()
    world = PomPomWorld(width, height, pomNumber, bushNumber, percentcarn) 
    screen = pygame.display.set_mode((world.width * world.cell_size, world.height * world.cell_size))
    pygame.display.set_caption("PomPom Evolution")