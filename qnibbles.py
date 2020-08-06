# QNibbles - A Quantum Nibbles game
# Based on the classical version Wormy By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license


# Quantum Version by Sergio Gago


# 2-dimensional Hadamard walk.) Let
# A = H2 ⊗ H2 = 1/2 [[1,1,1,1], [1, -1,1,-1], [1,1,-1,-1], [1,-1,-1,1]]


# QUANTUM RANDOM WALKS ON ONE AND TWO DIMENSIONAL LATTICES - 2005, 2005
# https://pdfs.semanticscholar.org/ce7f/794ee142599bdee748df267fb84b5dcf83c0.pdf

# Two-dimensional quantum random walk
# https://arxiv.org/abs/0810.5495


# Algorithm to apply

"""
Algorithm Discrete time quantum walk
Input:
• Two quantum registers. The coin register and the position register.
• Number of steps, T . Output:
• State of the quantum walk after T steps. Procedure:
Step 1. Create the initial state. The initial state depends on the application. For instance, in quantum search algorithms, the initial state is the uniform superposition state.
for 0 ≤ k < T do
Step 2a. Apply the coin operator, C, to the coin register.
Step 2b. Apply the shift operator, S. This shifts the position of the walker controlled
on the coin state.
end for
Step 3. (Optional) Measure the final state.
"""




import random, pygame, sys
from quantum_worm import *
from pygame.locals import *

FPS = 30

# 16 squares = 256 positions. We can represent with 8 qubits.
QUBITS = 8
WINDOWWIDTH = 320
WINDOWHEIGHT = 320
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

SNAKES_GRID = [ [ 0 for y in range( CELLHEIGHT ) ]
                    for x in range( CELLWIDTH ) ]





#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
ORANGE    = (255, 165,   0)
DARKORANGE  = (180, 64, 16)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
valid_movements = [UP, LEFT, RIGHT, DOWN]

HEAD = 0 # syntactic sugar: index of the worm's head

SCORE_PLAYER_1 = FINAL_SCORE_1 = 0
SCORE_PLAYER_2 = FINAL_SCORE_2 = 0


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('QNibbles')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():

    # Set a random start point.
    startx = random.randint(4, CELLWIDTH - 8)
    starty = random.randint(4, CELLHEIGHT - 8)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT
    #SNAKES_GRID[startx][starty] = 1
    #SNAKES_GRID[startx-1][starty] = 1
    #SNAKES_GRID[startx-2][starty] = 1

    # Our Quantum Adversary!
    quantumCoordinates = quantumRandomStartingPoint(QUBITS)
    print(quantumCoordinates)
    startx = quantumCoordinates['x']
    starty = quantumCoordinates['y']
    qwormCoords = [{'x': startx,     'y': starty},
                   {'x': startx + 1, 'y': starty},
                   {'x': startx + 2, 'y': starty}]
    qWormDirection = LEFT
    #SNAKES_GRID[startx][starty] = 1
    #SNAKES_GRID[startx+1][starty] = 1
    #SNAKES_GRID[startx+2][starty] = 1

    # Start the apple in a random place.
    apple = getRandomLocation()

    while True: # main game loop
        # Key control
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            """ Let's ignore keystrokes for the moment
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()
            """

        direction = calculateRandomDirection(wormCoords, apple)
        qWormDirection = calculateRandomDirection(qwormCoords, apple)

        # If we run out of possible directions, game over
        if(len(direction) == 0 or len(qWormDirection) == 0):
            print("--- Final scores: Death by no more directions ---")
            storeResults(getScore(wormCoords), getScore(qwormCoords))
            return # game over

        # move the worm by adding a segment in the direction it is moving
        newHead = calculateNewMovement(wormCoords, direction)
        qNewHead = calculateNewMovement(qwormCoords, qWormDirection)
        wormCoords.insert(0, newHead)
        qwormCoords.insert(0, qNewHead)

        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords, 1)
        drawWorm(qwormCoords, 2)

        # check if the worm has hit something or the edge
        if (SNAKES_GRID[wormCoords[HEAD]['x']][wormCoords[HEAD]['y']] == 1):
            print("--- Final scores: Classical him himself ---")
            storeResults(getScore(wormCoords), getScore(qwormCoords))
            return # game over
        elif (SNAKES_GRID[qwormCoords[HEAD]['x']][qwormCoords[HEAD]['y']] == 1):
            print("--- Final scores: Quantum hit himself ---")
            storeResults(getScore(wormCoords), getScore(qwormCoords))
            return # game over
        else:
            SNAKES_GRID[newHead['x']][newHead['y']] = 1
            SNAKES_GRID[qNewHead['x']][qNewHead['y']] = 1


        # check if worm has eaten an apple
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
        else:
            SNAKES_GRID[wormCoords[-1]['x']][wormCoords[-1]['y']] = 0
            del wormCoords[-1] # remove worm's tail segment

        # check if Quantum worm has eaten an apple
        if qwormCoords[HEAD]['x'] == apple['x'] and qwormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
        else:
            SNAKES_GRID[qwormCoords[-1]['x']][qwormCoords[-1]['y']] = 0
            del qwormCoords[-1] # remove worm's tail segment

        drawApple(apple)

        drawScore(getScore(wormCoords), 1)
        drawScore(getScore(qwormCoords), 2)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def randomMovement(valid_movements):
    return valid_movements[random.randint(0, len(valid_movements)-1)]

