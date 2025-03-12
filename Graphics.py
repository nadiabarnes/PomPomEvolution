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
            'N': 0,
            'E': -90,
            'S': 180,
            'W': 90,
            1: 0,    # spot = 1 is North?
            2: -90,  # East
            3: 180,  # South
            4: 90    # West
        }

        #self.herbivoreImage = pygame.image.load('assets/herbivore.png').convert_alpha()
        #self.carnivoreImage = pygame.image.load('assets/carnivore.png').convert_alpha()
        #self.omnivoreImage = pygame.image.load('assets/omnivore.png').convert_alpha()

        # Scale images to fit the cell size
        #self.herbivoreImage = pygame.transform.scale(self.herbivoreImage, (world.cell_size, world.cell_size))
        #self.carnivoreImage = pygame.transform.scale(self.carnivoreImage, (world.cell_size, world.cell_size))
        #self.omnivoreImage = pygame.transform.scale(self.omnivoreImage, (world.cell_size, world.cell_size))

        #bush setup
        bush_scale_factor = 1.5
        new_bush_size = int(world.cell_size * bush_scale_factor)
        self.bush_offset = (new_bush_size - world.cell_size) // 2

        self.bushImage = pygame.image.load('assets/bushLive.png').convert_alpha()
        self.bushImage = pygame.transform.scale(self.bushImage, (new_bush_size, new_bush_size))
        self.bushDeadImage = pygame.image.load('assets/bushDead.png').convert_alpha()
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
                screen.blit(self.bushImage, (draw_x, draw_y))
            else:
                screen.blit(self.bushDeadImage, (draw_x, draw_y))



    def drawPomPomsMating(self, screen, font, text_color, world):
            for x in range(world.width):
                for y in range(world.height):
                    if world.grid[x][y]: #if there is a pompom in this spot
                        pompom = world.grid[x][y]
                        if pompom.mateReady == True:
                            pygame.draw.rect(
                                screen,
                                (212, 30, 60),  # Green for living PomPoms
                                (x * world.cell_size, y * world.cell_size, world.cell_size, world.cell_size)
                            )
                        elif pompom.mateReady == False:
                            pygame.draw.rect(
                                screen,
                                (16, 144, 144),  # Green for living PomPoms
                                (x * world.cell_size, y * world.cell_size, world.cell_size, world.cell_size)
                            )
                        energy_text = font.render(str(pompom.energy), True, text_color)
                        text_rect = energy_text.get_rect(center=(
                            x * world.cell_size + world.cell_size // 2,
                            y * world.cell_size + world.cell_size // 2
                        ))
                        screen.blit(energy_text, text_rect)
        

    def drawPomPomsFoodtype(self, screen, font, text_color, world):
            for x in range(world.width):
                for y in range(world.height):
                    if world.grid[x][y]: #if there is a pompom in this spot
                        pompom = world.grid[x][y]
                        if pompom.foodType == "herb":
                            pygame.draw.rect(
                                screen,
                                (65, 255, 110),  #Green for herb
                                (x * world.cell_size, y * world.cell_size, world.cell_size, world.cell_size)
                            )
                        elif pompom.foodType == "omnivore":
                            pygame.draw.rect(
                                screen,
                                (255, 184, 74),  #Yellow for omivore
                                (x * world.cell_size, y * world.cell_size, world.cell_size, world.cell_size)
                            )
                        elif pompom.foodType == "carn":
                            pygame.draw.rect(
                                screen,
                                (212, 30, 60),  #Red for carn
                                (x * world.cell_size, y * world.cell_size, world.cell_size, world.cell_size)
                            )
                        energy_text = font.render(str(pompom.energy), True, text_color)
                        text_rect = energy_text.get_rect(center=(
                            x * world.cell_size + world.cell_size // 2,
                            y * world.cell_size + world.cell_size // 2
                        ))
                        screen.blit(energy_text, text_rect)


    def drawPomPomsMovePattern(self, screen, font, text_color, world):
        for x in range(world.width):
            for y in range(world.height):
                if world.grid[x][y]: #if there is a pompom in this spot
                    pompom = world.grid[x][y]
                    if pompom.movePattern == "random":
                        pygame.draw.rect(
                            screen,
                            (65, 255, 110),  #Green for herb
                            (x * world.cell_size, y * world.cell_size, world.cell_size, world.cell_size)
                        )
                    elif pompom.movePattern == "roomba":
                        pygame.draw.rect(
                            screen,
                            (255, 184, 74),  #Yellow for omivore
                            (x * world.cell_size, y * world.cell_size, world.cell_size, world.cell_size)
                        )
                    elif pompom.movePattern == "wander":
                        pygame.draw.rect(
                            screen,
                            (212, 30, 60),  #Red for carn
                            (x * world.cell_size, y * world.cell_size, world.cell_size, world.cell_size)
                        )
                    energy_text = font.render(str(pompom.energy), True, text_color)
                    text_rect = energy_text.get_rect(center=(
                        x * world.cell_size + world.cell_size // 2,
                        y * world.cell_size + world.cell_size // 2
                    ))
                    screen.blit(energy_text, text_rect)


    def drawPomPoms(self, screen, font, text_color, world):
        for x in range(world.width):
            for y in range(world.height):
                if world.grid[x][y]: #if there is a pompom in this spot
                    pompom = world.grid[x][y]
                    pygame.draw.rect(
                        screen,
                        (212, 30, 60),  # Green for living PomPoms
                        (x * world.cell_size, y * world.cell_size, world.cell_size, world.cell_size)
                    )
                    energy_text = font.render(str(pompom.energy), True, text_color)
                    text_rect = energy_text.get_rect(center=(
                        x * world.cell_size + world.cell_size // 2,
                        y * world.cell_size + world.cell_size // 2
                    ))
                    screen.blit(energy_text, text_rect)


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
