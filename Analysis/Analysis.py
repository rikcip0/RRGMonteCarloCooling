import glob
import re
import os
import numpy as np
import matplotlib.pyplot as plt
import re

from MyBasePlots import Hist2dWithMarginals

# Define the path of the TXT files to ana lyze
Stories_path = "../Data/ThisRun/McStories/*.txt"
# Define the path of thetext file with infos on the input
InputInfo_path = "../Data/ThisRun/Info.txt"

# Define the path of destination for the plots
Plots_path = "../Data/ThisRun/Plots"

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
for i in range(0,3, 1):
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
'''
lastTimes = 200
totalOccurrences = lastTimes*nStories
magMin, magMax = np.min(magnetization[:,-lastTimes:]), np.max(magnetization[:,-lastTimes:])
eneMin, eneMax = np.min(energy[:,-lastTimes:]), np.max(energy[:,-lastTimes:])

hist, xedges, yedges = np.histogram2d(energy[:,-lastTimes:].flatten(), magnetization[:,-lastTimes:].flatten(), range=[[eneMin,eneMax],[magMin,magMax]])
'''
# Ottieni le dimensioni dell'istogramma
'''
num_bins_energy = hist.shape[0]
num_bins_magnetization = hist.shape[1]
non_empty_bins = np.count_nonzero(hist)

while True:
    if (non_empty_bins > totalOccurrences**0.5 or num_bins_energy>totalOccurrences/50) :
        break
    num_bins_energy*=2
    num_bins_magnetization*=2
    hist, xedges, yedges = np.histogram2d(energy[:,-lastTimes:].flatten(), magnetization[:,-lastTimes:].flatten(), range=[[eneMin,eneMax],[magMin,magMax]], bins=(num_bins_energy, num_bins_magnetization))
    non_empty_bins = np.count_nonzero(hist)


for i in range(0,3, 1):
        plt.figure('EnergyMagnetizationHistogramStory'+str(i))
        plt.title(f'Histogram of magnetizations and energies\n(last {lastTimes} MCtimes, for story #{i}')
        plt.xlabel('Energy')
        plt.ylabel('Magnetization')  
        hist, xedges, yedges = np.histogram2d(energy[i,-lastTimes:].flatten(), magnetization[i,-lastTimes:].flatten(),
                                                   bins=(num_bins_energy, num_bins_magnetization),
                                      range=[[eneMin,eneMax],[magMin,magMax]])
        normalized_hist = hist / np.sum(hist)
        plt.imshow(normalized_hist.T, extent=[magMin, magMax, eneMin, eneMax], origin='lower', aspect='auto', cmap='plasma')
        plt.colorbar()

'''

'''
plt.rcParams.update(plt.rcParamsDefault)
fig = plt.figure('EnergyMagnetizationHistogramAll', figsize=(10, 8))
plt.suptitle(f'Histogram of magnetization and energies\n(last {lastTimes} MCtimes, for {nStories} stories)', fontsize=14)
gs = fig.add_gridspec(11, 10)


ax_hist2d = fig.add_subplot(gs[1:9, 0:8])
hist, xedges, yedges, im = ax_hist2d.hist2d(energy[:,-lastTimes:].flatten(), magnetization[:,-lastTimes:].flatten(), bins=(num_bins_energy, num_bins_magnetization),
                                      range=[[eneMin,eneMax],[magMin,magMax]],cmap='plasma')
ax_hist2d.set_xlabel('Energy')
ax_hist2d.set_ylabel('Magnetization')
'''
# Marginali sull'asse Y
'''
ax_y = fig.add_subplot(gs[1:9, 8:9])
ax_y.hist(magnetization[:,-lastTimes:].flatten(), bins= 2*num_bins_magnetization, range=[magMin, magMax], orientation='horizontal', color='gray', alpha=0.7)
ax_y.yaxis.tick_right()
ax_y.set_ylim(magMin, magMax)
'''
# Marginali sull'asse X
'''
ax_x = fig.add_subplot(gs[0:1, 0:8])
ax_x.hist(energy[:,-lastTimes:].flatten(), bins=2*num_bins_energy, range=[eneMin, eneMax], color='gray', alpha=0.7)
ax_x.xaxis.tick_top()
ax_x.set_xlim(eneMin, eneMax)
'''
# Colorbar
'''
cax = fig.add_subplot(gs[10:11, 0:8])
cbar = plt.colorbar(im, cax=cax, orientation='horizontal')
cbar.set_label(f'Occurrences (total occurrences = {np.sum(hist)})')
cax.yaxis.set_ticks_position('right')
'''
# Regolazione degli spazi
'''
plt.subplots_adjust(wspace=0.8, hspace=0.6)
'''
Hist2dWithMarginals(energy, magnetization, 'energy', 'magnetization', 200, 10, nStories)

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
plt.title(f"Histogram of last MCtime magnetizations\nover all stories ({nStories})")
plt.xlabel("Magnetization")
plt.ylabel("Frequency")
plt.text(0.05, 0.9, f"Mean value: {meanMagnetization:.5f}", transform=plt.gca().transAxes)
plt.text(0.05, 0.85, f"$\sigma$: {sigmaMagnetization:.5f}", transform=plt.gca().transAxes)

plt.figure('HistogramFinalEnergies')
meanEnergy = np.mean(energy[:,-1])
sigmaEnergy = np.var(energy[:,-1])**0.5

plt.hist(energy[:,-1], density=True)
plt.title(f"Histogram of last MCtime energies\nover all stories ({nStories})")
plt.xlabel("Energy")
plt.ylabel("Frequency")
plt.text(0.05, 0.9, f"Mean value: {meanEnergy:.5f}", transform=plt.gca().transAxes)
plt.text(0.05, 0.85, f"$\sigma$: {sigmaEnergy:.5f}", transform=plt.gca().transAxes)


with open(results_path, "w") as file:
    # Scrivi i contenuti nel file
    file.write(f"The average final energy is {meanEnergy: .5f}, with variance {sigmaEnergy: .5f}.\n")
    file.write(f"The average final magnetization is {meanMagnetization: .5f}, with variance {sigmaMagnetization: .5f}.\n")

if not os.path.exists(Plots_path):
    os.makedirs(Plots_path)

figs = plt.get_figlabels()  # Ottieni i numeri di tutte le figure create
for fig_name in figs:
    fig = plt.figure(fig_name)
    filename = os.path.join(Plots_path, f'{fig_name}.png')
    fig.savefig(filename)


plt.show()