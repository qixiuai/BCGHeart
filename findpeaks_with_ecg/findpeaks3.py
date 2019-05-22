
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import ecgpeaks
import autopeaks


class Peak(object):

    def __init__(self, index, value):
        self.index = index
        self.value = value


class PeakPair(object):

    def __init__(self, left_peak, ecg_peak, right_peak):
        self.left_peak = left_peak
        self.ecg_peak = ecg_peak
        self.right_peak = right_peak


def generate_peakpairs(bcg_indices, bcg_values, ecg_indices, ecg_values):
    num_bcg_indices = len(bcg_indices)
    num_ecg_indices = len(ecg_indices)
    peakpair_pool = []
    
    for 
    
    bcg_id = 0
    ecg_id = 0    
    while (ecg_id < num_ecg_indices and bcg_id + 1 < num_bcg_indices):
        bcg_index = bcg_indices[bcg_id]
        next_bcg_index = bcg_indices[bcg_id+1]
        ecg_index = ecg_indices[ecg_id]
        #next_ecg_index = ecg_indices[ecg_id+1]
        if abs(bcg_index - ecg_index) <  abs(next_bcg_index - ecg_index):
            peak_indices.append(bcg_index)
            peak_value = bcg_peak_values[bcg_id]
            peak_values.append(peak_value)
            ecg_id += 1
        bcg_id += 1
    return peak_indices, peak_values


def findpeaks_in_bcg_with_ecg(bcg, ecg, ecg_fs=500):
    """
        assume bcg ecg data without time delay
    """
    # get ecg peak indices and peak values
    ecg_peak_indices, ecg_peak_values = ecgpeaks.findpeaks_in_ecg(ecg, fs=ecg_fs)

    # get candidate bcg peaks
    # TODO finetune peaks
    auto_peaks = autopeaks.AutoPeaks(thres=0.50, min_dist=10, buffer_size=30)
    list(map(auto_peaks.findpeaks, bcg))
    bcg_candidate_indices, bcg_candidate_values = \
      auto_peaks.peak_indexes, auto_peaks.peak_values

    # filter candidate peaks
    bcg_peak_indices, bcg_peak_values = filter_bcg_candidate_peaks(
        bcg_candidate_indices, bcg_candidate_values, ecg_peak_indices)
    
    return bcg_peak_indices, bcg_peak_values, ecg_peak_indices, ecg_peak_values
