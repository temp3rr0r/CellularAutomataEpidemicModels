####################################################################
###    This is the PYTHON version of program 2.1 from page 19 of   #
### "Modeling Infectious Disease in humans and animals"            #
### by Keeling & Rohani.					    #
###								    #
### It is the simple SIR epidemic without births or deaths.        #
####################################################################

##########################################################################
### Copyright (C) <2008> Ilias Soumpasis                                 #
### ilias.soumpasis@deductivethinking.com                                #
### ilias.soumpasis@gmail.com	                                         #
###                                                                      #
### This program is free software: you can redistribute it and/or modify #
### it under the terms of the GNU General Public License as published by #
### the Free Software Foundation, version 3.                             #
###                                                                      #
### This program is distributed in the hope that it will be useful,      #
### but WITHOUT ANY WARRANTY; without even the implied warranty of       #
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
### GNU General Public License for more details.                         #
###                                                                      #
### You should find a copy of the GNU General Public License at          #
###the Copyrights section or, see http://www.gnu.org/licenses.           #
##########################################################################


import scipy.integrate as spi
import numpy as np
import pylab as pl

beta = .4247
gamma = .14286

populationCount = 10000

TimeStep = 1.0
TimeRange = 70.0
# InitInfected=1e-6
# InitSusceptibles=1-1e-6
InitInfected = 0.0016
InitSusceptibles = 1 - InitInfected
InitVariables = (InitSusceptibles, InitInfected, 0.0, 0.0)


def diff_eqs(INP, t):
    '''The main set of equations'''
    Y = np.zeros((4))
    V = INP

    '''SIR'''
    Y[0] = - beta * V[0] * V[1]
    Y[1] = beta * V[0] * V[1] - gamma * V[1]
    Y[2] = gamma * V[1]

    '''SIS'''
    '''Y[0] = - beta * V[0] * V[1] + gamma * V[1]
	Y[1] = beta * V[0] * V[1] - gamma * V[1]'''

    Y[3] = V[0] + V[1] + V[2]  # Should always be constant
    # Y[3] = Y[0] + Y[1] + Y[2] # Should always be zero
    return Y  # For odeint


t_start = 0.0
t_end = TimeRange
t_inc = TimeStep
t_range = np.arange(t_start, t_end + t_start, t_inc)

RES = spi.odeint(diff_eqs, InitVariables, t_range)

print(RES)

# Ploting
pl.subplot(111)
pl.plot(RES[:, 0] * populationCount, '-b', label='Susceptibles')
pl.plot(RES[:, 2] * populationCount, '-g', label='Recovereds')
pl.plot(RES[:, 1] * populationCount, '-r', label='Infected')
pl.legend(loc=0)
pl.title('Numerical SIR')
pl.xlabel('Time')
pl.ylabel('Susceptibles and Recovereds')

# pl.subplot(212)
# pl.plot(RES[:,0], '-b', label='Susceptibles')
# pl.plot(RES[:,1], '-r', label='Infected')
# pl.legend(loc=0)
# pl.xlabel('Time')
# pl.ylabel('Susceptibles and Infectious')
pl.show()
