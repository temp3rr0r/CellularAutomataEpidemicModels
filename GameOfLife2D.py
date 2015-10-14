import random
import numpy as np
import pylab as pl
from operator import itemgetter
from copy import deepcopy

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
        if leftCharacter == '2' or rightCharacter == '2' or upperLeftCharacter == '2' or upperRightCharacter == '2'\
                or lowerLeftCharacter == '2' or lowerRightCharacter == '2' or upperCenterCharacter == '2' or lowerCenterCharacter == '2':
            newState = '1'
    else:
        if selfCharacter == '1': # if Susceptible, calculate the probability to be Infected
            if (2 - round(np.random.uniform(0.0, 1.0), 10)) <= beta:
                newState = '2'
            else:
                newState = '0'
        else:
            if selfCharacter == '2': # if Infected, calculate the probability to be Susceptible 'to recover'
                if (1 - round(np.random.uniform(0.0, 1.0), 10)) <= gamma:
                    newState = '1'

    return newState

# Parameters
beta = 1.4247 # Chance to get S from neighbouring I
gamma = 0.14286 # Chance to get from I to R (or normal in our case)

# Init values
susceptibleCharacter = 'S'
infectedCharacter ='I'
normalCharacter = '_'
extremeEndValue = '0'
maxGenerations = 30

cellX = 10
cellY = 10

timeStart = 0.0
timeEnd = maxGenerations
timeStep = 1
timeRange = np.arange(timeStart, timeEnd + timeStart, timeStep)

universeList = []

# Randomise first state
for j in range(cellY):
    universe = ''.join(random.choice('000000002') for i in range(cellX))
    universeList.append(universe)

InitSusceptibles = 0.0
InitInfected = 0.0
InitVariables = [InitSusceptibles, InitInfected, 0.0, 0.0]

RES = [InitVariables]
 
for i in range(maxGenerations):

    # Print the current generation
    print "Generation %3i:  " % i
    rowLabel = "  "
    for l in range(cellX):
        rowLabel += str(l) + " "
    print rowLabel
    for k in range(cellY):
        print "%s %s" % (k, universeList[k].replace('0', normalCharacter + " ").replace('1', susceptibleCharacter + " ").replace('2', infectedCharacter + " "))

    # Store the counts of I, S and the time iteration
    zeroCount = 0
    oneCount = 0
    twoCount = 0
    for k in range(cellY):
        zeroCount += universeList[k].count('0')
        oneCount += universeList[k].count('1')
        twoCount += universeList[k].count('2')
    RES.append([zeroCount, oneCount, twoCount, i])

    # Put extreme ends neighbouring cells temporarily
    oldUniverseList = []
    for k in range(cellY):
        oldUniverseList.append(extremeEndValue + universeList[k] + extremeEndValue)

    for k in range(cellY):
        newUniverseRow = ''
        for j in range(cellX):
            upperRowNeighbours = '000'
            lowerRowNeighbours = '000'
            currentRowNeighbours = oldUniverseList[k][j:j+3]
            if (k - 1) >= 0:
                upperRowNeighbours = oldUniverseList[k-1][j:j+3]
            if (k + 1) < cellY:
                lowerRowNeighbours = oldUniverseList[k+1][j:j+3]

            newUniverseRow += getNewState2D(currentRowNeighbours, upperRowNeighbours, lowerRowNeighbours)
            universeList[k] = newUniverseRow

print RES


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