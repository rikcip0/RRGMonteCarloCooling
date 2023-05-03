import matplotlib.pyplot as plt
import numpy as np
import sys

n_stories=10
n = int(sys.argv[1])
print(n+1)
path = "C:\\Users\\Riccardo\\Desktop\\Codici\\PhD\\diluted_pSpin\\Quenching\\Data\\LastRun"

with open(path + '\\McStories.txt', 'r') as file:
    lines = file.readlines()


data = np.genfromtxt(lines, delimiter=' ')
times = data[:, 2]
energies = data[:, 1]
magnetizations = data[:, 0]

plt.plot(times, magnetizations, label='magnetization')
#plt.plot(times[:100000], energies[:100000], label='energy')
#plt.xscale('log')
plt.legend()
plt.title('Titolo del {} grafico' .format(n))
plt.savefig(path+"\\Ciao.png")

plt.show()