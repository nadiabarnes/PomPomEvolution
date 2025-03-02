from World import PomPomWorld
from Pom import PomPom
import pygame

class Visualize:
    """
    runs the graphics
    """
    def __init__(self, world):
        self.world = world

    def draw(self, screen):
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
    


    def drawLivingPomPomCount(self, screen, font, world):
        """
        draw a box in the top left that displays the curr num of pompoms
        """
        # Count the number of living PomPoms
        living_pompoms = len([pompom for pompom in world.pompoms if pompom.energy > 0])

        # Create the text to display the count
        count_text = font.render(f"Living PomPoms: {living_pompoms}", True, (255, 255, 255))

        # Define the position and size for the box
        box_width = count_text.get_width() + 10  # Add padding
        box_height = count_text.get_height() + 10
        box_rect = pygame.Rect(10, 10, box_width, box_height)  # Box position at (10, 10) in the corner

        # Draw the box (background)
        pygame.draw.rect(screen, (0, 0, 0), box_rect)  # Black background for the box
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)  # White border for the box

        # Draw the text inside the box
        screen.blit(count_text, (box_rect.x + 5, box_rect.y + 5))  # Position the text inside the box
    

    def drawEpochCount(self, screen, font, world):
        """
        draw box in top left that displays how many turns the world has existed
        incompatiable with drawLivingPompomCount
        """

        # Create the text to display the count
        count_text = font.render(f"Epoch: {world.epoch}", True, (255, 255, 255))

        # Define the position and size for the box
        box_width = count_text.get_width() + 10  # Add padding
        box_height = count_text.get_height() + 10
        box_rect = pygame.Rect(10, 10, box_width, box_height)  # Box position at (10, 10) in the corner

        # Draw the box (background)
        pygame.draw.rect(screen, (0, 0, 0), box_rect)  # Black background for the box
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)  # White border for the box

        # Draw the text inside the box
        screen.blit(count_text, (box_rect.x + 5, box_rect.y + 5))  # Position the text inside the box
    

    def drawPomPomFoodTypeMetrics(self, screen, font, world):
        """
        Draws two boxes in the top right that display the curr num
        of living herbs and carns
        """
        # Count the number of living PomPoms
        carn_pompoms = len([pompom for pompom in world.pompoms if (pompom.energy > 0 and pompom.foodType == "carn")])
        herb_pompoms = len([pompom for pompom in world.pompoms if (pompom.energy > 0 and pompom.foodType == "herb")])

        # Create the text for each metric
        living_text = font.render(f"Carn PomPoms: {carn_pompoms}", True, (255, 255, 255))
        energy_text = font.render(f"Herb PomPoms: {herb_pompoms}", True, (255, 255, 255))

        # Define the position and size for the boxes
        box_width = max(living_text.get_width(), energy_text.get_width()) + 20  # Use the wider text
        box_height = living_text.get_height() + 20
        screen_width, screen_height = screen.get_size()

        # First box (Living PomPoms) at the top-right
        box1_x = screen_width - box_width - 10  # 10px padding from right
        box1_y = 10  # 10px padding from top
        box1_rect = pygame.Rect(box1_x, box1_y, box_width, box_height)

        # Second box (Avg Energy) directly below the first one
        box2_y = box1_y + box_height + 10  # 10px padding between boxes
        box2_rect = pygame.Rect(box1_x, box2_y, box_width, box_height)

        # Draw the boxes (background)
        pygame.draw.rect(screen, (0, 0, 0), box1_rect)  # Black background
        pygame.draw.rect(screen, (255, 255, 255), box1_rect, 2)  # White border
        pygame.draw.rect(screen, (0, 0, 0), box2_rect)  # Black background
        pygame.draw.rect(screen, (255, 255, 255), box2_rect, 2)  # White border

        # Draw the text inside each box
        screen.blit(living_text, (box1_rect.x + 10, box1_rect.y + 10))  # Living PomPoms
        screen.blit(energy_text, (box2_rect.x + 10, box2_rect.y + 10))  # Avg Energy


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

                        