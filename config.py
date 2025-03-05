

class values():
    """
    change values for the simulation.
    saves me time and energy.
    """

    #world traits
    WIDTH = 70
    HEIGHT = 70
    POM_DENSITY = .005 #percent of tiles that will be poms
    BUSH_DENSITY = .05 #percent of tiles that will be bushes
    PERCENT_CARN = 0.2
    GAME_SPEED = 40

    #pompom traits
    HERB_START_MATE = 600 #nrg min to be horny
    HERB_END_MATE = 400 #nrg max to be hungry
    CARN_START_MATE = 1500
    CARN_END_MATE = 1000
    CARN_DAMAGE = 100 #nrg carns can depelete per round
    HERB_EAT_ENERGY = 50 #nrg gained from eating
    CARN_EAT_ENERGY = 500
    CARN_ENERGY_CAP = 2000 #max carn nrg to be hungry
    HERB_MATE_COOLDOWN = 10 #turn count until horny again
    HERB_MATE_LOSS = 100 #nrg loss for mating
    CARN_MATE_COOLDOWN = 50
    CARN_MATE_LOSS = 300
    HERB_VISION_SIZE = 3 #len one size of vision square. MUST BE ODD
    CARN_VISION_SIZE = 7 #MUST BE ODD
    HERB_START_ENERGY= 300
    HERB_START_COOLDOWN= 10
    CARN_START_ENERGY= 1000
    CARN_START_COOLDOWN = 200
    FLEE_TIME = 40
    BUSH_COOLDOWN = 100

    #PC
    PANEL_WIDTH = 200 
    SCREEN_WIDTH = 1000 + PANEL_WIDTH 
    SCREEN_HEIGHT = 1000  # Fixed screen height

    #laptop
    #PANEL_WIDTH = 200 
    #SCREEN_WIDTH = 700 + PANEL_WIDTH 
    #SCREEN_HEIGHT = 700  # Fixed screen height

    CELLSIZE = min((SCREEN_WIDTH - PANEL_WIDTH) // WIDTH, SCREEN_HEIGHT // HEIGHT)  # Ensure grid fits
