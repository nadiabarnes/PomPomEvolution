
from World import PomPomWorld
import pygame

"""
This will actually run a simulation
"""

def main():
    pygame.init()
    world = PomPomWorld(width=40, height=40, pomNumber = 30, bushNumber = 300) 
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
