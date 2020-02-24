""" A test 2D CA model for SIR without mortality or birth """

import random
import numpy as np
import pylab as pl


def printGenerationUniverse(currentTimeStep, cellCountX, cellCountY, normalCharacter, susceptibleCharacter,
                            infectedCharacter, recoveredCharacter):
    """
    Print the current generation.
    :param currentTimeStep:
    :param cellCountX:
    :param cellCountY:
    :param normalCharacter:
    :param susceptibleCharacter:
    :param infectedCharacter:
    :param recoveredCharacter:
    :return:
    """
    print("TimeStep %3i:  " % currentTimeStep)
    rowLabel = "  "
    for l in range(cellCountX):
        rowLabel += str(l) + " "
    print(rowLabel)
    for currentRow in range(cellCountY):
        print("%s %s" % (currentRow, universeList[currentRow].replace('0', normalCharacter + " ").replace('1',
                                                                                                          susceptibleCharacter + " ").
                         replace('2', infectedCharacter + " ").replace('3', recoveredCharacter + " ")))


''' This method calculates the new state of the cell based on Von Neumann neighborhood '''


def getNewState2D(currentRowNeighbours, upperRowNeighbours, lowerRowNeighbours):
    newState = '0'

    leftCharacter = currentRowNeighbours[0]
    selfCharacter = currentRowNeighbours[1]
    rightCharacter = currentRowNeighbours[2]

    upperLeftCharacter = upperRowNeighbours[0]
    upperCenterCharacter = upperRowNeighbours[1]
    upperRightCharacter = upperRowNeighbours[2]

    lowerLeftCharacter = lowerRowNeighbours[0]
    lowerCenterCharacter = lowerRowNeighbours[1]
    lowerRightCharacter = lowerRowNeighbours[2]

    newState = selfCharacter

    if selfCharacter == '0':  # If Normal and there is an Infected close, be Susceptible
        if leftCharacter == '2' or rightCharacter == '2' or \
                upperLeftCharacter == '2' or upperRightCharacter == '2' or upperCenterCharacter == '2' \
                or lowerLeftCharacter == '2' or lowerRightCharacter == '2' or lowerCenterCharacter == '2':
            newState = '1'
    elif selfCharacter == '1':  # if Susceptible, calculate the probability to be Infected
        # betaChance = (2 - np.random.normal(0.5, 1.0)) # NORMAL
        betaChance = (2 - np.random.uniform())  # UNIFORM
        # betaChance = (2 - (np.random.poisson(2) % 10) * 0.1) # POISSON
        if betaChance > 0 and betaChance < beta:
            newState = '2'
        else:
            newState = '0'
    elif selfCharacter == '2':  # if Infected, calculate the probability to be Recovered 'to recover'
        gammaChance = (1 - np.random.normal(0.5, 1.0))  # NORMAL
        # gammaChance = (1 - np.random.uniform()) # UNIFORM
        # gammaChance = (1 - (np.random.poisson(2) % 10) * 0.1) # POISSON

        if gammaChance < gamma and gammaChance > 0:
            newState = '3'
    elif selfCharacter == '3':  # Recovered, immune for a while
        rhoChance = (1 - np.random.normal(0.5, 1.0))  # NORMAL
        # rhoChance = (1 - np.random.uniform()) # UNIFORM
        # rhoChance = (1 - (np.random.poisson(2) % 10) * 0.1) # POISSON

        if rhoChance < rho and rhoChance > 0:
            newState = '0'

    return newState


# SIS Model Parameters
beta = 1.2247  # Chance to get S from neighbouring I
gamma = 0.015  # Chance to get from I to R (or normal in our case)
rho = 0.0  # Chance ot get from R to normal (Loss of immunity rate)
simulationIterations = 300
cellCountX = 10
cellCountY = 10

# Init values
susceptibleCharacter = 'S'
recoveredCharacter = 'R'
infectedCharacter = 'I'
normalCharacter = '_'
extremeEndValue = '0'
timeStart = 0.0
timeEnd = simulationIterations
timeStep = 1
timeRange = np.arange(timeStart, timeEnd + timeStart, timeStep)
universeList = []

# Randomise first state
for currentColumn in range(cellCountY):
    universe = ''.join(random.choice('000002') for universeColumn in range(cellCountX))
    universeList.append(universe)

# TODO: Fix init state vars
InitSusceptibles = 0.0
InitInfected = 0.0
InitRecovered = 0.0
InitVariables = [InitSusceptibles, InitInfected, 0.0, 0.0, 0.0]

RES = [InitVariables]

# Main Execution loop
for currentTimeStep in range(simulationIterations):

    # Print the current generation
    if currentTimeStep < 4:
        printGenerationUniverse(currentTimeStep, cellCountX, cellCountY, normalCharacter, susceptibleCharacter,
                                infectedCharacter, recoveredCharacter)

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
    for currentRow in range(cellCountY):
        oldUniverseList.append(extremeEndValue + universeList[currentRow] + extremeEndValue)

    for currentRow in range(cellCountY):
        newUniverseRow = ''
        for currentColumn in range(cellCountX):
            upperRowNeighbours = '000'
            lowerRowNeighbours = '000'
            currentRowNeighbours = oldUniverseList[currentRow][currentColumn:currentColumn + 3]
            if (currentRow - 1) >= 0:
                upperRowNeighbours = oldUniverseList[currentRow - 1][currentColumn:currentColumn + 3]
            if (currentRow + 1) < cellCountY:
                lowerRowNeighbours = oldUniverseList[currentRow + 1][currentColumn:currentColumn + 3]

            newUniverseRow += getNewState2D(currentRowNeighbours, upperRowNeighbours, lowerRowNeighbours)
            universeList[currentRow] = newUniverseRow

# print RES
RES = np.array(RES)

# Ploting
pl.subplot(4, 1, 1)
pl.plot(RES[:, 4], RES[:, 2], '-r', label='Infected')
pl.plot(RES[:, 4], RES[:, 0], '-b', label='Normal')
pl.legend(loc=0)
pl.title('Infected and Normal')
pl.xlabel('Time')
pl.ylabel('Count')

pl.subplot(4, 1, 2)
pl.plot(RES[:, 4], RES[:, 1], '-r', label='Susceptibles')
pl.plot(RES[:, 4], RES[:, 0], '-b', label='Normal')
pl.legend(loc=0)
pl.title('Susceptibles and Normal')
pl.xlabel('Time')
pl.ylabel('Count')

pl.subplot(4, 1, 3)
pl.plot(RES[:, 4], RES[:, 1], '-r', label='Susceptibles')
pl.plot(RES[:, 4], RES[:, 2], '-b', label='Infected')
pl.legend(loc=0)
pl.title('Susceptibles and Infected')
pl.xlabel('Susceptibles')
pl.ylabel('Infected')

pl.subplot(4, 1, 4)
pl.plot(RES[:, 4], RES[:, 3], '-r', label='Recovered')
pl.plot(RES[:, 4], RES[:, 0], '-b', label='Normal')
pl.legend(loc=0)
pl.title('Recovered and Normal')
pl.xlabel('Time')
pl.ylabel('Count')

pl.show()
