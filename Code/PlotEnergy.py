import matplotlib.pyplot as plt
import numpy as np
import sys
#import os when using absolute paths
import scipy as sp
from scipy import stats
 
N = int(sys.argv[1])
T_p = str(sys.argv[2])
T = float(sys.argv[3])
n_samples = int(sys.argv[4])
h = float(sys.argv[5])
t_max = int(sys.argv[6])

averages = []

#path = os.path.abspath('..\Data\LastRun')     to be implemented, when using absolute paths
path = '..\Data\LastRun'

print(path+'\\McStories.txt')
with open(path+'\\McStories.txt', 'r') as f:
    lines = f.readlines()  # Legge tutte le righe in una lista
    dataLines = filter(lambda x: not x.startswith('#'), lines)
    paramsLines =  filter(lambda x: x.startswith('#'), lines)

data = np.genfromtxt(dataLines, delimiter=' ')
plt.figure(0)

for i in range (n_samples):
    times = data[i*t_max:(i+1)*t_max,2]
    energies = data[i*t_max:(i+1)*t_max, 1]
    magnetizations = data[i*t_max:(i+1)*t_max, 0]
    moments = stats.describe(energies[2000:10000])
    print("s {} per 1" .format(moments.mean))
    print("s {} per 2" .format(moments.variance))
    print("s {} per 3" .format(moments.skewness))
    print("s {} per 4" .format(moments.kurtosis))
    plt.hist(energies[2000:1000], label='en')
    plt.title('Data')
    plt.show()
    averages.append(np.average(energies[2000:t_max]))
plt.figure(1)
plt.plot(times, energies, label='magnetization')
plt.legend("c")
plt.title('Titolo del {} grafico'.format(4))
plt.savefig(path+"\\EnergyStories.png")

plt.figure(1)




plt.figure(2)
plt.hist(averages)
plt.legend("c")
plt.title('Averages')
plt.savefig(path+"\\EnergyHystogram.png")

plt.show()

with open(path+'\\Results.txt', 'w') as f:
    for line in paramsLines:
        f.write(line)
    f.write('The average final energy is {}.'.format(np.average(averages)))