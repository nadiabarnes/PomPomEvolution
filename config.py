

class values():
    """
    change values for the simulation.
    saves me time and energy.
    """

    #world traits
    WIDTH = 70
    HEIGHT = 70
    POM_NUMBER = 50
    BUSH_NUMBER = 200
    PERCENT_CARN = 0.1
    GAME_SPEED = 20

    #pompom traits
    HERB_START_MATE = 50 #nrg min to be horny
    HERB_END_MATE = 30 #nrg max to be hungry
    CARN_START_MATE = 120
    CARN_END_MATE = 70
    CARN_DAMAGE = 40 #nrg carns can depelete per round
    HERB_EAT_ENERGY = 10 #nrg gained from eating
    CARN_EAT_ENERGY = 50
    CARN_ENERGY_CAP = 200 #max carn nrg to be hungry
    HERB_MATE_COOLDOWN = 10 #turn count until horny again
    HERB_MATE_LOSS = 15 #nrg loss for mating
    CARN_MATE_COOLDOWN = 50
    CARN_MATE_LOSS = 50
    HERB_VISION_SIZE = 3 #len one size of vision square. MUST BE ODD
    CARN_VISION_SIZE = 7 #MUST BE ODD
    HERB_START_ENERGY = 20
    HERB_START_COOLDOWN = 10
    CARN_START_ENERGY = 200
    CARN_START_COOLDOWN = 200
    FLEE_TIME = 10

    PANEL_WIDTH = 200 
    SCREEN_WIDTH = 700 + PANEL_WIDTH  # Fixed screen width (Simulation + Panel)
    SCREEN_HEIGHT = 700  # Fixed screen height

    CELLSIZE = min((SCREEN_WIDTH - PANEL_WIDTH) // WIDTH, SCREEN_HEIGHT // HEIGHT)  # Ensure grid fits
