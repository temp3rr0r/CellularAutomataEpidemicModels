import random
import numpy as np
import pylab as pl
from operator import itemgetter


def getNewState(previousNeighboursState):
    newState = '0'

    beforeCharacter = previousNeighboursState[0]
    selfCharacter = previousNeighboursState[1]
    afterCharacter = previousNeighboursState[2]

    if selfCharacter == '1' or selfCharacter == '2':
        newState = '2'
    else:
        if beforeCharacter == '1' or afterCharacter == '1' or beforeCharacter == '2' or afterCharacter == 2:
            newState = '1'

    '''neighbours2newstate = {
     '000': '0',
     '001': '1',
     '010': '2',
     '011': '2',
     '100': '1',
     '101': '1',
     '110': '2',
     '111': '2',

     '012': '2',
     '021': '2',
     '102': '1',
     '120': '2',
     '201': '1',
     '210': '2',

     '002': '1',
     '020': '2',
     '022': '2',
     '200': '1',
     '202': '1',
     '220': '2',
     '222': '2',

     '112': '2',
     '121': '2',
     '122': '2',
     '211': '2',
     '212': '2',
     '221': '2',
     '222': '2',
     }'''
    return newState

susceptibleCharacter = 'S'
infectedCharacter ='I'
normalCharacter = ' '
maxgenerations = 15
cellcount = 30
offendvalue = '0'

t_start = 0.0
t_end = maxgenerations
t_inc = 1
t_range = np.arange(t_start, t_end + t_start, t_inc)

universe = ''.join(random.choice('000000001') for i in range(cellcount))

InitSusceptibles = 0.0
InitInfected = universe.count('2')
InitVariables = [InitSusceptibles, InitInfected, 0.0, 0.0]

RES = [InitVariables]

neighbours2newstate = {
 '000': '0',
 '001': '1',
 '010': '2',
 '011': '2',
 '100': '1',
 '101': '1',
 '110': '2',
 '111': '2',

 '012': '2',
 '021': '2',
 '102': '1',
 '120': '2',
 '201': '1',
 '210': '2',

 '002': '1',
 '020': '2',
 '022': '2',
 '200': '1',
 '202': '1',
 '220': '2',
 '222': '2',

 '112': '2',
 '121': '2',
 '122': '2',
 '211': '2',
 '212': '2',
 '221': '2',
 '222': '2',
 }
 
for i in range(maxgenerations):
    print "Generation %3i:  %s" % ( i,
          universe.replace('0', normalCharacter).replace('1', susceptibleCharacter).replace('2', infectedCharacter ))


    RES.append([universe.count('0'), universe.count('1'), universe.count('2'), i])

    universe = offendvalue + universe + offendvalue
    universe = ''.join(
        neighbours2newstate[
            universe[i:i+3]
        ] for i in range(cellcount)
    )

print RES

print getNewState('000')

#Ploting
pl.subplot(211)
pl.plot(map(itemgetter(3), RES), map(itemgetter(1), RES), '-r', label='Susceptibles')
pl.plot(map(itemgetter(3), RES), map(itemgetter(0), RES), '-b', label='Normal')
pl.legend(loc=0)
pl.title('Susceptibles and Normal')
pl.xlabel('Time')
pl.ylabel('Count')


pl.subplot(212)
pl.plot(map(itemgetter(3), RES), map(itemgetter(2), RES), '-r', label='Infected')
pl.plot(map(itemgetter(3), RES), map(itemgetter(0), RES), '-b', label='Normal')
pl.legend(loc=0)
pl.title('Infected and Normal')
pl.xlabel('Time')
pl.ylabel('Count')
pl.show()
