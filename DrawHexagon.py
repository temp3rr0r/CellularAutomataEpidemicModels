import random
import numpy as np
import pylab as pl
from operator import itemgetter
# Import a library of functions called 'pygame'
import pygame
from math import pi
import time

def drawSquare(screen, currentColour, currentColumn, cellSize, currentRow):
    pygame.draw.rect(screen, currentColour, [currentColumn * cellSize, currentRow * cellSize, (currentColumn + 1)
                                                                 * cellSize, (currentRow + 1) * cellSize])

def drawHexagon(screen, currentColour, currentColumn, cellSize, currentRow):

    minX = currentColumn * cellSize
    maxX =(currentColumn + 1)* cellSize
    minY = currentRow * cellSize
    maxY = (currentRow + 1) * cellSize
    quarterLength = (maxY - minY) / 4

    spacing =  (2 * quarterLength)

    if currentColumn > 1:
        minX -= spacing * int(currentColumn / 2)
        maxX -= spacing * int(currentColumn / 2)
    #     # #
    #     # if currentColumn % 2 == 0:
    #     # #     minX -= spacing * currentColumn
    #     # #     maxX -= spacing * currentColumn
    #     # # else:
    #     #     minX -= spacing * currentColumn
    #     #     maxX -= spacing * currentColumn
    if currentColumn % 2 == 1:
        minX -= quarterLength
        maxX -= quarterLength
        minY += spacing
        maxY += spacing


    center = [minX + 2 * quarterLength, minY + 2 * quarterLength]
    a = [minX + quarterLength, minY]
    b = [minX + 3 * quarterLength, minY]
    d = [maxX, minY + 2 * quarterLength]
    e = [minX + 3 * quarterLength, maxY]
    f = [minX + quarterLength, maxY]
    g = [minX, minY + 2 * quarterLength]

    pygame.draw.polygon(screen, currentColour, [center, a, b])
    pygame.draw.polygon(screen, currentColour, [center, b, d])
    pygame.draw.polygon(screen, currentColour, [center, d, e])
    pygame.draw.polygon(screen, currentColour, [center, e, f])
    pygame.draw.polygon(screen, currentColour, [center, f, g])
    pygame.draw.polygon(screen, currentColour, [center, g, a])

def drawGenerationUniverseHexagons(cellCountX, cellCountY, universeTimeSeries):
    # Initialize the game engine
    pygame.init()

    # Define the colors we will use in RGB format
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)
    BLUE =  (  0,   0, 255)
    GREEN = (  0, 255,   0)
    YELLOW =   (255,   255,   0)
    RED =   (255,   0,   0)
    ORANGE =   (255,   165,   0)

    # Set the height and width of the screen
    screenHeight = 400
    screenWidth = 400
    cellSize = screenHeight / cellCountX
    size = [screenHeight * 2, screenWidth * 2]
    screen = pygame.display.set_mode(size)
    screen.fill(WHITE)

    #Loop until the user clicks the close button.
    clock = pygame.time.Clock()

    #while 1:
    # Make sure game doesn't run at more than 60 frames per second
    mainloop = True
    FPS = 60                           # desired max. framerate in frames per second.
    playtime = 0
    cycletime = 0
    interval = .15#.15 # how long one single images should be displayed in seconds
    picnr = 0

    #for currentStep in range(simulationIterations):
    currentTimeStep = 0

    while mainloop:
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
        playtime += seconds
        cycletime += seconds
        if cycletime > interval:

            if currentTimeStep >= simulationIterations:
                currentTimeStep = 0
            else:
                currentTimeStep += 1
            #pygame.time.delay(3000)
            pygame.display.set_caption("TimeStep %3i:  " % currentTimeStep)

            picnr += 1
            if picnr > 5:
                picnr = 0
            cycletime = 0

            currentColour = BLACK
            for currentRow in range(cellCountY):# Draw a solid rectangle
                for currentColumn in range (cellCountX):
                    # rect(Surface, color, Rect, width=0) -> Rect
                    if currentTimeStep > 0 and currentTimeStep < simulationIterations:
                        if universeTimeSeries[currentTimeStep][currentRow][currentColumn] == '0':
                            currentColour = BLUE
                        if universeTimeSeries[currentTimeStep][currentRow][currentColumn] == '1':
                            currentColour = YELLOW
                        if universeTimeSeries[currentTimeStep][currentRow][currentColumn] == '2':
                            currentColour = RED
                        if universeTimeSeries[currentTimeStep][currentRow][currentColumn] == '3':
                            currentColour = BLUE

                        # pygame.draw.rect(screen, currentColour, [currentColumn * cellSize, currentRow * cellSize, (currentColumn + 1)
                        #                                          * cellSize, (currentRow + 1) * cellSize])
                        #drawSquare(screen, currentColour, currentColumn, cellSize, currentRow)
                        drawHexagon(screen, currentColour, currentColumn, cellSize, currentRow)

        # This MUST happen after all the other drawing commands.
        pygame.display.flip()
        #pygame.time.delay(1)
        # Go ahead and update the screen with what we've drawn.
        #time.sleep(3)

    # print "TimeStep %3i:  " % currentTimeStep
    # rowLabel = "  "
    # for l in range(cellCountX):
    #     rowLabel += str(l) + " "
    # print rowLabel
    # for currentRow in range(cellCountY):
    #     print "%s %s" % (currentRow, universeList[currentRow].replace('0', normalCharacter + " ").replace('1', susceptibleCharacter + " ").
    #                      replace('2', infectedCharacter + " ").replace('3', recoveredCharacter + " "))

