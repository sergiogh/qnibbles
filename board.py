
class Board:

    def __init__(self, width, height):
        self.collision_grid = [ [ 0 for y in range( height ) ]
                                    for x in range( width ) ]


    def activateCollision(self, x, y):
        self.collision_grid[y][x] = 1

    def deactivateCollision(self, x, y):
        self.collision_grid[y][x] = 0

    def getStatus(self, x, y):
        return self.collision_grid[y][x]

    def printGrid(self):
        for r in self.collision_grid:
            for c in r:
                print(c, end = " ")
            print()
