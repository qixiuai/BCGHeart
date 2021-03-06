
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pdb
import autopeaks

from fs import load_ecg


def findpeaks_in_ecg(signal, fs=500):
    """
    """
    min_dist = int(fs * 0.6)
    auto_peaks = autopeaks.AutoPeaks(thres=0.65, min_dist=min_dist, buffer_size=2*fs)
    list(map(auto_peaks.findpeaks, signal))
    return (auto_peaks.peak_indexes, auto_peaks.peak_values)


def main(unused_args):
    del unused_args
    data_dir = "/home/guo/physio/BCG_data/bcg_ecg_data/bcg_ecg_data(500HZ)/"
    ecg_path = data_dir + "wsx_ecg.edf"
    ecg = load_ecg(ecg_path)
    indices, values = findpeaks_in_ecg(ecg)
    

if __name__ == '__main__':
    app.run(main)
