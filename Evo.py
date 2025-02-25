import random

class Evolution():
    """
    This will handle the creation of new pom poms.
    """

    def __init__(self, pom1, pom2, grid):
        self.mother = pom1
        self.father = pom2
        self.grid = grid

    def spawnBabies(self):
        num = random.randint(1, 3)  # Number of babies
        spawnPoints = [pos for pos in self.mother.adjacentTiles if pos is not None]
        available_spots = [pos for pos in spawnPoints if self.isValid(pos)]
        random.shuffle(available_spots)  # Shuffle to randomize placement
        for i in range(min(num, len(available_spots))):  # Only place babies in valid spots
            baby = self.createPom()
            baby.rect.x, baby.rect.y = available_spots[i]  # Assign position
            self.grid[baby.rect.x][baby.rect.y] = baby  # Place in grid
        return self.grid

    def isValid(self, pos):
        """Check if the position is within bounds and empty."""
        x, y = pos
        return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0]) and self.grid[x][y] is None

    def createPom(self):
        """
        Will look at the two parents and make a new pom
        with randomized genes from them.
        """
        baby = PomPom(self.mother.rect.x, self.mother.rect.y, self.grid)  # Create a new instance
        return baby
