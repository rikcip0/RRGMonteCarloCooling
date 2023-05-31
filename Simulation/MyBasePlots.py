import numpy as np
import matplotlib.pyplot as plt

def Hist2dWithMarginals(x_array, y_array, xName, yName, lastTimes, t_meas, nStories):
    totalOccurrences = lastTimes*nStories
    yMin, yMax = np.min(y_array[:,-lastTimes:]), np.max(y_array[:,-lastTimes:])
    xMin, xMax = np.min(x_array[:,-lastTimes:]), np.max(x_array[:,-lastTimes:])

    hist, xedges, yedges = np.histogram2d(x_array[:,-lastTimes:].flatten(), y_array[:,-lastTimes:].flatten(), range=[[xMin,xMax],[yMin,yMax]])

    # Ottieni le dimensioni dell'istogramma
    num_bins_x_array = hist.shape[0]
    num_bins_y_array = hist.shape[1]
    non_empty_bins = np.count_nonzero(hist)

    while True:
        if (non_empty_bins > totalOccurrences**0.5 or num_bins_x_array>totalOccurrences/50) :
            break
        num_bins_x_array*=2
        num_bins_y_array*=2
        hist, xedges, yedges = np.histogram2d(x_array[:,-lastTimes:].flatten(), y_array[:,-lastTimes:].flatten(), range=[[xMin,xMax],[yMin,yMax]], bins=(num_bins_x_array, num_bins_y_array))
        non_empty_bins = np.count_nonzero(hist)


    for i in range(0,3, 1):
        # Calcola il numero di bin predefinito

            plt.figure(f'{xName}{yName}HistogramStory'+str(i))
            plt.title(f'Histogram of {yName}s and {xName}\n(last {lastTimes} MCtimes, for story #{i}')
            plt.xlabel(f'{xName}')  
            plt.ylabel(f'{yName}')
            hist, xedges, yedges = np.histogram2d(x_array[i,-lastTimes:].flatten(), y_array[i,-lastTimes:].flatten(),
                                                    bins=(num_bins_x_array, num_bins_y_array),
                                        range=[[xMin,xMax],[yMin,yMax]])
            normalized_hist = hist / np.sum(hist)
            plt.imshow(normalized_hist.T, extent=[yMin, yMax, xMin, xMax], origin='lower', aspect='auto', cmap='plasma')
            plt.colorbar()




    # Creazione dei sottografici
    plt.rcParams.update(plt.rcParamsDefault)
    fig = plt.figure(f'{xName}{yName}HistogramAll', figsize=(10, 8))
    plt.suptitle(f'Histogram of {xName} and {yName}\n(last {lastTimes} MCtimes, for {nStories} stories)', fontsize=14)
    gs = fig.add_gridspec(11, 10)

    # Istogramma 2D
    ax_hist2d = fig.add_subplot(gs[1:9, 0:8])
    hist, xedges, yedges, im = ax_hist2d.hist2d(x_array[:,-lastTimes:].flatten(), y_array[:,-lastTimes:].flatten(), bins=(num_bins_x_array, num_bins_y_array),
                                        range=[[xMin,xMax],[yMin,yMax]],cmap='plasma')
    ax_hist2d.set_xlabel(f'{xName}')
    ax_hist2d.set_ylabel(f'{yName}')

    # Marginali sull'asse Y
    ax_y = fig.add_subplot(gs[1:9, 8:9])
    ax_y.hist(y_array[:,-lastTimes:].flatten(), bins= 2*num_bins_y_array, range=[yMin, yMax], orientation='horizontal', color='gray', alpha=0.7)
    ax_y.yaxis.tick_right()
    ax_y.set_ylim(yMin, yMax)

    # Marginali sull'asse X
    ax_x = fig.add_subplot(gs[0:1, 0:8])
    ax_x.hist(x_array[:,-lastTimes:].flatten(), bins=2*num_bins_x_array, range=[xMin, xMax], color='gray', alpha=0.7)
    ax_x.xaxis.tick_top()
    ax_x.set_xlim(xMin, xMax)

    # Colorbar
    cax = fig.add_subplot(gs[10:11, 0:8])
    cbar = plt.colorbar(im, cax=cax, orientation='horizontal')
    cbar.set_label(f'Occurrences (total occurrences = {np.sum(hist)})')
    cax.yaxis.set_ticks_position('right')

    # Regolazione degli spazi
    plt.subplots_adjust(wspace=0.8, hspace=0.6)
