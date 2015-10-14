import random
import numpy as np
import pylab as pl
from operator import itemgetter

''' Print the current generation '''
def printGenerationUniverse(currentTimeStep, cellCountX, cellCountY, normalCharacter, susceptibleCharacter, infectedCharacter):
    print "TimeStep %3i:  " % currentTimeStep
    rowLabel = "  "
    for l in range(cellCountX):
        rowLabel += str(l) + " "
    print rowLabel
    for currentRow in range(cellCountY):
        print "%s %s" % (currentRow, universeList[currentRow].replace('0', normalCharacter + " ").replace('1', susceptibleCharacter + " ").
                         replace('2', infectedCharacter + " "))

''' This method calculates the new state of the cell based on Van Neumann neighborhood '''
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

    if selfCharacter == '0': # If Normal and there is an Infected close, be Susceptible
        if leftCharacter == '2' or rightCharacter == '2' or\
            upperLeftCharacter == '2' or upperRightCharacter == '2' or upperCenterCharacter == '2'\
                or lowerLeftCharacter == '2' or lowerRightCharacter == '2' or lowerCenterCharacter == '2':
            newState = '1'
    else:
        if selfCharacter == '1': # if Susceptible, calculate the probability to be Infected
            betaChance = (2 - np.random.uniform())
            if betaChance > 0 and betaChance < beta:
                newState = '2'
            else:
                newState = '0'
        else:
            if selfCharacter == '2': # if Infected, calculate the probability to be Susceptible 'to recover'
                gammaChance = (1 - np.random.uniform())
                if gammaChance < gamma and gammaChance > 0:
                    newState = '1'

    return newState

# SIS Model Parameters
beta = 1.999#1.4247 # Chance to get S from neighbouring I
gamma = 0.0#12286 # Chance to get from I to R (or normal in our case)
simulationIterations = 100
cellCountX = 33
cellCountY = 33

# Init values
susceptibleCharacter = 'S'
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
    if currentTimeStep == 1:
        printGenerationUniverse(currentTimeStep, cellCountX, cellCountY, normalCharacter, susceptibleCharacter, infectedCharacter)
    #print "TimeStep %3i:  " % currentTimeStep
    #rowLabel = "  "
    #for l in range(cellCountX):
    #    rowLabel += str(l) + " "
    #print rowLabel
    #for currentRow in range(cellCountY):
    #    print "%s %s" % (currentRow, universeList[currentRow].replace('0', normalCharacter + " ").replace('1', susceptibleCharacter + " ").
    print
    #                     replace('2', infectedCharacter + " "))

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
        oldUniverseList.append(extremeEndValue + universeList[currentRow] + extremeEndValue)

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


#Ploting
pl.subplot(3, 1, 1)
pl.plot(map(itemgetter(3), RES), map(itemgetter(2), RES), '-r', label='Infected')
pl.plot(map(itemgetter(3), RES), map(itemgetter(0), RES), '-b', label='Normal')
pl.legend(loc=0)
pl.title('Infected and Normal')
pl.xlabel('Time')
pl.ylabel('Count')

pl.subplot(3, 1, 2)
pl.plot(map(itemgetter(3), RES), map(itemgetter(1), RES), '-r', label='Susceptibles')
pl.plot(map(itemgetter(3), RES), map(itemgetter(0), RES), '-b', label='Normal')
pl.legend(loc=0)
pl.title('Susceptibles and Normal')
pl.xlabel('Time')
pl.ylabel('Count')

pl.subplot(3, 1, 3)
pl.plot(map(itemgetter(3), RES), map(itemgetter(1), RES), '-r', label='Susceptibles')
pl.plot(map(itemgetter(3), RES), map(itemgetter(2), RES), '-b', label='Infected')
pl.legend(loc=0)
pl.title('Susceptibles and Infected')
pl.xlabel('Susceptibles')
pl.ylabel('Infected')

pl.show()