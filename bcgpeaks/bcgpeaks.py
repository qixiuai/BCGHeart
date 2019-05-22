
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import autopeaks
import plotly.graph_objs as go

from absl import app
from collections import namedtuple
from collections import deque
from itertools import product
from plotly.offline import plot
from scipy.signal import lfilter

from bcg import load_bcg

class Sample(object):

    def __init__(self, index, value):
        self.index = index
        self.value = value
        self.next = []
        self.prev = []
    pass


class Peak(object):

    def __init__(self, index, value):
        self.index = index
        self.value = value
    pass


class Cycle(object):
    pass


def body_movement(signal):
    auto_peaks = autopeaks.AutoPeaks(thres=0.5, min_dist=60, fs=500, buffer_size=200)
    list(map(auto_peaks.findpeaks, signal))
    peak_indices = auto_peaks.peak_indexes
    peak_values = auto_peaks.peak_values
    base_buffer = deque(maxlen=60*5)
    in_event = False
    mts = []
    start = 0
    end = 0
    prev_index = 0
    base_buffer.append(peak_values[0])
    for (index, value) in zip(peak_indices, peak_values):
        l = list(base_buffer)
        l.sort()
        base = l[int(0.9*len(l))]
        mt_thres_start = base * 2
        mt_thres_end = base * 1.5
        if not in_event and value >= mt_thres_start:
            in_event = True
            start = prev_index
        if in_event and value <= mt_thres_end:
            end = index
            mts.append((start,end))
            start = end = 0
            in_event = False
        if not in_event:
            base_buffer.append(value)
        prev_index = index

    # merge mt series to a single mt
    final_mts = []
    num_mts = len(mts)
    mt = mts[0]
    prev_start = mt[0] 
    prev_end = mt[1]
    for ind in range(1, num_mts):
        mt = mts[ind]
        cur_start = mt[0]
        cur_end = mt[1]
        if (cur_start - prev_end) > 0.5 * 500:
            final_mts.append((prev_start, prev_end))
            prev_start = cur_start
            prev_end = cur_end
        prev_end = cur_end
    final_mts.append((prev_start, prev_end))
    return mts


def repair_body_movement(signal, mts):
    """
    ratio = (max(normal) - min(normal)) / (max(mt) - min(mt))
    mt /= ratio
    """
    normal = deque(maxlen=10*500)
    mt_ind = 0
    num_mts = len(mts)
    mt = mts[mt_ind]
    mt_start = mt[0]
    mt_end = mt[1]    
    new_signal = np.copy(signal)
    num_samples = len(signal)
    ind = 0
    while (ind < num_samples):
        sample = signal[ind]

        # keep normal
        if ind < mt_start:
            normal.append(sample)
            ind += 1
            continue
        
        # repair
        if ind >= mt_start:
            mt_signal = signal[mt_start:mt_end]
            normal_max = np.max(normal)
            normal_min = np.min(normal)
            mt_max = np.max(mt_signal)
            mt_min = np.min(mt_signal)
            ratio = normal_max / mt_max
            new_signal[mt_start:mt_end] = mt_signal * ratio
            mt_ind += 1
            if mt_ind >= num_mts:
                break
            mt = mts[mt_ind]
            mt_start = mt[0]
            mt_end = mt[1]
            ind = mt_end

        ind += 1
    return new_signal


def approximate_jj_interval(intervals):
    return np.median(intervals)

def variance_jj_interval(intervals):
    return np.std(intervals)


def benchmark_model(signal):
    # 1. bandpass
    # 2. remove MT
    #
    # repeat from 1 - 3
    # 1. findpeaks from high prob to low
    # 2. mean JJ interval
    # 3. patterned error remove
    #

    # remove body movement
    mts = body_movement(signal)
    new_signal = repair_body_movement(signal, mts)

    # find peaks
    bcg_auto_peaks = autopeaks.AutoPeaks(thres=0.70, min_dist=300, fs=500)
    list(map(bcg_auto_peaks.findpeaks, new_signal))
    bcg_peak_indices = bcg_auto_peaks.peak_indexes
    bcg_peak_values = bcg_auto_peaks.peak_values

    bcg_auto_peaks_mini = autopeaks.AutoPeaks(thres=0.65, min_dist=60, fs=500)
    list(map(bcg_auto_peaks_mini.findpeaks, new_signal))
    bcg_peak_indices_mini = bcg_auto_peaks_mini.peak_indexes
    bcg_peak_values_mini = bcg_auto_peaks_mini.peak_values
    
    bcg_jj = np.diff(bcg_peak_indices)
    
    final_peak_indices = np.copy(bcg_peak_indices)
    
    # interval finetune
    ### check normal or abnormal JJ intervals
    flags = []
    mean_interval = np.median(bcg_jj)
    std_interval = np.std(bcg_jj)
    interval_max = mean_interval + 2 * std_interval
    interval_min = mean_interval - 2 * std_interval
    for interval in bcg_jj:
        if interval > interval_max:
            flags.append(1)
        elif interval < interval_min:
            flags.append(-1)
        else:
            flags.append(0)

    abnormal_start = 0
    abnormal_end = 0
    num_jj = len(bcg_jj)
    in_abnormal = True
    for ind_jj in range(num_jj):
        flag = flags[ind_jj]
        if in_abnormal and flag == 0:
            abnormal_end = ind_jj - 1

            # handle abnormal
            ### handle small, big pattern
            start_interval = bcg_jj[abnormal_start]
            end_interval = bcg_jj[abnormal_end]
            if abnormal_end - abnormal_start == 1 and \
               start_interval < mean_interval and \
               end_interval > mean_interval:
                # caused by one error peak
                error_peak = bcg_peak_indices[abnormal_start+1]
                peak_end = bcg_peak_indices[abnormal_end+1]
                new_peak_index = find_new_peak(bcg_peak_indices_mini,
                                               bcg_peak_values_mini,
                                               error_peak, peak_end)
                final_peak_indices[abnormal_start+1] = new_peak_index

            if abnormal_end - abnormal_start > 1:
                all_large = np.sum(bcg_jj[abnormal_start:abnormal_end] - 1) == 0
                if all_large:
                    pass
                else:
                    pass

        if not in_abnormal and flag != 0:
            abnormal_start = ind_jj


def metrics(autopeaks):
    """ 
    1. quality of convergence for intervals
    2. distribution of peak values
    3. hrv variability
    """
    pass


def findpeaks_parallel(signal):
    thres = range(50, 85, 5)
    min_dist = range(100, 500, 50)
    result = []
    for (t, d) in product(thres, min_dist):
        thres = t / 100
        min_dist = d
        print(t,d)
        auto_peaks = autopeaks.AutoPeaks(thres=thres, min_dist=min_dist, fs=500)
        result.append(auto_peaks)
    return result


def merge_peaks(auto_peaks):
    """
    1. find median cycle
    2. merge by segment
    """
    pass


def main(unused_args):
    del unused_args

    # load bcg
    bcg_path = "/home/guo/BCGHeart/data/wsx_bcg_wave(500HZ).txt"
    signal = load_bcg(bcg_path, offset=12726, filter=True)

    # find peaks with best thres and min_dist
    auto_peaks = findpeaks_parallel(signal)

    # merge findpeaks results
    
    
    # peak finetune
    
    


if __name__ == '__main__':
    app.run(main)


