from World import PomPomWorld
from Graphics import Visualize
import pygame

"""
This will actually run a simulation
"""

def main():
    pygame.init()

    #world traits
    width = 50
    height = 50
    pomNumber = 20
    bushNumber = 150
    percentcarn = 0.1
    gameSpeed = 20

    #pompom traits
    herbStartMate = 50 #nrg min to be horny
    herbEndMate = 30 #nrg max to be hungry
    carnStartMate = 120 
    carnEndMate = 50
    carnDamage = 40 #nrg carns can depelete per round
    herbEatEnergy = 10 #nrg gained from eating
    carnEatEnergy = 50
    carnEnergyCap = 300 #max carn nrg to be hungry
    herbMateCooldown = 10 #turn count until horny again
    herbMateLoss = 20 #nrg loss for mating
    carnMateCooldown = 40
    carnMateLoss = 20
    herbVisionSize = 3 #len one size of vision square. MUST BE ODD
    carnVisionSize = 7

    #TODO make bush cooldown modifiable
    
    PANEL_WIDTH = 200 
    SCREEN_WIDTH = 700 + PANEL_WIDTH  # Fixed screen width (Simulation + Panel)
    SCREEN_HEIGHT = 700  # Fixed screen height

    cellsize = min((SCREEN_WIDTH - PANEL_WIDTH) // width, SCREEN_HEIGHT // height)  # Ensure grid fits
    print(cellsize * width)

    world, screen, graphics = initialize(width, height, cellsize, pomNumber, 
                                         bushNumber, percentcarn, SCREEN_WIDTH, 
                                         SCREEN_HEIGHT,herbStartMate,herbEndMate,
                                         carnStartMate,carnEndMate,carnDamage,
                                         herbEatEnergy,carnEatEnergy,carnEnergyCap,
                                         herbMateCooldown,herbMateLoss,carnMateCooldown,
                                         carnMateLoss, herbVisionSize, carnVisionSize)
    
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if world.update() == False:  #If simulation ends, restart
            world, screen, graphics = initialize(width, height, cellsize, pomNumber, 
                                                 bushNumber, percentcarn, SCREEN_WIDTH, 
                                                 SCREEN_HEIGHT,herbStartMate,herbEndMate,
                                                 carnStartMate,carnEndMate,carnDamage,
                                                 herbEatEnergy,carnEatEnergy,carnEnergyCap,
                                                 herbMateCooldown,herbMateLoss,carnMateCooldown,
                                                 carnMateLoss, herbVisionSize, carnVisionSize)
        else:
            graphics.draw(screen, PANEL_WIDTH) 
            pygame.display.flip()
            clock.tick(gameSpeed)

    pygame.quit()



def initialize(width, height, cellsize, pomNumber, bushNumber, percentcarn, 
               SCREEN_WIDTH, SCREEN_HEIGHT,herbStartMate,herbEndMate,
               carnStartMate,carnEndMate,carnDamage,herbEatEnergy,carnEatEnergy,
               carnEnergyCap,herbMateCooldown,herbMateLoss,carnMateCooldown,carnMateLoss,
               herbVisionSize, carnVisionSize):
    """
    Begins a new simulation
    """
    pygame.init()
    world = PomPomWorld(width, height, cellsize, pomNumber, bushNumber, percentcarn,
                        herbStartMate,herbEndMate,carnStartMate,carnEndMate,
                        carnDamage,herbEatEnergy,carnEatEnergy,carnEnergyCap,
                        herbMateCooldown,herbMateLoss,carnMateCooldown,carnMateLoss,
                        herbVisionSize, carnVisionSize) 
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Set the updated screen size
    graphics = Visualize(world)
    pygame.display.set_caption("PomPom Evolution")
    return world, screen, graphics


#-----------------------------------
if __name__ == "__main__":
    main()
