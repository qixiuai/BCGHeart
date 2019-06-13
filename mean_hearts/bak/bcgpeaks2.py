
import numpy as np
import peakutils

from collections import namedtuple

class AutoPeaks(object):

    def __init__(self):
        pass


class PeakCluster(namedtuple("PeakCluster",
                             ["upper_peak_index", "upper_peak_value",
                              "lower_peak_index", "lower_peak_value",
                              "zero_peak_index", "zero_peak_value"])):
    def __init__(self, upper_peak_index, lower_peak_index):
        self.upper_peak_index = upper_peak_index
        self.lower_peak_index = lower_peak_index



def findpeaks(signal, thres=0.73, pair_dist=30, min_dist=300):
    """
    assume distance between J peak and K valley is fixed around 60ms
    offline version
    """
    if isinstance(signal, list):
        signal = np.asarray(signal)
    diff = np.diff(signal)
    diff_abs = np.abs(diff)
    zero_peak_indices = peakutils.indexes(-diff_abs, thres=0.9, min_dist=pair_dist)
    upper_peak_indices = peakutils.indexes(diff, thres=thres, min_dist=min_dist)
    lower_peak_indices = peakutils.indexes(-diff, thres=thres, min_dist=min_dist)
    peak_pairs = []
    num_upper_peaks = len(upper_peak_indices)
    num_lower_peaks = len(lower_peak_indices)
    ind_upper = 0
    ind_lower = 0
    while ind_upper < num_upper_peaks and ind_lower < num_lower_peaks:
        upper_peak_index = upper_peak_indices[ind_upper]
        lower_peak_index = lower_peak_indices[ind_lower]
        if upper_peak_index - lower_peak_index > pair_dist:
            lower_peak_index += 1
            continue
        if lower_peak_index - upper_peak_index > pair_dist:
            upper_peak_index += 1
            continue
        upper_peak_value = diff_abs[upper_peak_index]
        lower_peak_value = diff_abs[lower_peak_index]
        
        
        
    if ind_upper < num_upper_peaks:
        pass

    if ind_lower < num_lower_peaks:
        pass

    num_peaks = len(peak_indices)
    for ind in range(num_peaks-1):
        curr_peak_index = peak_indices[ind]
        next_peak_index = peak_indices[ind+1]
        curr_peak_value = diff[curr_peak_index]
        next_peak_value = diff[next_peak_index]
        if curr_peak_value * next_peak_value < 0:
            pair_peak_value = np.abs(curr_peak_value) + np.abs(next_peak_value)
            zero_peak_index = curr_peak_index + \
                              np.argmin(diff_abs[curr_peak_index:next_peak_index])
            peak_pairs.append((zero_peak_index, curr_peak_index, next_peak_index, pair_peak_value))



            
