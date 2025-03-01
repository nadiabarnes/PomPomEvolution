from World import PomPomWorld
import pygame

"""
This will actually run a simulation
"""

def initialize(width, height, pomNumber, bushNumber, percentcarn):
    pygame.init()
    world = PomPomWorld(width, height, 20, pomNumber, bushNumber, percentcarn) 
    screen = pygame.display.set_mode((world.width * world.cell_size, world.height * world.cell_size))
    pygame.display.set_caption("PomPom Evolution")
    return world, screen  # Return both world and screen

def main():
    pygame.init()
    world, screen = initialize(width=35, height=35, pomNumber=10, bushNumber=300, percentcarn=0.5)  # Use the corrected function
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if world.update() == False:
            world, screen = initialize(width=35, height=35, pomNumber=10, bushNumber=300, percentcarn=0.5)  # Restart world and screen
        else:
            world.draw(screen)
            pygame.display.flip()  # Ensure the screen updates
            clock.tick(20)  # updates per second

    pygame.quit()

if __name__ == "__main__":
    main()
