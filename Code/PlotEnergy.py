import matplotlib.pyplot as plt
import numpy as np
import sys

t_max=9999
n_stories=10
averages = []

path = path = "C:\\Users\\Riccardo\\Desktop\\Codici\\PhD\\diluted_pSpin\\Quenching\\Data\\LastRun"
with open(path+ '\\McStories.txt', 'r') as file:
    lines = file.readlines()

data = np.genfromtxt(lines, delimiter=' ')
plt.figure(0)

for i in range (n_stories):
    times = data[i*t_max:(i+1)*t_max,2]
    energies = data[i*t_max:(i+1)*t_max, 1]
    magnetizations = data[i*t_max:(i+1)*t_max, 0]
    plt.plot(times, energies, label='sample')
    averages.append(np.average(energies[2000:t_max]))
plt.legend("c")
plt.title('Titolo del {} grafico'.format(4))
plt.savefig(path+"\\EnergyStories.png")

plt.figure(2)
plt.hist(averages)
plt.legend("c")
plt.title('Titolo del22 {} grafico'.format(4))
plt.savefig(path+"\\EnergyHystogram.png")

plt.show()

with open(path+'\\Results.txt', 'w') as f:
    f.write('The average final energy is {}.'.format(np.average(averages)))