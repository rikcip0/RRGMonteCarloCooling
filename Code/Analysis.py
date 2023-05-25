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
nStories = time.__len__

plt.figure(0)
plt.plot(time[1,20:], energy[:,20:].mean(0))
plt.figure(1)
plt.plot(time[1,20:], magnetization[:,20:].mean(0))


#FIRST TYPE OF PLOTS: ENERGY AND MAGNETIZATION BEHAVIOURS FOR SOME STORIES/SAMPLES, AND FOR AVERAGE OVER ALL STORIES
for i in range(0,4, 1):
    plt.figure('mag'+str(i))
    plt.plot(time[i,20:], magnetization[i,20:])
    plt.figure('ene'+str(i))
    plt.plot(time[i,20:], energy[i,20:])





#SECOND TYPE OF PLOTS: 2D HISTOGRAMS (within the same frame) of single stories (ener,mag) and of all stories (en,mag)
magMin, magMax = np.min(magnetization[:,400:]), np.max(magnetization[:,400:])
eneMin, eneMax = np.min(energy[:,400:]), np.max(energy[:,400:])

for i in range(0,10, 1):
    plt.figure('histo {}'.format(i))
    plt.hist2d(magnetization[i,400:].flatten(),energy[i,400:].flatten(), range=[[magMin,magMax],[eneMin,eneMax]])

plt.figure('histoGen {}'.format(i))
plt.hist2d(magnetization[:,400:].flatten(),energy[:,400:].flatten(), range=[[magMin,magMax],[eneMin,eneMax]])


plt.figure('magAv')
plt.scatter(time[1,10:], magnetization[:,10:].mean(0))
plt.figure('eneAv')
plt.scatter(time[1,10:], energy[:,10:].mean(0))

plt.figure('magAvAv')
mean = np.mean(magnetization[:,-1])
variance = np.var(magnetization[:,-1])

# Plotta l'istogramma
plt.hist(magnetization[:,-1])
plt.title("Istogramma")
plt.xlabel("Valore")
plt.ylabel("Frequenza")

# Aggiungi valore medio e varianza al grafico
plt.text(0.05, 0.9, f"Valore medio: {mean:.2f}", transform=plt.gca().transAxes)
plt.text(0.05, 0.85, f"Varianza: {variance:.2f}", transform=plt.gca().transAxes)

plt.figure('eneAvAv')
mean = np.mean(energy[:,-1])
variance = np.var(energy[:,-1])

# Plotta l'istogramma
plt.hist(energy[:,-1])

# Aggiungi valore medio e varianza al grafico
plt.text(0.05, 0.9, f"Valore medio: {mean:.2f}", transform=plt.gca().transAxes)
plt.text(0.05, 0.85, f"Varianza: {variance:.2f}", transform=plt.gca().transAxes)

plt.show()
