
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from scipy.signal import lfilter

import autopeaks
import numpy as np
import pdb


def findpeaks_in_ecg(signal,
                     fs=500,
                     use_bandpass=False,
                     use_notch=False):
    if use_bandpass:
        signal = bandpass_filter(signal, fs)
    if use_notch:
        signal = notch_filter(signal, fs)
    min_dist = int(fs * 0.6)
    buffer_size = 2*fs
    auto_peaks = autopeaks.AutoPeaks(thres=0.70, min_dist=min_dist, buffer_size=buffer_size)
    pad_value = np.median(signal)
    list(map(auto_peaks.findpeaks, signal+[pad_value]*buffer_size))
    peak_indices, peak_values = auto_peaks.peak_indexes, auto_peaks.peak_values
    end_ind = len(peak_indices)
    max_index = len(signal)
    for index in peak_indices:
        if index >= max_index:
            end_ind = index
            break
    return peak_indices[:end_ind], peak_values[:end_ind]

def bandpass_filter(signal, fs):
    b = np.loadtxt("filter/bcg_bandpass_b_" + str(fs) + ".csv", delimiter=',')
    a = np.loadtxt("filter/bcg_bandpass_a_" + str(fs) + ".csv", delimiter=',')
    signal = lfilter(b, a, signal)
    return signal

def notch_filter(signal, fs):
    b = np.loadtxt("filter/ecg_notch_b.csv", delimiter=',')
    a = np.loadtxt("filter/ecg_notch_a.csv", delimiter=',')
    signal = lfilter(b, a, signal)
    return signal


def main(unused_args):
    from fs import load_ecg
    del unused_args
    data_dir = "/home/guo/physio/BCG_data/bcg_ecg_data/bcg_ecg_data(500HZ)/"
    ecg_path = data_dir + "wsx_ecg.edf"
    ecg = load_ecg(ecg_path)
    indices, values = findpeaks_in_ecg(ecg)
    

if __name__ == '__main__':
    app.run(main)