def calculateRandomDirection(wormCoords, apple):

    # Hack to make movements automatic
    valid_movements = [UP, LEFT, RIGHT, DOWN]

    # Add more random weight to tilt towards the apple
    if(apple['x'] > wormCoords[HEAD]['x']):
        valid_movements.append(RIGHT)
    else:
        valid_movements.append(LEFT)
    if(apple['y'] < wormCoords[HEAD]['y']):
        valid_movements.append(UP)
    else:
        valid_movements.append(DOWN)

    # Avoid the walls
    if wormCoords[HEAD]['x'] == 0:
        valid_movements = list(filter(lambda a: a != LEFT, valid_movements))
    if wormCoords[HEAD]['x'] >= CELLWIDTH-1:
        valid_movements = list(filter(lambda a: a != RIGHT, valid_movements))
    if wormCoords[HEAD]['y'] == 0:
        valid_movements = list(filter(lambda a: a != UP, valid_movements))
    if wormCoords[HEAD]['y'] >= CELLHEIGHT-1:
        valid_movements = list(filter(lambda a: a != DOWN, valid_movements))

    direction = randomMovement(valid_movements) # Get a random movement

    change_direction = True
    while(change_direction == True):
        potentialNewHead = calculateNewMovement(wormCoords, direction)
        if SNAKES_GRID[potentialNewHead['x']][potentialNewHead['y']] == 1:
            change_direction = True
            valid_movements = list(filter(lambda a: a != direction, valid_movements))   # Remove invalid direction from the list
            if(len(valid_movements) == 0):
                return direction
            direction = randomMovement(valid_movements)
        else:
            change_direction = False

        # If there is no solution we are stuck
        if len(direction) == 0:
            return direction

    return direction

def calculateNewMovement(wormCoords, direction):
    if direction == UP:
        newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
    elif direction == DOWN:
        newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
    elif direction == LEFT:
        newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
    elif direction == RIGHT:
        newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}

    return newHead

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Quantum', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Nibbles!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 50)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    drawScore(FINAL_SCORE_1, 1)
    drawScore(FINAL_SCORE_1, 2)

    # Reset collision grid
    SNAKES_GRID = [ [ 0 for y in range( CELLHEIGHT ) ]
                        for x in range( CELLWIDTH ) ]

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue


    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        else:
            pygame.time.wait(600)
            pygame.event.get() # clear event queue
            return


def drawScore(score, player):
    if (player == 1):
        scoreSurf = BASICFONT.render('Classical Worm: %s' % (score), True, DARKGREEN)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 320, 10)
    if (player == 2):
        scoreSurf = BASICFONT.render('Quantum Worm: %s' % (score), True, DARKORANGE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topright = (WINDOWWIDTH - 320, 40)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords, palette = 1):
    if palette == 2:
        dark_color = DARKORANGE
        light_color = ORANGE
    else:
        dark_color = DARKGREEN
        light_color = GREEN

    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, dark_color, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, light_color, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

def getScore(worm):
    return len(worm) - 3

def storeResults(score_1, score_2):
    print("Classical: %s" % score_1)
    print("Quantum: %s" % score_2)

if __name__ == '__main__':
    main()
