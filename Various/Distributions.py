""" Distribution function checking script """

import numpy as np
#s = np.random.poisson(20, 10000)
s = (np.random.poisson(1, 10000) % 10) * 0.1
import matplotlib.pyplot as plt
count, bins, ignored = plt.hist(s, 14, normed=True)
plt.show()