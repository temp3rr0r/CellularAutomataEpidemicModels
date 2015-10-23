####################################################################
###    This is the PYTHON version of program 7.3 from page 256 of  #
### "Modeling Infectious Disease in humans and animals"            #
### by Keeling & Rohani.										   #
###																   #
### It is the SIR epidemic on an nxn lattice with coupling (rho)   #
### to 4 nearest neighbour. nI defines the number of lattice sites #
### (chosen randomly) that start with some infection.              #
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
#video=1
### or just0in-time plotting
video=0
t = time.time()

n=25;
beta=1#.42;
gamma=0#0.14;
mu=0.0001;
rho=0.1;
X0=0.1;
nI=4.;
N0=1.0;
nu=mu
timestep=1.;
ND=MaxTime=500#2910;
C=np.arange(0.0, 1.0, 0.001)
X=X0*np.ones((n,n)); Y=np.zeros(n*n); 
ind=np.ceil(n*n*np.random.uniform(size=nI))
for i in range(len(ind)):
    Y[ind[i]]=0.001*X0;

INPUT1=np.hstack((X0*np.ones((n*n)),Y))

Y3=Y
Y=np.reshape(Y, ((n,n)))
Y2=Y

INPUT3=np.hstack((X,Y));

INPUT2=np.reshape(INPUT3, ((2*n*n,1)))

for i in range(len(INPUT1)):
    INPUT1[i]=INPUT2[i]

INPUT=INPUT1
ndem=np.zeros((n,n))
Size=n
N=N0
### Note the size loop
for i in range(Size):
    for j in range(Size):
        ndem[i][j]=(1-4*rho)*N
        if i>0 : ndem[i][j] += rho*N
        if i<(Size-1) : ndem[i][j] += rho*N
        if j>0 : ndem[i][j] += rho*N
        if j<(Size-1) : ndem[i][j] += rho*N
            
def diff_eqs(INP,t):
    V=INP
    Y=np.zeros(2*n*n)

    ### internal dynamics
    for i in range(Size):
        for j in range(Size):
            ss=i+j*Size*2
            ii=Size+i+j*Size*2
            Y[ss]=nu - beta*(1-4*rho)*V[ss]*V[ii]/ndem[i][j] - mu * V[ss]
            Y[ii]=beta*(1-4*rho)*V[ss]*V[ii]/ndem[i][j] - (gamma + mu) * V[ii]
        
            ### Interactions with four neighbours
            if i>0: 
                FoI = beta*V[ss]*rho*V[ii-1]/ndem[i][j]
                Y[ss]-=FoI
                Y[ii]+=FoI
            
            if i<(Size-1):
                FoI = beta*V[ss]*rho*V[ii+1]/ndem[i][j]
                Y[ss]-=FoI
                Y[ii]+=FoI
            
            if j>0:
                FoI = beta*V[ss]*rho*V[ii-Size*2]/ndem[i][j]
                Y[ss]-=FoI
                Y[ii]+=FoI
            
            if j<(Size-1):
                FoI = beta*V[ss]*rho*V[ii+Size*2]/ndem[i][j]
                Y[ss]-=FoI
                Y[ii]+=FoI
            
    return Y


ola=np.zeros((n*n), dtype=np.integer)
for i in range(Size):
    for j in range(Size):
        ola[i*n+j]=i*Size*2+j

ola1=ola+n
tcS=[(n*n*X0)]
tcI=[sum(Y3[range(n*n)])]
tc22=np.zeros((n,n))
if video==1:
    if os.path.exists('movie')==True: pass 
    else: os.mkdir('movie')

    for k in range(ND):
        t_range = np.arange(2.0)	
        RES = spi.odeint(diff_eqs,INPUT,t_range)
        INPUT=RES[-1]

        tcS.append(sum(RES[-1][ola]))
        tcI.append(sum(RES[-1][ola1]))

        if k%1==0:
            pl.clf()
            tc22=np.reshape(RES[-1][ola1], (n,n))
            pl.subplot(211)
            pl.pcolor(tc22, cmap=pl.cm.spectral)
            pl.title('Coupled Lattice Model')
            pl.colorbar()	

            pl.subplot(413)
            pl.plot(tcS, color='b')
            pl.ylabel('Susceptible')
            pl.subplot(414)
            pl.plot(tcI, color='r')
            pl.ylabel('Infected')
            pl.xlabel('Time (days)')
            pl.savefig("movie/frame_%04d.png" %k)
            ## watch the progress
            print k

    ## You will mencoder from mplayer for this to work
    ## With windows you have to modify the path
    ## With linux if you have mencoder istall usually it should work
    ## Format is windows media player - plays on windows
    ## You could try other formats also
    print('Please wait... Converting pictures to avis....')
    ## Select different video speed
#    os.system('mencoder "mf://movie/*.png" -mf fps=5:type=png -ovc lavc -lavcopts vcodec=wmv1 -of avi -o movie/movie_very_slow.avi')
#    os.system('mencoder "mf://movie/*.png" -mf fps=10:type=png -ovc lavc -lavcopts vcodec=wmv1 -of avi -o movie/movie_slow.avi')
    os.system('mencoder "mf://movie/*.png" -mf fps=25:type=png -ovc lavc -lavcopts vcodec=wmv1 -of avi -o movie/movie_fast.avi')
    print('Convertion completed. Hope it worked...')
    ## Delete images to save work space
    os.system('rm movie/*.png')

    print "Operation took %g seconds" % (time.time()-t)

else:
    ### You could also try plotting at each step but it is slow
    pl.ion()
    for k in range(ND):
        t_range = np.arange(2.0)	
        RES = spi.odeint(diff_eqs,INPUT,t_range)
        INPUT=RES[-1]

        tcS.append(sum(RES[-1][ola]))
        tcI.append(sum(RES[-1][ola1]))
        
        ### Changing the k%50 parameter you change the frames you are watching
        ###  With 1 you can see all the graphs
        if k%10==0:
            pl.clf()
            tc22=np.reshape(RES[-1][ola1], (n,n))
            pl.subplot(211)
            pl.pcolor(tc22, cmap=pl.cm.spectral)
            pl.title('Coupled Lattice Model')
            pl.colorbar()	

            pl.subplot(413)
            pl.plot(tcS, color='b')
            pl.ylabel('Susceptible')
            
            pl.subplot(414)
            pl.plot(tcI, color='r')
            pl.ylabel('Infected')
            pl.xlabel('Time (days)')
            
            ### watch the progress
            print k
            pl.draw()
    pl.ioff()
    pl.show()