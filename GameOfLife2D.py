import random
import numpy as np
import pylab as pl
from operator import itemgetter

def getNewState2D(currentRowNeighbours, upperRowNeighbours, lowerRowNeighbours):
    newState = '0'

    leftCharacter = currentRowNeighbours[0]
    selfCharacter = currentRowNeighbours[1]
    rightCharacter = currentRowNeighbours[2]

    upperLeftCharacter = upperRowNeighbours[0]
    upperCenterCharacter = upperRowNeighbours[0]
    upperRightCharacter = upperRowNeighbours[0]

    lowerLeftCharacter = lowerRowNeighbours[0]
    lowerCenterCharacter = lowerRowNeighbours[0]
    lowerRightCharacter = lowerRowNeighbours[0]

    newState = selfCharacter

    if selfCharacter == '0': # If Normal and there is an infected close, be Susceptible
        if leftCharacter == '2' or rightCharacter == '2':
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

def getNewState(previousNeighboursState):
    newState = '0'

    leftCharacter = previousNeighboursState[0]
    selfCharacter = previousNeighboursState[1]
    rightCharacter = previousNeighboursState[2]

    newState = selfCharacter

    if selfCharacter == '0': # If Normal and there is an infected close, be Susceptible
        if leftCharacter == '2' or rightCharacter == '2':
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

beta = 1.4247 # Chance to get S from neighbouring I
gamma = 0.14286 # Chance to get from I to R (or normal in our case)
susceptibleCharacter = 'S'
infectedCharacter ='I'
normalCharacter = ' '
maxgenerations = 30

cellX = 10
cellY = 10

extremeEndValue = '0'

t_start = 0.0
t_end = maxgenerations
t_inc = 1
t_range = np.arange(t_start, t_end + t_start, t_inc)

universeList = []

# Init, get random I
for j in range(cellY):
    universe = ''.join(random.choice('000000002') for i in range(cellX))
    universeList.append(universe)

InitSusceptibles = 0.0
InitInfected = 0.0
InitVariables = [InitSusceptibles, InitInfected, 0.0, 0.0]

RES = [InitVariables]
 
for i in range(maxgenerations):

    # Print the current generation
    print "Generation %3i:  " % i
    for k in range(cellY):
        print universeList[k].replace('0', normalCharacter).replace('1', susceptibleCharacter).replace('2', infectedCharacter)

    # Store the counts of I, S and the time iteration
    zeroCount = 0
    oneCount = 0
    twoCount = 0
    for k in range(cellY):
        zeroCount += universeList[k].count('0')
        oneCount += universeList[k].count('1')
        twoCount += universeList[k].count('2')
    RES.append([zeroCount, oneCount, twoCount, i])

    # Calculate the next generation
    for k in range(cellY):
        universeList[k] = extremeEndValue + universeList[k] + extremeEndValue

        #universeList[k] = ''.join(
        #    getNewState(
        #        universeList[k][i:i+3]
        #    ) for i in range(cellX)

        # newUniverseList = universeList
        newUniverseList = ''
        for i in range(cellX):
            upperRowNeighbours = '000'
            lowerRowNeighbours = '000'
            currentRowNeighbours = universeList[k][i:i+3]
            if (k - 1) >= 0:
                upperRowNeighbours = universeList[k-1][i:i+3]
            if (k + 1) < cellY:
                lowerRowNeighbours = universeList[k+1][i:i+3]
            newUniverseList += getNewState2D(currentRowNeighbours, upperRowNeighbours, lowerRowNeighbours)
        universeList[k] = newUniverseList

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