def drawGenerationUniverse(cellCountX, cellCountY, universeTimeSeries):
    # Initialize the game engine
    pygame.init()

    # Define the colors we will use in RGB format
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)
    BLUE =  (  0,   0, 255)
    GREEN = (  0, 255,   0)
    YELLOW =   (255,   255,   0)
    RED =   (255,   0,   0)
    ORANGE =   (255,   165,   0)

    # Set the height and width of the screen
    screenHeight = 400
    screenWidth = 400
    size = [screenHeight, screenWidth]
    screen = pygame.display.set_mode(size)
    screen.fill(WHITE)
    cellSize = screenHeight / cellCountX

    #Loop until the user clicks the close button.
    clock = pygame.time.Clock()

    #while 1:
    # Make sure game doesn't run at more than 60 frames per second
    mainloop = True
    FPS = 60                           # desired max. framerate in frames per second.
    playtime = 0
    cycletime = 0
    interval = .15#.15 # how long one single images should be displayed in seconds
    picnr = 0

    #for currentStep in range(simulationIterations):
    currentTimeStep = 0

    while mainloop:
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
        playtime += seconds
        cycletime += seconds
        if cycletime > interval:

            if currentTimeStep >= simulationIterations:
                currentTimeStep = 0
            else:
                currentTimeStep += 1
            #pygame.time.delay(3000)
            pygame.display.set_caption("TimeStep %3i:  " % currentTimeStep)

            picnr += 1
            if picnr > 5:
                picnr = 0
            cycletime = 0

            currentColour = BLACK
            for currentRow in range(cellCountY):# Draw a solid rectangle
                for currentColumn in range (cellCountX):
                    # rect(Surface, color, Rect, width=0) -> Rect
                    if currentTimeStep > 0 and currentTimeStep < simulationIterations:
                        if universeTimeSeries[currentTimeStep][currentRow][currentColumn] == '0':
                            currentColour = BLUE
                        if universeTimeSeries[currentTimeStep][currentRow][currentColumn] == '1':
                            currentColour = YELLOW
                        if universeTimeSeries[currentTimeStep][currentRow][currentColumn] == '2':
                            currentColour = RED
                        if universeTimeSeries[currentTimeStep][currentRow][currentColumn] == '3':
                            currentColour = BLUE

                        pygame.draw.rect(screen, currentColour, [currentColumn * cellSize, currentRow * cellSize, (currentColumn + 1)
                                                                 * cellSize, (currentRow + 1) * cellSize])

        # This MUST happen after all the other drawing commands.
        pygame.display.flip()
        #pygame.time.delay(1)
        # Go ahead and update the screen with what we've drawn.
        #time.sleep(3)

    # print "TimeStep %3i:  " % currentTimeStep
    # rowLabel = "  "
    # for l in range(cellCountX):
    #     rowLabel += str(l) + " "
    # print rowLabel
    # for currentRow in range(cellCountY):
    #     print "%s %s" % (currentRow, universeList[currentRow].replace('0', normalCharacter + " ").replace('1', susceptibleCharacter + " ").
    #                      replace('2', infectedCharacter + " ").replace('3', recoveredCharacter + " "))

simulationIterations = 4

drawGenerationUniverseHexagons(5, 5, [['00020','00020','00020','00020','00020'],['00020','00020','00020','00020','00000'],
                              ['02020','00020','00020','00020','00000'], ['02020','00020','00000','00020','00000']] )