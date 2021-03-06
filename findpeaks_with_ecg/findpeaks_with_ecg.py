
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import fs
import numpy as np
import autopeaks

from absl import app
from ecgpeaks import findpeaks_in_ecg
from collections import deque

def filter_bcg_candidate_peaks(bcg_indices, bcg_peak_values, ecg_indices):
    """
    get corrent bcg peaks by choose closest peaks at ecg_indices
    """
    peak_indices = []
    peak_values = []
    num_bcg_indices = len(bcg_indices)
    num_ecg_indices = len(ecg_indices)
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


def filter2_bcg_candidate_peaks(candidate_indices, candidate_values,
                                bcg_indices, bcg_values, ecg_indices):
    """
    get corrent bcg peaks by choose closest peaks at ecg_indices
    """
    num_bcg_indices = len(bcg_indices)
    num_ecg_indices = len(ecg_indices)
    bcg_id = 0
    ecg_id = 0
    while (ecg_id < num_ecg_indices and bcg_id + 1 < num_bcg_indices):
        bcg_index = bcg_indices[bcg_id]
        next_bcg_index = bcg_indices[bcg_id+1]
        #next_ecg_index = ecg_indices[ecg_id+1]
        # fix edge error
        start = ecg_id-30 if ecg_id - 30 >= 0 else 0
        end = ecg_id+30 if ecg_id + 30 < num_bcg_indices else num_bcg_indices
        bcg_indices_pool = peak_indices[start : end]
        ecg_indices_pool = ecg_indices[start : end]
        pred_bcg_index = bcg_index + \
            np.median(np.asarray(ecg_indices_pool)-np.asarray(bcg_indices_pool))
        if abs(bcg_index - pred_bcg_index) <  abs(next_bcg_index - pred_bcg_index):
            peak_indices.append(bcg_index)
            peak_value = bcg_peak_values[bcg_id]
            peak_values.append(peak_value)
            ecg_id += 1
        bcg_id += 1
    return peak_indices, peak_values


def filter_outerlier_peaks(peak_indices):
    intervals = np.diff(peak_indices)
    outerlies = []
    num_rr = len(intervals)
    buf_rr = deque(maxlen=10)
    for ind_rr in range(num_rr):
        rr = intervals[ind_rr]
        buf_rr.append(rr)
        mean_rr = np.median(buf_rr)
        if (abs(rr - mean_rr) > 20):
            pass


def repair_bcg_peaks_with_ecg_peaks(bcg_indices, ecg_indices):
    pass


def findpeaks_in_bcg_with_ecg(bcg, ecg, bcg_fs=500, ecg_fs=500):
    """
        assume bcg ecg data without time delay
    """
    # get ecg peak indices and peak values
    ecg_peak_indices, ecg_peak_values = findpeaks_in_ecg(ecg, fs=ecg_fs)

    # get candidate bcg peaks
    # TODO finetune peaks
    auto_peaks = autopeaks.AutoPeaks(thres=0.50, min_dist=10, buffer_size=30)
    list(map(auto_peaks.findpeaks, bcg))
    bcg_candidate_indices, bcg_candidate_values = \
      auto_peaks.peak_indexes, auto_peaks.peak_values

    # filter candidate peaks
    bcg_peak_indices, bcg_peak_values = filter_bcg_candidate_peaks(
        bcg_candidate_indices, bcg_candidate_values, ecg_peak_indices)
 
    bcg_peak_indices, bcg_peak_values = filter2_bcg_candidate_peaks(
        bcg_candidate_indices, bcg_candidate_values,
        bcg_peak_indices, bcg_peak_values, ecg_peak_indices)
    
    return bcg_peak_indices, bcg_peak_values, ecg_peak_indices, ecg_peak_values


def findpeaks_wsx():
    data_dir = "/home/guo/physio/BCG_data/bcg_ecg_data/bcg_ecg_data(500HZ)/"
    bcg_path = data_dir + "wsx_bcg_wave(500HZ).txt"
    ecg_path = data_dir + "wsx_ecg.edf"
    bcg = fs.load_bcg(bcg_path, offset=12726-68-6-43)
    ecg = fs.load_ecg(ecg_path)
    peak_indexes, peak_values, ecg_peak_indices, ecg_peak_values = \
      findpeaks_in_bcg_with_ecg(bcg, ecg)
    return peak_indexes, peak_values, ecg_peak_indices, ecg_peak_values


def main(unused_args):
    del unused_args

    
if __name__ == "__main__":    
    app.run(main)


