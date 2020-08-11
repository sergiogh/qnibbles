
import random
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
valid_movements = [UP, LEFT, RIGHT, DOWN]

class Worm:

    initial_lenght = 3

    def __init__(self, name, width, height, direction):
        startx = random.randint(4, width - 8)
        starty = random.randint(4, height - 8)
        self.coordinates = [{'x': startx,     'y': starty},
                            {'x': startx - 1, 'y': starty},
                            {'x': startx - 2, 'y': starty}]

        self.direction = direction

        self.score = 0
        self.name = name

        self.board_width = width
        self.board_height = height

        self.alive = 1


    def setCoordinates(self, coordinates):
        self.coordinates = [{'x': coordinates['x'],     'y': coordinates['y']},
                            {'x': coordinates['x'] - 1, 'y': coordinates['y']},
                            {'x': coordinates['x'] - 2, 'y': coordinates['y']}]

    def growWorm(self, coordinates):
        self.coordinates.insert(0, coordinates)

    def randomMovement(self, valid_movements):
        if len(valid_movements) == 1:
            return valid_movements[0]
        else:
            return valid_movements[random.randint(0, len(valid_movements)-1)]

    def calculateNewMovement(self):
        if self.direction == UP:
            newHead = {'x': self.coordinates[0]['x'], 'y': self.coordinates[0]['y'] - 1}
        elif self.direction == DOWN:
            newHead = {'x': self.coordinates[0]['x'], 'y': self.coordinates[0]['y'] + 1}
        elif self.direction == LEFT:
            newHead = {'x': self.coordinates[0]['x'] - 1, 'y': self.coordinates[0]['y']}
        elif self.direction == RIGHT:
            newHead = {'x': self.coordinates[0]['x'] + 1, 'y': self.coordinates[0]['y']}

        return newHead

    def die(self, board):
        self.alive = 0
        # Remove collision points in the board for the whole worm
        for coordinate in self.coordinates:
            boatd.deactivateCollision(coordinate['x'], coordinate['y'])
        self.coordinates.clear()

    def live(self):
        self.alive = 1

    def getScore(self):
        return self.score

    def setScore(self, score):
        self.score = score
        return self.score

    def storeResults(self):
        print("===================")
        print("-------------------")
        print("FINAL SCORE FOR %s" % self.name)
        print("%s: %s" % (self.name, self.getScore()))

    def calculateRandomDirection(self, apple, board):
        # Weighted random walk. With a bias towards the apple and avoiding walls and other collisions

        # Make movements automatic
        valid_movements = [UP, LEFT, RIGHT, DOWN]

        # Add more random weight to tilt towards the apple
        if(apple['x'] > self.coordinates[0]['x']):
            valid_movements.append(RIGHT)
        else:
            valid_movements.append(LEFT)
        if(apple['y'] < self.coordinates[0]['y']):
            valid_movements.append(UP)
        else:
            valid_movements.append(DOWN)

        # Avoid the walls
        if self.coordinates[0]['x'] == 0:
            valid_movements = list(filter(lambda a: a != LEFT, valid_movements))
        if self.coordinates[0]['x'] >= self.board_width - 1:
            valid_movements = list(filter(lambda a: a != RIGHT, valid_movements))
        if self.coordinates[0]['y'] == 0:
            valid_movements = list(filter(lambda a: a != UP, valid_movements))
        if self.coordinates[0]['y'] >= self.board_height - 1:
            valid_movements = list(filter(lambda a: a != DOWN, valid_movements))

        self.direction = self.randomMovement(valid_movements) # Get a random movement

        change_direction = True
        while(change_direction == True):
            potentialNewHead = self.calculateNewMovement()
            if (board.getStatus(potentialNewHead['x'], potentialNewHead['y']) > 0):
                change_direction = True
                valid_movements = list(filter(lambda a: a != self.direction, valid_movements))   # Remove invalid direction from the list
                if(len(valid_movements) == 0):
                    return ''
                self.direction = self.randomMovement(valid_movements)
            else:
                change_direction = False

            # If there is no solution we are stuck
            if len(self.direction) == 0:
                return ''

        return self.direction
