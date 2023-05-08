import glob
import re
import numpy as np
import matplotlib.pyplot as plt

# Define the path of the TXT files
file_path = "../Data/ThisRun/*.txt"

# Number of columns in the files (assuming all files have the same number of columns)
num_columns = 3

# List of custom column names
column_names = ["magnetization", "energy", "time"]

# Dictionary of arrays for the columns
columns = {column_name: [] for column_name in column_names}

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
        raise ValueError("Impossibile trovare un numero preceduto da 'McStory_' nel nome del file.")

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

plt.plot(time[1,1:], energy[:,1:].mean(axis=0))
plt.figure(2)
plt.plot(time[1,1:], energy[:,1:].var(axis=0))
plt.legend()
plt.show()
