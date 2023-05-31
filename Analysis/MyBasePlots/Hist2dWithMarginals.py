import numpy as np
import matplotlib.pyplot as plt

def Hist2dWithMarginals(x_array, y_array, xName, yName, startMeasure, endMeasure, timeArray):
    nStories = x_array.shape[0]
    totalOccurrences = (np.abs(startMeasure-endMeasure)+1)*nStories
    yMin, yMax = np.min(y_array[:,startMeasure:endMeasure]), np.max(y_array[:,startMeasure:endMeasure])
    xMin, xMax = np.min(x_array[:,startMeasure:endMeasure]), np.max(x_array[:,startMeasure:endMeasure])

    hist, xedges, yedges = np.histogram2d(x_array[:,startMeasure:endMeasure].flatten(), y_array[:,startMeasure:endMeasure].flatten(), range=[[xMin,xMax],[yMin,yMax]])

    # Ottieni le dimensioni dell'istogramma
    num_bins_x_array = hist.shape[0]
    num_bins_y_array = hist.shape[1]
    non_empty_bins = np.count_nonzero(hist)

    while True:
        if (non_empty_bins > totalOccurrences**0.5 or num_bins_x_array>totalOccurrences/50) :
            break
        num_bins_x_array*=2
        num_bins_y_array*=2
        hist, xedges, yedges = np.histogram2d(x_array[:,startMeasure:endMeasure].flatten(), y_array[:,startMeasure:endMeasure].flatten(), range=[[xMin,xMax],[yMin,yMax]], bins=(num_bins_x_array, num_bins_y_array))
        non_empty_bins = np.count_nonzero(hist)


    for i in range(0,3, 1):
        # Calcola il numero di bin predefinito

            plt.figure(f'{xName}{yName}HistogramStory'+str(i))
            plt.title(f'Histogram of {yName}s and {xName}\n(last {startMeasure} MCtimes, for story #{i}')
            plt.xlabel(f'{xName}')  
            plt.ylabel(f'{yName}')
            hist, xedges, yedges = np.histogram2d(x_array[i,startMeasure:endMeasure].flatten(), y_array[i,startMeasure:endMeasure].flatten(),
                                                    bins=(num_bins_x_array, num_bins_y_array),
                                        range=[[xMin,xMax],[yMin,yMax]])
            normalized_hist = hist / np.sum(hist)
            plt.imshow(normalized_hist.T, extent=[yMin, yMax, xMin, xMax], origin='lower', aspect='auto', cmap='plasma')
            plt.colorbar()




    # Creazione dei sottografici
    plt.rcParams.update(plt.rcParamsDefault)
    fig = plt.figure(f'{xName}{yName}HistogramAll', figsize=(10, 10))
    gs = fig.add_gridspec(21, 18)

    # Istogramma 2D
    ax_hist2d = fig.add_subplot(gs[3:18, 0:15])
    hist, xedges, yedges, im = ax_hist2d.hist2d(x_array[:,startMeasure:endMeasure].flatten(), y_array[:,startMeasure:endMeasure].flatten(), bins=(num_bins_x_array, num_bins_y_array),
                                        range=[[xMin,xMax],[yMin,yMax]],cmap='plasma')
    
    ax_x = fig.add_subplot(gs[1:3, 0:15])
    ax_y = fig.add_subplot(gs[3:18, 15:17])
    
    
    mean_y = np.mean(y_array[:,startMeasure:endMeasure].flatten())
    sigma_y = np.var(y_array[:,startMeasure:endMeasure].flatten())**0.5
    mean_x = np.mean(x_array[:,startMeasure:endMeasure].flatten())
    sigma_x = np.var(x_array[:,startMeasure:endMeasure].flatten())**0.5
    ax_hist2d.set_xlabel(f'{xName}')
    ax_hist2d.set_ylabel(f'{yName}')

    # Marginali sull'asse X
    ax_x.hist(x_array[:,startMeasure:endMeasure].flatten(), bins=2*num_bins_x_array, range=[xMin, xMax], color='gray', alpha=0.7)
    ax_x.xaxis.tick_top()
    ax_x.set_xlim(xMin, xMax)
    ax_x.axvline(mean_x, color='black', linestyle='solid', linewidth=2)
    ax_x.text(1., 1.9, f'Mean {xName}: {mean_x: .3f}  $\sigma$: {sigma_x: .3f}', color='black', ha='right', va='center',transform=ax_x.transAxes)
    ax_x.axvline(mean_x+sigma_x, color='red', linestyle='dashed', linewidth=1)
    ax_x.axvline(mean_x-sigma_x, color='red', linestyle='dashed', linewidth=1)

    # Marginali sull'asse Y
    ax_y.hist(y_array[:,startMeasure:endMeasure].flatten(), bins= 2*num_bins_y_array, range=[yMin, yMax], orientation='horizontal', color='gray', alpha=0.7)
    ax_y.yaxis.tick_right()
    ax_y.set_ylim(yMin, yMax)
    ax_y.axhline(mean_y, color='black', linestyle='solid', linewidth=2)
    ax_y.text(2., 1., f'Mean {yName}: {mean_y: .3f}  $\sigma$: {sigma_y: .3f}', color='black', ha='left', rotation=270, va='top',transform=ax_y.transAxes)
    ax_y.axhline(mean_y+sigma_y, color='red', linestyle='dashed', linewidth=1)
    ax_y.axhline(mean_y-sigma_y, color='red', linestyle='dashed', linewidth=1)

    # Colorbar
    cax = fig.add_subplot(gs[19:21, 0:15])
    cbar = plt.colorbar(im, cax=cax, orientation='horizontal')
    cbar.set_label(f'Occurrences (total occurrences = {np.sum(hist)})')
    cax.yaxis.set_ticks_position('right')

    # Regolazione degli spazi
    plt.subplots_adjust(hspace=0.7, wspace=0.7)


    title = f'Histogram of {xName} and {yName}\n'
    if endMeasure==-1:
         title += f'(last {startMeasure} measures'
    else:
         title += f'(measures from {startMeasure} to {endMeasure}'
    title+=f', times from {timeArray[startMeasure]} to {timeArray[endMeasure]}, over {nStories} stories)'

    plt.suptitle(title, fontsize=10)

