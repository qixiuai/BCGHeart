
import numpy as np

from absl import app
from autopeaks import AutoPeaks
from scipy.signal import medfilt


def findpeaks(signal):
    auto_peaks = AutoPeaks(thres=0.72, min_dist=300, buffer_size=1000)
    list(map(auto_peaks.findpeaks, signal))
    peak_indices = auto_peaks.peak_indexes
    peak_values = auto_peaks.peak_values
    return (peak_indices, peak_values)


def denoise_peaks(intervals):
    duration_before = np.sum(intervals)
    intervals_medfilt = medfilt(intervals, kernel_size=5)
    mean = np.median(intervals)
    intervals_final = []
    num_intervals = len(intervals)
    for ind in range(num_intervals):
        interval = intervals_medfilt[ind]
        if np.abs(interval - mean) > 0.20 * mean:
            interval = mean
        intervals_final.append(interval)
    duration_cur = np.sum(intervals_final)
    num_new_interval = int((duration_before - duration_cur) / mean)
    if num_new_interval > 0:
        for ind in range(num_new_interval):
            intervals_final.append(mean)
    elif num_new_interval < 0:
        for ind in range(-num_new_interval+1):
            intervals_final.pop()
    else:
        pass
    return intervals_final


def findpeaks_clinical(signal):
    peak_indices, peak_values = findpeaks(signal)
    intervals = np.diff(peak_indices)
    intervals_denoise = denoise_peaks(intervals)
    return peak_indices, peak_values, intervals_denoise


def main(unused_args):
    del unused_args


if __name__ == '__main__':
    app.run(main)

