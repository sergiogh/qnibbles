
class Board:

    def __init__(self, width, height):
        self.collision_grid = [ [ 0 for y in range( height ) ]
                                    for x in range( width ) ]


    def activateCollision(self, x, y, probability = 1):
        self.collision_grid[y][x] += probability

    def deactivateCollision(self, x, y):
        self.collision_grid[y][x] = 0

    def getStatus(self, x, y):
        if 0 <= x < len(self.collision_grid):
            if 0 <= y < len(self.collision_grid[x]):
                return self.collision_grid[y][x]

        return 1

    def printGrid(self):
        for r in self.collision_grid:
            for c in r:
                print(c, end = " ")
            print()
