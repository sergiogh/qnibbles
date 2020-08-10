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
from pygame.locals import *

from worm import Worm
from quantum_worm import Quantumworm

from board import Board

FPS = 0.5

QUBITS = 8 # 16 squares = 256 positions. We can represent with 8 qubits.
WINDOWWIDTH = 320
WINDOWHEIGHT = 320
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

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

FINAL_SCORE_1 = 0
FINAL_SCORE_2 = 0

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

    global FINAL_SCORE_1, FINAL_SCORE_2

    board = Board(CELLWIDTH, CELLHEIGHT)

    # Set a random start point.
    classicalWorm   = Worm('Classical', CELLWIDTH, CELLHEIGHT, RIGHT)
    # Our Quantum Adversary!
    quantumWorm     = Quantumworm('Quantum', CELLWIDTH, CELLHEIGHT, LEFT, QUBITS)

    for coordinates in classicalWorm.coordinates:
        board.activateCollision(coordinates['x'], coordinates['y'])
    for coordinates in quantumWorm.coordinates:
        board.activateCollision(coordinates['x'], coordinates['y'])

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

        if classicalWorm.alive == 1:
            wormDirection = classicalWorm.calculateRandomDirection(apple, board)
        if quantumWorm.alive == 1:
            qWormDirections = quantumWorm.calculateQuantumRandomDirection(apple, board)


        # If we run out of possible directions, game over
        if(classicalWorm.alive == 1 and len(wormDirection) == 0):
            print("--- Final scores: Classical Worm has nowhere to go ---")
            classicalWorm.storeResults()
            FINAL_SCORE_1 = classicalWorm.getScore()
            classicalWorm.die()
            for coordinate in classicalWorm.coordinates:
                board.deactivateCollision(coordinate['x'], coordinate['y'])
            classicalWorm.coordinates.clear()

            if classicalWorm.alive == 0 and quantumWorm.alive == 0:
                return # game over

        # If we run out of possible directions, game over
        for qWormDirection in qWormDirections:
            if(quantumWorm.alive == 1 and len(qWormDirection) == 0):
                if(len(quantumWorm.heads) == 1):
                    print("--- Final scores: Quantum Worm has nowhere to go ---")
                    quantumWorm.storeResults()
                    FINAL_SCORE_2 = quantumWorm.getScore()
                    quantumWorm.die()
                    for coordinate in quantumWorm.coordinates:
                        board.deactivateCollision(coordinate['x'], coordinate['y'])
                    quantumWorm.coordinates.clear()

                    if classicalWorm.alive == 0 and quantumWorm.alive == 0:
                        return # game over
                else:
                    quantumWorm.killHeadWithoutDirection()

        # move the worm by adding a segment in the direction it is moving
        if classicalWorm.alive == 1:
            newHead = classicalWorm.calculateNewMovement()
            classicalWorm.growWorm(newHead)

        if quantumWorm.alive == 1:
            print("------------------------")
            print("GROWING QUANTUM WORM ")
            total_heads = []
            for head in quantumWorm.heads:
                qNewHeads = quantumWorm.calculateNewQuantumMovement(head)
                total_heads += qNewHeads
            quantumWorm.heads = total_heads
            quantumWorm.growQuantumWorm(board)

        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(classicalWorm.coordinates, 1)
        drawWorm(quantumWorm.coordinates, 2)

        # check if the worm has hit something or the edge
        if (classicalWorm.alive == 1 and board.getStatus(classicalWorm.coordinates[0]['x'], classicalWorm.coordinates[0]['y']) == 1):
            print("--- Final scores: Classical him himself ---")
            classicalWorm.storeResults()
            FINAL_SCORE_1 = classicalWorm.getScore()
            classicalWorm.die()

            for coordinate in classicalWorm.coordinates:
                board.deactivateCollision(coordinate['x'], coordinate['y'])
            classicalWorm.coordinates.clear()

            if classicalWorm.alive == 0 and quantumWorm.alive == 0:
                return # game over
        else:
            board.activateCollision(classicalWorm.coordinates[0]['x'], classicalWorm.coordinates[0]['y'])

        print("---------------")
        print("HEADS TO CHECK: ")
        print(quantumWorm.heads)
        for qWormHead in quantumWorm.heads:
            if (quantumWorm.alive == 1 and board.getStatus(qWormHead['x'], qWormHead['y']) == 1):
                print("--- Final scores: Quantum hit himself with Head:  ---")
                print(qWormHead)
                print(board.printGrid())
                quantumWorm.storeResults()
                FINAL_SCORE_2 = quantumWorm.getScore()
                quantumWorm.die()

                for coordinate in quantumWorm.coordinates:
                    board.deactivateCollision(coordinate['x'], coordinate['y'])
                quantumWorm.coordinates.clear()

                if classicalWorm.alive == 0 and quantumWorm.alive == 0:
                    return # game over
            else:
                board.activateCollision(qWormHead['x'], qWormHead['y'], qWormHead['probability'])




        # check if worm has eaten an apple
        if (classicalWorm.alive == 1 and len(classicalWorm.coordinates) > 0) :
            if classicalWorm.coordinates[0]['x'] == apple['x'] and classicalWorm.coordinates[0]['y'] == apple['y']:
                # don't remove worm's tail segment
                apple = getRandomLocation() # set a new apple somewhere
            else:
                board.deactivateCollision(classicalWorm.coordinates[-1]['x'], classicalWorm.coordinates[-1]['y'])
                del classicalWorm.coordinates[-1] # remove worm's tail segment

        # check if Quantum worm has eaten an apple
        if (quantumWorm.alive == 1 and len(quantumWorm.coordinates) > 0) :
            if quantumWorm.coordinates[0]['x'] == apple['x'] and quantumWorm.coordinates[0]['y'] == apple['y']:
                # don't remove worm's tail segment
                apple = getRandomLocation() # set a new apple somewhere
            else:
                board.deactivateCollision(quantumWorm.coordinates[-1]['x'], quantumWorm.coordinates[-1]['y'])
                del quantumWorm.coordinates[-1] # remove worm's tail segment

        drawApple(apple)
        drawScore(classicalWorm.getScore(), 1)
        drawScore(quantumWorm.getScore(), 2)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

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

    global FINAL_SCORE_1, FINAL_SCORE_2

    gameOverFont = pygame.font.Font('freesansbold.ttf', 50)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 30)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 30 + 25)

    drawScore(FINAL_SCORE_1, 1)
    drawScore(FINAL_SCORE_2, 2)

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
            pygame.time.wait(3000)
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
        scoreRect.topleft = (WINDOWWIDTH - 320, 30)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords, palette = 1):
    if palette == 2:
        dark_color = DARKORANGE
        light_color = ORANGE
    else:
        dark_color = DARKGREEN
        light_color = GREEN

    i = 0
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE



        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, dark_color, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        if i == 0:
            pygame.draw.rect(DISPLAYSURF, dark_color, wormInnerSegmentRect)
        else:
            pygame.draw.rect(DISPLAYSURF, light_color, wormInnerSegmentRect)
        i += 1

        if ('probability' in coord and coord['probability'] > 0):
            s = pygame.Surface((CELLSIZE-8,CELLSIZE-8))  # the size of your rect
            alpha = 255 * coord['probability']
            if (alpha < 20): alpha = 20
            s.set_alpha(alpha)                # alpha level
            s.fill((255,255,255))           # this fills the entire surface
            DISPLAYSURF.blit(s, (x+4,y+4))    # (0,0) are the top-left coordinates


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


if __name__ == '__main__':
    main()
