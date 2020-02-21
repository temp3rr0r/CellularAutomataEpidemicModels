####################################################################
###    This is the PYTHON version of program 7.4 from page 260 of  #
### "Modeling Infectious Disease in humans and animals"            #
### by Keeling & Rohani.										   #
###																   #
### It is the forest-fire model on a grid of size NxN.             #
### A zero time-step means that asynchronous updating is used.     #
####################################################################

###################################
### Written by Ilias Soumpasis    #
### ilias.soumpasis@ucd.ie (work) #
### ilias.soumpasis@gmail.com	  #
###################################

import scipy.integrate as spi
import numpy as np
import pylab as pl
import time, os

### Select if you want to make a video (faster way) 
# video=1
### or just0in-time plotting
video = 0
t = time.time()

N = 25
tau = 1.0
gamma = 0  # 0.1
nu = 0.01
epsilon = 1e-4
timestep = 0.5
ND = MaxTime = 1000

Grid = 2 * np.ones((N, N), dtype=np.integer)
Grid[int(np.ceil((N - 1) * np.random.uniform(size=1))[0]), int(np.ceil((N - 1) * np.random.uniform(size=1))[0])] = 3
t = 0
i = 1
T = []
X = []
Y = []


def diff_eqs(INP, t):
    INF = np.zeros((N, N))
    SUS = np.zeros((N, N))
    EMP = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if INP[i][j] == 1: EMP[i][j] = 1
            if INP[i][j] == 2: SUS[i][j] = 1
            if INP[i][j] == 3: INF[i][j] = 1

    Infecteds = INF
    Susceptibles = SUS
    X.append(sum(sum(Susceptibles)))
    Y.append(sum(sum(Infecteds)))  # T[i]=t

    Inf_Nbrs = Infecteds[:, np.hstack((np.arange(1, N), 0))] + \
               Infecteds[np.hstack((np.arange(1, N), 0)), :] + \
               Infecteds[:, np.hstack((49, np.arange(49)))] + \
               Infecteds[np.hstack((49, np.arange(49))), :]

    if (timestep == 0):  # asynchronous updating
        Rates = nu * EMP + gamma * Infecteds + tau * Susceptibles * (Inf_Nbrs + epsilon)
        vectorRates = np.reshape(Rates, N * N)
        Total_Rates = sum(vectorRates)
        Cum_Rates = np.cumsum(vectorRates)
        step = -np.log(np.random.uniform(size=(N, N))) / Total_Rates
        R = rand(1, 1) * Total_Rates
        Event = min(pl.find(R < Cum_Rates))
        S[Event] = np.mod(S[Event], 3) + 1
    else:
        Rates = nu * EMP + gamma * Infecteds + tau * Susceptibles * (Inf_Nbrs + epsilon)
        R = timestep * Rates - np.random.uniform(size=(N, N))
        S = np.mod(Grid - 1 + np.ceil(R), 3) + 1
        step = timestep

    return S, X, Y, timestep


if video == 1:
    if os.path.exists('movie') == True:
        pass
    else:
        os.mkdir('movie')
    k = 0
    while t <= ND:
        [Grid, X, Y, timestep] = diff_eqs(Grid, timestep)
        t += timestep
        T.append(t)
        k += 1

        pl.clf()
        pl.subplot(211)
        pl.pcolor(Grid, cmap=pl.cm.jet)
        pl.title('Forest-Fire Model')

        pl.subplot(413)
        pl.plot(T, X, color='g')
        pl.ylabel('Susceptible')
        pl.subplot(414)
        pl.plot(T, Y, color='r')
        pl.ylabel('Infected')
        pl.xlabel('Time (days)')
        pl.savefig("movie/frame_%04d.png" % k)
        print(k)

    ## You will mencoder from mplayer for this to work
    ## With windows you have to modify the path
    ## With linux if you have mencoder istall usually it should work
    ## Format is windows media player - plays on windows
    ## You could try other formats also
    print('Please wait... Converting pictures to avis....')
    ## Select different video speed
    #    os.system('mencoder "mf://movie/*.png" -mf fps=5:type=png -ovc lavc -lavcopts vcodec=wmv1 -of avi -o movie/movie_very_slow.avi')
    #    os.system('mencoder "mf://movie/*.png" -mf fps=10:type=png -ovc lavc -lavcopts vcodec=wmv1 -of avi -o movie/movie_slow.avi')
    os.system(
        'mencoder "mf://movie/*.png" -mf fps=25:type=png -ovc lavc -lavcopts vcodec=wmv1 -of avi -o movie/movie_fast.avi')
    print('Convertion completed. Hope it worked...')
    ## Delete images to save work space
    os.system('rm movie/*.png')

    print("Operation took %g seconds" % (time.time() - t))

else:
    ### You could also try plotting at each step but it is slow
    k = 0
    pl.ion()
    while t <= ND:
        [Grid, X, Y, timestep] = diff_eqs(Grid, timestep)
        t += timestep
        T.append(t)
        k += 1

        pl.clf()
        pl.subplot(211)
        pl.pcolor(Grid, cmap=pl.cm.jet)
        pl.title('Forest-Fire Model')

        pl.subplot(413)
        pl.plot(T, X, color='g')
        pl.ylabel('Susceptible')

        pl.subplot(414)
        pl.plot(T, Y, color='r')
        pl.ylabel('Infected')
        pl.xlabel('Time (days)')
        print(k)
        pl.draw()
    pl.ioff()
    pl.show()
