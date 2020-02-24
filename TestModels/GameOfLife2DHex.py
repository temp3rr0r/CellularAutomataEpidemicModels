""" An ascii 2D CA model for SEIRS without mortality or birth """

import random

import numpy as np
import pylab as pl


def printGenerationUniverseHex(currentTimeStep, cellCountX, cellCountY, normalCharacter, susceptibleCharacter,
                               infectedCharacter):
    print("TimeStep %3i:  " % currentTimeStep)
    rowLabel = "   "
    for l in range(cellCountX):
        rowLabel += str(l) + " "
    print(rowLabel)
    for currentRow in range(cellCountY):
        cellGap = ''
        if currentRow % 2 == 1:
            cellGap = '  '
        print("%s%s  %s" % (currentRow, cellGap,
                            universeList[currentRow].replace('0', normalCharacter + " ").replace('1',
                                                                                                 susceptibleCharacter + " ").
                            replace('2', infectedCharacter + " ")))


def printGenerationUniverse(currentTimeStep, cellCountX, cellCountY, normalCharacter, susceptibleCharacter,
                            infectedCharacter):
    """
    Print the current generation.
    :param currentTimeStep:
    :param cellCountX:
    :param cellCountY:
    :param normalCharacter:
    :param susceptibleCharacter:
    :param infectedCharacter:
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
                         replace('2', infectedCharacter + " ")))


# This method calculates the new state of the cell based on Von Neumann HEX neighborhood
def getNewState2DHex(selfCharacter, hexNeighbours):
    newState = '0'
    newState = selfCharacter

    if selfCharacter == '0':  # If Normal and there is an Infected close, be Susceptible
        if hexNeighbours.count('2') > 0:
            newState = '1'
    else:
        if selfCharacter == '1':  # if Susceptible, calculate the probability to be Infected
            # betaChance = (2 - np.random.normal(0.5, 1.0)) # NORMAL
            # betaChance = (2 - np.random.uniform()) # UNIFORM
            betaChance = (2 - (np.random.poisson(1) % 10) * 0.1)  # POISSON
            if 0 < betaChance < beta:
                newState = '2'
            else:
                newState = '0'
        else:
            if selfCharacter == '2':  # if Infected, calculate the probability to be Susceptible 'to recover'
                # gammaChance = (1 - np.random.normal(0.5, 1.0)) # NORMAL
                # gammaChance = (1 - np.random.uniform()) # UNIFORM
                gammaChance = (1 - (np.random.poisson(1) % 10) * 0.1)  # POISSON

                if gammaChance < gamma and gammaChance > 0:
                    newState = '1'

    return newState


# SIS Model Parameters
beta = 1.4247  # Chance to get S from neighbouring I
gamma = 0.14286  # Chance to get from I to R (or normal in our case)
simulationIterations = 100
cellCountX = 33
cellCountY = 33

# Init values
susceptibleCharacter = 'S'
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
    universe = ''.join(random.choice('000000002') for universeColumn in range(cellCountX))
    universeList.append(universe)

# TODO: Fix init state vars
InitSusceptibles = 0.0
InitInfected = 0.0
InitVariables = [InitSusceptibles, InitInfected, 0.0, 0.0]

RES = [InitVariables]

# Main Execution loop
for currentTimeStep in range(simulationIterations):

    # Print the current generation
    if currentTimeStep < 4:
        printGenerationUniverse(currentTimeStep, cellCountX, cellCountY, normalCharacter, susceptibleCharacter,
                                infectedCharacter)

    # Store the counts of I, S and the time iteration
    zeroCount = 0
    oneCount = 0
    twoCount = 0
    for currentRow in range(cellCountY):
        zeroCount += universeList[currentRow].count('0')
        oneCount += universeList[currentRow].count('1')
        twoCount += universeList[currentRow].count('2')
    RES.append([zeroCount, oneCount, twoCount, currentTimeStep])

    # Put extreme ends neighbouring cells temporarily on the old universe
    oldUniverseList = []
    for currentRow in range(cellCountY):
        oldUniverseList.append(universeList[currentRow])

    for currentRow in range(cellCountY):
        newUniverseRow = ''
        for currentColumn in range(cellCountX):

            # HEX
            hexNeighbours = list("000000")  # list of characters

            # Top/bottom CELL 2 & CELL 3 - Same for ODD and EVEN
            if (currentRow - 1) >= 0:  # CELL 2
                hexNeighbours[2] = oldUniverseList[currentRow - 1][currentColumn]
            if (currentRow + 1) < cellCountY:  # CELL 3
                hexNeighbours[3] = oldUniverseList[currentRow + 1][currentColumn]

            if (currentColumn % 2 == 0):
                if (currentColumn - 1) >= 0:  # CELL 1 EVEN
                    hexNeighbours[1] = oldUniverseList[currentRow][currentColumn - 1]
                    if (currentRow - 1) >= 0:  # CELL 0 EVEN
                        hexNeighbours[0] = oldUniverseList[currentRow - 1][currentColumn - 1]
                if (currentColumn + 1) < cellCountX:  # CELL 5 EVEN
                    hexNeighbours[5] = oldUniverseList[currentRow][currentColumn + 1]
                    if (currentRow - 1) >= 0:  # CELL 4 EVEN
                        hexNeighbours[4] = oldUniverseList[currentRow - 1][currentColumn + 1]
            else:
                # Make string of ODD neighbours - Check ranges
                if (currentColumn - 1) >= 0:  # CELL 0 ODD
                    hexNeighbours[0] = oldUniverseList[currentRow][currentColumn - 1]
                    if (currentRow - 1) >= 0:  # CELL 1 ODD
                        hexNeighbours[1] = oldUniverseList[currentRow - 1][currentColumn - 1]
                if (currentColumn + 1) < cellCountX:  # CELL 4 ODD
                    hexNeighbours[4] = oldUniverseList[currentRow][currentColumn + 1]
                    if (currentRow + 1) < cellCountY:  # CELL 5 ODD
                        hexNeighbours[5] = oldUniverseList[currentRow + 1][currentColumn + 1]

            # Get the new state by sending the currentCell value + string of all neighbours
            hexNeighbours = "".join(hexNeighbours)  # join the characters into 1 string
            newUniverseRow += getNewState2DHex(oldUniverseList[currentRow][currentColumn], hexNeighbours)
            universeList[currentRow] = newUniverseRow

# print RES
RES = np.array(RES)

# Ploting
pl.subplot(3, 1, 1)
pl.plot(RES[:, 3], RES[:, 2], '-r', label='Infected')
pl.plot(RES[:, 3], RES[:, 0], '-b', label='Normal')
pl.legend(loc=0)
pl.title('Infected and Normal')
pl.xlabel('Time')
pl.ylabel('Count')

pl.subplot(3, 1, 2)
pl.plot(RES[:, 3], RES[:, 1], '-r', label='Susceptibles')
pl.plot(RES[:, 3], RES[:, 0], '-b', label='Normal')
pl.legend(loc=0)
pl.title('Susceptibles and Normal')
pl.xlabel('Time')
pl.ylabel('Count')

pl.subplot(3, 1, 3)
pl.plot(RES[:, 3], RES[:, 1], '-r', label='Susceptibles')
pl.plot(RES[:, 3], RES[:, 2], '-b', label='Infected')
pl.legend(loc=0)
pl.title('Susceptibles and Infected')
pl.xlabel('Susceptibles')
pl.ylabel('Infected')

pl.show()
