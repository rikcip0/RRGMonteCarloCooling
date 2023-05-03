import matplotlib.pyplot as plt
import numpy as np
import sys
import os

n_stories=10
n = int(sys.argv[1])
print(n+1)
path = os.path.abspath('..\\Data\\LastRun')

with open(path + '\\McStories.txt', 'r') as file:
    dataLines = file.readlines().filter(lambda x: not x.startswith('#'))

with open(path + '\\McStories.txt', 'r') as file:
    paramsLines = file.readlines().filter(lambda x: x.startswith('#'))

data = np.genfromtxt(dataLines, delimiter=' ')
times = data[:, 2]
energies = data[:, 1]
magnetizations = data[:, 0]

plt.plot(times, magnetizations, label='magnetization')
#plt.plot(times[:100000], energies[:100000], label='energy')
#plt.xscale('log')
plt.legend()
plt.title('Titolo del {} grafico' .format(n))
plt.savefig(path+"\\Magnetizations.png")

plt.show()