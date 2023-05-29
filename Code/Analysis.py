import glob
import re
import os
import numpy as np
import matplotlib.pyplot as plt
import re
import fileinput

# Define the path of the TXT files to ana lyze
Stories_path = "../Data/ThisRun/McStories/*.txt"
# Define the path of thetext file with infos on the input
InputInfo_path = "../Data/ThisRun/Info.txt"

# Define the path of destination for the plots
Plots_path = "../Data/ThisRun/Plots"
if not os.path.exists(Plots_path):
    os.makedirs(Plots_path)
plt.rcParams["figure.autolayout"] = True


# Define the path of the destination for the results
results_path = "../Data/ThisRun/Results.txt"

# Get the stories names in the folder
file_names = glob.glob(Stories_path)

# Check if there are no matching files
if not file_names:
    raise FileNotFoundError("No files found in the specified path.")



#EXTRACTING INPUT PARAMETERS
# Open the text file with infos on the input in read mode
with open(InputInfo_path, "r") as file:
    # Read the content of the file
    content = file.read()

    # Find the line starting with "#"
    params_line = next((line for line in content.split("\n") if line.startswith("#")), None)

    if params_line is not None:
        # Extract the symType
        symType = re.search(r"#(\w+)", params_line).group(1)

        # Search for parameters and values using regular expressions
        results = re.findall(r"\b(\w+)\s*=\s*([^\s#]+)", params_line)

        # Create a dictionary to store the parameters and their values
        parameters = {}
        for result in results:
            parameter = result[0]
            value = result[1]
            if "." in value:
                # If the value contains a decimal point, convert to float
                value = float(value)
            else:
                try:
                    # Try converting the value to float
                    value = int(value)
                except ValueError:
                    # If the conversion fails, keep the value as string
                    pass
            parameters[parameter] = value
    
        # Print the keyword, parameters, and their values
        print("Analyzing simulation of type:", symType, "\nwith parameters")
        for parameter, value in parameters.items():
            print(parameter, "=", value, end=" ")
        print("\n")
    else:
        print("No line specifying parameters (starting with '#') found in the file.")
        # Find the line with "paramSpecial"
    
    projectedStories_line = next((line for line in content.split("\n") if line.startswith("projectedStories")), None)

    if projectedStories_line is not None:
        # Extract the value of "paramSpecial"
        projectedStories = re.search(r"=\s*([^\s#]+)", projectedStories_line).group(1)

        # Print the value of "paramSpecial"
        print("projectedStories =", projectedStories)

    actual_stories_line_exists = next((line for line in content.split("\n") if line.startswith("actualStories")), None)


magnetization =[]
energy = []
time = []

# Leggi i file e popola gli array delle colonne
for nome_file in sorted(file_names):
    # Utilizza espressione regolare per trovare il numero nel nome del file dopo la stringa "CIAO"
    matchStoryNumber = re.search(r"Story_(\d+)", nome_file)
    if matchStoryNumber:
        storyNumber = int(matchStoryNumber.group(1))  # Converte il numero da stringa a intero
    else:
        raise ValueError("No file starting with 'Story_' found.")

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

nStories = time.shape[0]
print("nStories =", nStories)

if not actual_stories_line_exists:
    with open(InputInfo_path, "a") as file:
        file.write(f"actualStories = {nStories}\n")

magnetization/=parameters["N"]
energy/=parameters["N"]




#FIRST TYPE OF PLOTS: ENERGY AND MAGNETIZATION BEHAVIOURS FOR SOME STORIES/SAMPLES, AND FOR AVERAGE OVER ALL STORIES
for i in range(0,4, 1):
    plt.figure('MagnetizationStory'+str(i))
    plt.title('Magnetization evolution for story #'+str(i))
    plt.xlabel('MC time')  
    plt.ylabel('Magnetization') 
    plt.grid(True)
    plt.plot(time[i,20:], magnetization[i,20:])

    plt.figure('EnergyStory'+str(i))
    plt.title('Energy evolution for story #'+str(i))
    plt.xlabel('MC time')  
    plt.ylabel('Energy')
    plt.grid(True) 
    plt.plot(time[i,20:], energy[i,20:])





#SECOND TYPE OF PLOTS: 2D HISTOGRAMS (within the same frame) of single stories (ener,mag) and of all stories (en,mag)
magMin, magMax = np.min(magnetization[:,40:]), np.max(magnetization[:,40:])
eneMin, eneMax = np.min(energy[:,40:]), np.max(energy[:,40:])

