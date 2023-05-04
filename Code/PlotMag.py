import matplotlib.pyplot as plt
import numpy as np
import sys
import os

path = os.path.abspath('..\\Data\\LastRun')

with open(path+'\\McStories.txt', 'r') as f:
    lines = f.readlines()  # Legge tutte le righe in una lista
    dataLines = filter(lambda x: not x.startswith('#'), lines)
    paramsLines =  filter(lambda x: x.startswith('#'), lines)

data = np.genfromtxt(dataLines, delimiter=' ')
times = data[:, 2]
energies = data[:, 1]
magnetizations = data[:, 0]

plt.plot(times, magnetizations, label='magnetization')
#plt.plot(times[:100000], energies[:100000], label='energy')
#plt.xscale('log')
plt.legend()
plt.title('Titolo del {} grafico' .format(2))
plt.savefig(path+"\\Magnetizations.png")

plt.show()