""" A very plain script that prints a Hexagon in a 2D grid """

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
    screenHeight = 800
    screenWidth = 800

    cellSize = screenHeight / cellCountX
    if hexagonLayout:
        screenHeight *= 0.85
        screenWidth *= 1.04

    size = [int(screenHeight), int(screenWidth)]
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
                            currentColour = GREEN

                        if hexagonLayout:
                            drawHexagon(screen, currentColour, currentColumn, cellSize, currentRow)
                        else:
                            drawSquare(screen, currentColour, currentColumn, cellSize, currentRow)

        # This MUST happen after all the other drawing commands.
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        #pygame.time.delay(1)
        #time.sleep(3)

''' Print the current generation '''
def printGenerationUniverse(currentTimeStep, cellCountX, cellCountY, susceptibleCharacter, exposedCharacter, infectedCharacter, recoveredCharacter):
    print "TimeStep %3i:  " % currentTimeStep
    rowLabel = "  "
    for l in range(cellCountX):
        rowLabel += str(l) + " "
    print rowLabel
    for currentRow in range(cellCountY):
        print "%s %s" % (currentRow, universeList[currentRow].replace('0', susceptibleCharacter + " ").replace('1', exposedCharacter + " ").
                         replace('2', infectedCharacter + " ").replace('3', recoveredCharacter + " "))

hexagonLayout = True
simulationIterations = 4
cellCountX = 5
cellCountY = 5

drawGenerationUniverse(cellCountX, cellCountY, [['00020','00020','00020','00020','00020'],['00020','00020','00020','00020','00000'],
                              ['02020','00020','00020','00020','00000'], ['02020','00020','00000','00020','00000']] )