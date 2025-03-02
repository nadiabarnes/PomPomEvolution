from World import PomPomWorld
from Pom import PomPom
import pygame

class Visualize:
    """
    runs the graphics
    """
    def __init__(self, world):
        self.world = world

    def drawOLD(self, screen):
        """
        updates the screen
        """
        screen.fill((21, 60, 74))  #Background Color
        font = pygame.font.Font(None, self.world.cell_size - 2)  #Create a font, size slightly smaller than cell
        text_color = (0, 0, 0)

        #self.drawVisableTiles(screen)
        self.drawBushes(screen, self.world)
        self.drawPomPomsFoodtype(screen,font,text_color, self.world)
        self.drawEpochCount(screen, font, self.world)
        self.drawPomPomFoodTypeMetrics(screen, font, self.world)

        pygame.display.flip() #update the screen
    

    def draw(self, screen, panel_width):
        """
        Updates the screen, including the simulation and statistics panel.
        """
        screen.fill((21, 60, 74))  #Background Color for Simulation
        font = pygame.font.Font(None, self.world.cell_size - 2)  # Font for statistics
        text_color = (0, 0, 0)  # black text

        # Draw the simulation area (left side)
        self.drawBushes(screen, self.world)
        self.drawPomPomsFoodtype(screen, font, text_color, self.world)
        
        # Draw the right-side panel
        panel_x = self.world.width * self.world.cell_size  # Start drawing after the simulation grid
        pygame.draw.rect(screen, (50, 0, 20), (panel_x, 0, panel_width, screen.get_height()))  #black panel

        self.drawStatisticsPanel(screen, panel_x)

        pygame.display.flip()  # Update the screen


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

        # Display PomPom Counts
        living_pompoms = len([pompom for pompom in self.world.pompoms if pompom.energy > 0])
        carn_pompoms = len([pompom for pompom in self.world.pompoms if pompom.energy > 0 and pompom.foodType == "carn"])
        herb_pompoms = len([pompom for pompom in self.world.pompoms if pompom.energy > 0 and pompom.foodType == "herb"])
        random_poms = len([pompom for pompom in self.world.pompoms if pompom.energy > 0 and pompom.movePattern == "random"])
        roomba_poms = len([pompom for pompom in self.world.pompoms if pompom.energy > 0 and pompom.movePattern == "roomba"])
        wander_poms = len([pompom for pompom in self.world.pompoms if pompom.energy > 0 and pompom.movePattern == "wander"])

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
            if bush.cooldown == 0:  # Only draw if active
                pygame.draw.rect(
                    screen,
                    (66, 144, 88),  # Green for active bushes
                    (bush.rect.x * world.cell_size, bush.rect.y * world.cell_size, world.cell_size, world.cell_size)
                )


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

                        