""" Distribution function checking script """

import numpy as np
import matplotlib.pyplot as plt
s = []

#sigmaChance = np.random.uniform() # UNIFORM
#sigmaChance = np.random.normal(.5, .1) # NORMAL
#sigmaChance = np.random.poisson(2) * .1 # POISSON
#sigmaChance = (np.random.binomial(20, .5, 100) % 10) * 0.1 # BINOMIAL

# UNIFORM
#for i in range(1000):
#    s.append(np.random.uniform())

# POISSON
#s = np.random.poisson(2, 10000) * 0.1

# NORMAL
#for i in range(10000):
#    s = abs(np.random.normal(.5, .1, 1000)) # NORMAL

# BINOMIAL
#s = (np.random.binomial(20, .5, 100) % 10) * 0.1

# MONTE CARLO METHOD
def monteCarlo():
    r1 = 0.0
    while(True):
        # Pick a random value.
        r1 = np.random.uniform()
        if np.random.uniform() < r1:
            return r1

for i in range(10000):
   s.append(monteCarlo())


print s
# Plot
count, bins, ignored = plt.hist(s, 14, normed=True)
plt.show()