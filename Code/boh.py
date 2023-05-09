import glob
import re
import numpy as np
import matplotlib.pyplot as plt

# Define the path of the TXT files
file_path = "../Data/ThisRun/*.txt"

magnetization =[]
energy = []
time = []

# Get the file names in the folder
file_names = glob.glob(file_path)

# Check if there are no matching files
if not file_names:
    raise FileNotFoundError("No files found in the specified path.")


# Leggi i file e popola gli array delle colonne
for nome_file in sorted(file_names):
    # Utilizza espressione regolare per trovare il numero nel nome del file dopo la stringa "CIAO"
    matchStoryNumber = re.search(r"McStory_(\d+)", nome_file)
    if matchStoryNumber:
        storyNumber = int(matchStoryNumber.group(1))  # Converte il numero da stringa a intero
    else:
        raise ValueError("No file starting with 'McStory_' found.")

    with open(nome_file, 'r') as file:
        # Leggi tutte le righe dal file
        lines = file.readlines()
        dataLines = filter(lambda x: not x.startswith('#'), lines)
        data = np.genfromtxt(dataLines, delimiter=' ')
        magnetization.append(data[:,0])
        energy.append(data[:,1])
        time.append(data[:,2])



# Access the data using the predefined arrays
time = np.array(time)
magnetization= np.array(magnetization)
energy = np.array(energy)

plt.figure(0)
plt.plot(time[1,20:], energy[:,20:].mean(0))
plt.figure(1)
plt.plot(time[1,20:], magnetization[:,20:].mean(0))

for i in range(0,4, 1):
    plt.figure('mag')
    plt.plot(time[i,20:], magnetization[i,20:])
    plt.figure('ene')
    plt.plot(time[i,20:], energy[i,20:])

magMin, magMax = np.min(magnetization[:,400:]), np.max(magnetization[:,400:])
eneMin, eneMax = np.min(energy[:,400:]), np.max(energy[:,400:])

#for i in range(0,9, 1):
    #plt.figure('histo {}'.format(i))
    #plt.hist2d(magnetization[i,400:].flatten(),energy[i,400:].flatten(), range=[[magMin,magMax],[eneMin,eneMax]])

plt.figure('magAv')
plt.scatter(time[1,100:220], magnetization[:,100:220].mean(0))
plt.figure('eneAv')
plt.scatter(time[1,100:220], energy[:,100:220].mean(0))

print(energy[:,100:220].mean(0))
plt.figure('Histogram')
plt.hist2d(magnetization[:,400:].flatten(),energy[:,400:].flatten())

plt.show()
