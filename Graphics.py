from World import PomPomWorld
from Pom import *
import pygame
from config import values

class Visualize:
    """
    runs the graphics
    """
    def __init__(self, world):
        self.world = world

        self.directionAngles = {
            'N': 180,
            'E': -90,
            'S': 0,
            'W': 90,
            1: 0,    # spot = 1 is North?
            2: -90,  # East
            3: 180,  # South
            4: 90    # West
        }

        #Pom Scale
        pom_scale_factor = 2
        new_pom_size = int(world.cell_size * pom_scale_factor)
        self.pom_offset = (new_pom_size - world.cell_size) // 2

        #herb default
        self.herbivoreImage = pygame.image.load('assets/HerbavorePom.png').convert_alpha()
        self.herbivoreImage = pygame.transform.scale(self.herbivoreImage, (new_pom_size, new_pom_size))

        #herb horny
        self.herbivoreImageHorny = pygame.image.load('assets/HerbavorePomHorny.png').convert_alpha()
        self.herbivoreImageHorny = pygame.transform.scale(self.herbivoreImageHorny, (new_pom_size, new_pom_size))

        #herb Scared
        self.herbivoreImageScared = pygame.image.load('assets/herbavorePomScared.png').convert_alpha()
        self.herbivoreImageScared = pygame.transform.scale(self.herbivoreImageScared, (new_pom_size, new_pom_size))

        #carn default
        self.carnivoreImage = pygame.image.load('assets/CarnivorePom.png').convert_alpha()
        self.carnivoreImage = pygame.transform.scale(self.carnivoreImage, (new_pom_size, new_pom_size))

        #carn horny
        self.carnivoreImageHorny = pygame.image.load('assets/CarnivorePomHorny.png').convert_alpha()
        self.carnivoreImageHorny = pygame.transform.scale(self.carnivoreImageHorny, (new_pom_size, new_pom_size))

        #bush setup
        bush_scale_factor = 2
        new_bush_size = int(world.cell_size * bush_scale_factor)
        self.bush_offset = (new_bush_size - world.cell_size) // 2

        self.bushImage1 = pygame.image.load('assets/bush1.png').convert_alpha()
        self.bushImage1 = pygame.transform.scale(self.bushImage1, (new_bush_size, new_bush_size))
        self.bushImage2 = pygame.image.load('assets/bush2.png').convert_alpha()
        self.bushImage2 = pygame.transform.scale(self.bushImage2, (new_bush_size, new_bush_size))
        self.bushImage3 = pygame.image.load('assets/bush3.png').convert_alpha()
        self.bushImage3 = pygame.transform.scale(self.bushImage3, (new_bush_size, new_bush_size))
        self.bushDeadImage = pygame.image.load('assets/deadBush1.png').convert_alpha()
        self.bushDeadImage = pygame.transform.scale(self.bushDeadImage, (new_bush_size, new_bush_size))


    def draw(self, screen):
        """
        Updates the screen, including the simulation and statistics panel.
        """
        screen.fill((21, 60, 74))  #Background Color for Simulation
        font = pygame.font.Font(None, self.world.cell_size - 2)  #font for pompoms
        text_color = (0, 0, 0)  # black text

        # Draw the simulation area (left side)
        #self.drawVisableTiles(screen, self.world)
        self.drawBushes(screen, self.world)
        self.drawPomPomsFoodtype(screen, font, text_color, self.world)

        # Draw the right-side panel
        panel_x = self.world.width * self.world.cell_size  # Start drawing after the simulation grid
        pygame.draw.rect(screen, (50, 0, 20), (panel_x, 0, values.PANEL_WIDTH, screen.get_height()))  #black panel

        self.drawStatisticsPanel(screen, panel_x)

        pygame.display.flip()  #Update the screen


    def drawStatisticsPanel(self, screen, panel_x):
        """
        Displays statistics in the right panel.
        """
        padding = 10
        y_offset = 20  # Starting Y position
        font = pygame.font.Font("FontFileMontserrat.ttf", 16)

        # Titles
        title_text = font.render("Statistics", True, (255, 255, 255))
        screen.blit(title_text, (panel_x + padding, y_offset))
        y_offset += 40

        living_pompoms = 0
        carn_pompoms = 0
        herb_pompoms = 0
        random_poms = 0
        roomba_poms = 0
        wander_poms = 0

        for pompom in self.world.pompoms:
            if pompom.energy > 0:
                living_pompoms += 1
            if pompom.energy > 0 and pompom.foodType == "carn":
                carn_pompoms += 1
            if pompom.energy > 0 and pompom.foodType == "herb":
                herb_pompoms += 1
            if pompom.energy > 0 and pompom.movePattern == "random":
                random_poms += 1
            if pompom.energy > 0 and pompom.movePattern == "roomba":
                roomba_poms += 1
            if pompom.energy > 0 and pompom.movePattern == "wander":
                wander_poms += 1

        stats = [
            f"Epoch: {self.world.epoch}",
            f"PomPoms: {living_pompoms}",
            f"Carns: {carn_pompoms}",
            f"Herbs: {herb_pompoms}",
            f"Random Movers: {random_poms}",
            f"Roomba Movers: {roomba_poms}",
            f"Wander Movers: {wander_poms}"
        ]

        # Display each stat
        for stat in stats:
            text_surface = font.render(stat, True, (255, 255, 255))
            screen.blit(text_surface, (panel_x + padding, y_offset))
            y_offset += 30


    def drawBushes(self, screen, world):
        for bush in world.bushes:  # Iterate over the bush list instead of scanning the entire grid
            draw_x = bush.rect.x * world.cell_size - self.bush_offset
            draw_y = bush.rect.y * world.cell_size - self.bush_offset
            if bush.cooldown == 0:  # Only draw if active
                if bush.version == 1:
                    screen.blit(self.bushImage1, (draw_x, draw_y))
                elif bush.version == 2:
                    screen.blit(self.bushImage2, (draw_x, draw_y))
                elif bush.version == 3:
                    screen.blit(self.bushImage3, (draw_x, draw_y))
            else:
                screen.blit(self.bushDeadImage, (draw_x, draw_y))


    def drawPomPomsFoodtype(self, screen, font, text_color, world):
            for x in range(world.width):
                for y in range(world.height):
                    if world.grid[x][y]: #if there is a pompom in this spot
                        pompom = world.grid[x][y]
                        draw_x = pompom.rect.x * world.cell_size - self.bush_offset
                        draw_y = pompom.rect.y * world.cell_size - self.bush_offset
                        if pompom.foodType == "herb":
                            if pompom.flee > 0:
                                print("flee")
                                baseImage = self.herbivoreImageScared
                                rotatedImage = self.rotatePomImage(pompom, baseImage)
                                screen.blit(rotatedImage, (draw_x, draw_y))
                            elif pompom.mateReady:
                                baseImage = self.herbivoreImageHorny
                                rotatedImage = self.rotatePomImage(pompom, baseImage)
                                screen.blit(rotatedImage, (draw_x, draw_y))
                            else:
                                baseImage = self.herbivoreImage
                                rotatedImage = self.rotatePomImage(pompom, baseImage)
                                screen.blit(rotatedImage, (draw_x, draw_y))
                        elif pompom.foodType == "carn":
                            if pompom.mateReady:
                                baseImage = self.carnivoreImageHorny
                                rotatedImage = self.rotatePomImage(pompom, baseImage)
                                screen.blit(rotatedImage, (draw_x, draw_y))
                            else:
                                baseImage = self.carnivoreImage
                                rotatedImage = self.rotatePomImage(pompom, baseImage)
                                screen.blit(rotatedImage, (draw_x, draw_y))
                        


    def rotatePomImage(self, pompom, baseimage):
        angle = self.directionAngles.get(pompom.facing, 0)  # Get rotation angle
        return pygame.transform.rotate(baseimage, angle)


    def drawVisableTiles(self, screen, world):
            for x in range(world.width):
                for y in range(world.height):
                    if world.grid[x][y] and isinstance(world.grid[x][y], PomPom):  # Ensure it's a PomPom
                        pompom = world.grid[x][y]
                        if pompom.energy <= 0:
                            return
                        pygame.draw.rect(
                            screen,
                            (255, 255, 255),
                            pygame.Rect(
                                pompom.vis.x * world.cell_size,
                                pompom.vis.y * world.cell_size,
                                pompom.vis.width * world.cell_size,
                                pompom.vis.height * world.cell_size
                            ),
                            2
                        )
    
    def drawPomPomsFoodtypeNew(self, screen, font, text_color, world):
        for x in range(world.width):
            for y in range(world.height):
                pompom = world.grid[x][y]
                if not pompom or pompom.energy <= 0:
                    continue  # Skip dead pompoms or empty cells

                # Choose the image by food type
                if pompom.foodType == "herb":
                    baseImage = self.herbivoreImage
                elif pompom.foodType == "omnivore":
                    baseImage = self.omnivoreImage
                elif pompom.foodType == "carn":
                    baseImage = self.carnivoreImage
                else:
                    continue  # Skip unknown food types

                # Get the angle to rotate based on facing/spot
                facing = getattr(pompom, 'facing', 'N')  # Or use spot if you prefer
                angle = self.directionAngles.get(facing, 0)

                rotatedImage = pygame.transform.rotate(baseImage, angle)

                # Draw the rotated image
                screen.blit(rotatedImage, (x * world.cell_size, y * world.cell_size))

                # Overlay energy text
                energy_text = font.render(str(pompom.energy), True, text_color)
                text_rect = energy_text.get_rect(center=(
                    x * world.cell_size + world.cell_size // 2,
                    y * world.cell_size + world.cell_size // 2
                ))
                screen.blit(energy_text, text_rect)
