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
    screenHeight = 600
    screenWidth = 600

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
                            currentColour = BLUE

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
def printGenerationUniverse(currentTimeStep, cellCountX, cellCountY, normalCharacter, susceptibleCharacter, infectedCharacter, recoveredCharacter):
    print "TimeStep %3i:  " % currentTimeStep
    rowLabel = "  "
    for l in range(cellCountX):
        rowLabel += str(l) + " "
    print rowLabel
    for currentRow in range(cellCountY):
        print "%s %s" % (currentRow, universeList[currentRow].replace('0', normalCharacter + " ").replace('1', susceptibleCharacter + " ").
                         replace('2', infectedCharacter + " ").replace('3', recoveredCharacter + " "))

''' This method calculates the new state of the cell based on Van Neumann HEX neighborhood '''
def getNewState2DHex(selfCharacter, hexNeighbours):
    newState = selfCharacter

    if selfCharacter == '0': # If Normal and there is an Infected close, be Susceptible
        if (hexNeighbours.count('2') > 0):
            newState = '1'
    elif selfCharacter == '1': # if Susceptible, calculate the probability to be Infected
        #betaChance = (2 - np.random.normal(0.5, 1.0)) # NORMAL
        betaChance = (2 - np.random.uniform()) # UNIFORM
        #betaChance = (2 - (np.random.poisson(2) % 10) * 0.1) # POISSON
        if betaChance > 0 and betaChance < beta:
            newState = '2'
        else:
            if (hexNeighbours.count('2') > 0):
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
beta = 1.13247 # Chance to get S from neighbouring I
gamma = 0.4140 # Chance to get from I to R (or normal in our case)
rho = .33 # Chance ot get from R to normal (Loss of immunity rate)
simulationIterations = 30
cellCountX = 50
cellCountY = 50
hexagonLayout = False

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
    if currentTimeStep < 0:
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
        if hexagonLayout:
            oldUniverseList.append(universeList[currentRow])
        else:
            oldUniverseList.append(extremeEndValue + universeList[currentRow] + extremeEndValue)
        toCopyUniverseList.append(universeList[currentRow])

    universeTimeSeries.append(toCopyUniverseList)

    for currentRow in range(cellCountY):
        newUniverseRow = ''
        for currentColumn in range(cellCountX):

            if hexagonLayout:
                # HEX
                hexNeighbours = list("000000") # list of characters

                # Top/bottom CELL 2 & CELL 3 - Same for ODD and EVEN
                if (currentRow - 1) >= 0: # CELL 2
                    hexNeighbours[2] = oldUniverseList[currentRow - 1][currentColumn]
                if (currentRow + 1) < cellCountY: # CELL 3
                    hexNeighbours[3] = oldUniverseList[currentRow + 1][currentColumn]

                if (currentColumn % 2 == 0):
                    if (currentColumn - 1) >= 0: # CELL 1 EVEN
                        hexNeighbours[1] = oldUniverseList[currentRow][currentColumn - 1]
                        if (currentRow - 1) >= 0: # CELL 0 EVEN
                            hexNeighbours[0] = oldUniverseList[currentRow - 1][currentColumn - 1]
                    if (currentColumn + 1) < cellCountX: # CELL 5 EVEN
                        hexNeighbours[5] = oldUniverseList[currentRow][currentColumn + 1]
                        if (currentRow - 1) >= 0: # CELL 4 EVEN
                            hexNeighbours[4] = oldUniverseList[currentRow - 1][currentColumn + 1]
                else:
                    # Make string of ODD neighbours - Check ranges
                    if (currentColumn - 1) >= 0: # CELL 0 ODD
                        hexNeighbours[0] = oldUniverseList[currentRow][currentColumn - 1]
                        if (currentRow - 1) >= 0: # CELL 1 ODD
                            hexNeighbours[1] = oldUniverseList[currentRow - 1][currentColumn - 1]
                    if (currentColumn + 1) < cellCountX: # CELL 4 ODD
                        hexNeighbours[4] = oldUniverseList[currentRow][currentColumn + 1]
                        if (currentRow + 1) < cellCountY: # CELL 5 ODD
                            hexNeighbours[5] = oldUniverseList[currentRow + 1][currentColumn + 1]

                # Get the new state by sending the currentCell value + string of all neighbours
                hexNeighbours = "".join(hexNeighbours) # join the characters into 1 string
                newUniverseRow += getNewState2DHex(oldUniverseList[currentRow][currentColumn], hexNeighbours)
                universeList[currentRow] = newUniverseRow
            else:
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