for i in range(0,5, 1):
    # Calcola il numero di bin predefinito
    while True:
        hist, xedges, yedges = np.histogram2d(magnetization[i,40:],energy[i,40:], range=[[magMin,magMax],[eneMin,eneMax]])

        # Ottieni le dimensioni dell'istogramma
        num_bins_x = hist.shape[0]
        num_bins_y = hist.shape[1]
        non_empty_bins = np.count_nonzero(hist)

        num_bins_x*=2
        num_bins_y*=2
        if (non_empty_bins > 5 or  num_bins_x>20 or True) :
            plt.figure('EnergyMagnetizationHistogramStory'+str(i))
            plt.title('Histogram of magnetization and energies\n for last times of story #{}'.format(i))
            plt.xlabel('Magnetization')  
            plt.ylabel('Energy')
            hist, xedges, yedges = np.histogram2d(magnetization[i,40:], energy[i,40:].flatten(),
                                                   bins=(num_bins_x, num_bins_y),
                                      range=[[magMin, magMax], [eneMin, eneMax]])
            normalized_hist = hist / np.sum(hist)
            plt.imshow(normalized_hist.T, extent=[magMin, magMax, eneMin, eneMax], origin='lower', aspect='auto', cmap='plasma')
            plt.colorbar()
            break

plt.figure('EnergyMagnetizationHistogramAll')
plt.title('Histogram of magnetization and energies\n for last times for all stories')
plt.xlabel('Magnetization')  
plt.ylabel('Energy')
hist, xedges, yedges = np.histogram2d(magnetization[:,40:].flatten(), energy[:,40:].flatten(), bins=(num_bins_x, num_bins_y),
                                      range=[[magMin, magMax], [eneMin, eneMax]])
normalized_hist = hist / np.sum(hist)
plt.imshow(normalized_hist.T, extent=[magMin, magMax, eneMin, eneMax], origin='lower', aspect='auto', cmap='plasma')
#plt.hist2d(magnetization[:,40:].flatten(), energy[:,40:].flatten(), bins=(num_bins_x, num_bins_y), range=[[magMin,magMax],[eneMin,eneMax]], density=True)
plt.colorbar()


#PLOTS OF AVERAGE (ON STORIES) OF ENERGIES AND MAGNETIZATIONS

plt.figure('AverageMagnetization')
plt.title('Magnetization averaged on all stories')
plt.xlabel('MC time')  
plt.ylabel('Average magnetization')
plt.grid(True)
plt.scatter(time[1,10:], magnetization[:,10:].mean(0))


plt.figure('AverageEnergy')
plt.title('Energy averaged on all stories')
plt.xlabel('MC time')  
plt.ylabel('Average energy')
plt.grid(True)
plt.scatter(time[1,10:], energy[:,10:].mean(0))



#HISTOGRAMS OF FINAL ENERGY AND MAGNETIZATIONS OVER THE STORIES

plt.figure('HistogramFinalMagnetizations')
meanMagnetization = np.mean(magnetization[:,-1])
sigmaMagnetization = np.var(magnetization[:,-1])**0.5

plt.hist(magnetization[:,-1], density=True)
plt.title("Histogram of")
plt.xlabel("Magnetization")
plt.ylabel("Frequency")
plt.text(0.05, 0.9, f"Mean value: {meanMagnetization:.5f}", transform=plt.gca().transAxes)
plt.text(0.05, 0.85, f"\Sigma: {sigmaMagnetization:.5f}", transform=plt.gca().transAxes)

plt.figure('HistogramFinalEnergies')
meanEnergy = np.mean(energy[:,-1])
sigmaEnergy = np.var(energy[:,-1])**0.5

plt.hist(energy[:,-1], density=True)
plt.title("Histogram of")
plt.xlabel("Energy")
plt.ylabel("Frequency")
plt.text(0.05, 0.9, f"Mean value: {meanEnergy:.5f}", transform=plt.gca().transAxes)
plt.text(0.05, 0.85, f"\Sigma: {sigmaEnergy:.5f}", transform=plt.gca().transAxes)



figs = plt.get_figlabels()  # Ottieni i numeri di tutte le figure create
for fig_name in figs:
    fig = plt.figure(fig_name)
    filename = os.path.join(Plots_path, f'{fig_name}.png')
    fig.savefig(filename)




#plt.show()

with open(results_path, "w") as file:
    # Scrivi i contenuti nel file
    file.write("Questo è un esempio di file di risultati.\n")
    file.write("Aggiungi qui i tuoi risultati o altre informazioni.\n")