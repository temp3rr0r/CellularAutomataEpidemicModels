import random
import numpy as np
import pylab as pl
from operator import itemgetter
# Import a library of functions called 'pygame'
import pygame
from math import pi
import time

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

''' Print the current generation '''
def printGenerationUniverse(currentTimeStep, cellCountX, cellCountY, normalCharacter, susceptibleCharacter, infectedCharacter, recoveredCharacter):
    print "TimeStep %3i:  " % currentTimeStep
    rowLabel = "  "
    for l in range(cellCountX):
        rowLabel += str(l) + " "
    print rowLabel
    for currentRow in range(cellCountY):
        print "%s %s" % (currentRow, universeList[currentRow].replace('0', normalCharacter + " ").replace('1', susceptibleCharacter + " ").
                         replace('2', infectedCharacter + " ").replace('3', recoveredCharacter + " "))

''' This method calculates the new state of the cell based on Van Neumann neighborhood '''
def getNewState2D(currentRowNeighbours, upperRowNeighbours, lowerRowNeighbours):

    selfCharacter = currentRowNeighbours[1]

    newState = selfCharacter

    if selfCharacter == '0': # If Normal and there is an Infected close, be Susceptible
        if currentRowNeighbours.count('2') > 0 or upperRowNeighbours.count('2') > 0 or lowerRowNeighbours.count('2') > 0:
            newState = '1'
    elif selfCharacter == '1': # if Susceptible, calculate the probability to be Infected
        #betaChance = (2 - np.random.normal(0.5, 1.0)) # NORMAL
        betaChance = (2 - np.random.uniform()) # UNIFORM
        #betaChance = (2 - (np.random.poisson(2) % 10) * 0.1) # POISSON
        if betaChance > 0 and betaChance < beta:
            newState = '2'
        else:
            if currentRowNeighbours.count('2') > 0 or upperRowNeighbours.count('2') > 0 or lowerRowNeighbours.count('2') > 0:
                newState = '1'
            else:
                newState = '0'
    elif selfCharacter == '2': # if Infected, calculate the probability to be Recovered 'to recover'
        #gammaChance = (1 - np.random.normal(0.5, 1.0)) # NORMAL
        gammaChance = (1 - np.random.uniform()) # UNIFORM
        #gammaChance = (1 - (np.random.poisson(2) % 10) * 0.1) # POISSON

        if gammaChance < gamma and gammaChance > 0:
            newState = '3'
    elif selfCharacter == '3': # Recovered, immune for a while
        #rhoChance = (1 - np.random.normal(0.5, 1.0)) # NORMAL
        rhoChance = (1 - np.random.uniform()) # UNIFORM
        #rhoChance = (1 - (np.random.poisson(2) % 10) * 0.1) # POISSON

        if rhoChance < rho and rhoChance > 0:
            newState = '0'

    return newState

# SIS Model Parameters
beta = 1.43#1.13247 # Chance to get S from neighbouring I
gamma = 0.14#.14#.1#.2#0.140 # Chance to get from I to R (or normal in our case)
rho = 0.33#.33#.8#.33#0.50 # Chance ot get from R to normal (Loss of immunity rate)
simulationIterations = 30
cellCountX = 100
cellCountY = 100

# Init values
susceptibleCharacter = 'S'
recoveredCharacter = 'R'
infectedCharacter ='I'
normalCharacter = '_'
extremeEndValue = '0'
timeStart = 0.0
timeEnd = simulationIterations
timeStep = 1
timeRange = np.arange(timeStart, timeEnd + timeStart, timeStep)
universeList = []

# Randomise first state
for currentColumn in range(cellCountY):
    # if currentColumn == (cellCountY / 2):
    #     universe = ''.join('0' for universeColumn in range((cellCountX / 2) - 1))
    #     universe += '2'
    #     universe += ''.join('0' for universeColumn in range(cellCountX / 2))
    # else:
    universe = ''.join(random.choice('0000000000000000000000000002') for universeColumn in range(cellCountX))
    universeList.append(universe)

# TODO: Fix init state vars
InitSusceptibles = 0.0
InitInfected = 0.0
InitRecovered = 0.0
InitVariables = [InitSusceptibles, InitInfected, 0.0, 0.0, 0.0]

RES = [InitVariables]

universeTimeSeries = []

# Main Execution loop
for currentTimeStep in range(simulationIterations):

    # Print the current generation
    if currentTimeStep < 4:
        printGenerationUniverse(currentTimeStep, cellCountX, cellCountY, normalCharacter, susceptibleCharacter, infectedCharacter, recoveredCharacter)

    # Store the counts of I, S and the time iteration
    zeroCount = 0
    oneCount = 0
    twoCount = 0
    threeCount = 0
    for currentRow in range(cellCountY):
        zeroCount += universeList[currentRow].count('0')
        oneCount += universeList[currentRow].count('1')
        twoCount += universeList[currentRow].count('2')
        threeCount += universeList[currentRow].count('3')
    RES.append([zeroCount, oneCount, twoCount, threeCount, currentTimeStep])

    # Put extreme ends neighbouring cells temporarily on the old universe
    oldUniverseList = []
    toCopyUniverseList = []
    for currentRow in range(cellCountY):
        oldUniverseList.append(extremeEndValue + universeList[currentRow] + extremeEndValue)
        toCopyUniverseList.append(universeList[currentRow])

    universeTimeSeries.append(toCopyUniverseList)

    for currentRow in range(cellCountY):
        newUniverseRow = ''
        for currentColumn in range(cellCountX):
            upperRowNeighbours = '000'
            lowerRowNeighbours = '000'
            currentRowNeighbours = oldUniverseList[currentRow][currentColumn:currentColumn+3]
            if (currentRow - 1) >= 0:
                upperRowNeighbours = oldUniverseList[currentRow-1][currentColumn:currentColumn+3]
            if (currentRow + 1) < cellCountY:
                lowerRowNeighbours = oldUniverseList[currentRow+1][currentColumn:currentColumn+3]

            newUniverseRow += getNewState2D(currentRowNeighbours, upperRowNeighbours, lowerRowNeighbours)
            universeList[currentRow] = newUniverseRow

#print RES

#print(universeTimeSeries)

#Ploting
pl.subplot(2, 1, 1)
pl.plot(map(itemgetter(4), RES), map(itemgetter(2), RES), '-r', label='Infected')
pl.plot(map(itemgetter(4), RES), map(itemgetter(0), RES), '-b', label='Normal')
pl.plot(map(itemgetter(4), RES), map(itemgetter(1), RES), '-y', label='Susceptibles')
pl.plot(map(itemgetter(4), RES), map(itemgetter(3), RES), '-g', label='Recovered')
pl.legend(loc=0)
pl.title('All vs Time')
pl.xlabel('Time')
pl.ylabel('Count')

pl.subplot(2, 1, 2)
pl.plot(map(itemgetter(4), RES), map(itemgetter(2), RES), '-r', label='Infected')
pl.plot(map(itemgetter(4), RES), map(itemgetter(1), RES), '-b', label='Normal')
pl.legend(loc=0)
pl.title('Infected and Normal')
pl.xlabel('Infected')
pl.ylabel('Normal')

pl.show()

drawGenerationUniverse(cellCountX, cellCountY, universeTimeSeries)
