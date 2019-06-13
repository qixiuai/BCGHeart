
import autopeaks
import numpy as np
import pdb

from collections import deque
from scipy.signal import medfilt
from filter import BandpassFilter
from filter import NotchFilter


class BCGPeaks(object):

    def __init__(self, fs=500):
        self._fs = fs
        self._bandpass_filter = BandpassFilter(fs)
        self._notch_filter = NotchFilter(fs)

        self._signal_raw = []
        self._signal = []

        self._peak_indices_hist = []
        self._peak_values_hist = []
        self._intervals_hist = []
        self._intervals_denoised = deque()
        self._autopeaks = autopeaks.AutoPeaks(thres=0.75, min_dist=int(0.6*fs), buffer_size=2*fs)

        self._is_signal_end = False
        self._denoise_time_residual = 0

    def _denoise_intervals(self):
        peak_indices = self._autopeaks.peak_indexes
        peak_values = self._autopeaks.peak_values
        if not peak_indices:
            return

        if self._peak_indices_hist:
            peak_indices.insert(0, self._peak_indices_hist[-1])

        self._peak_indices_hist.extend(peak_indices)
        self._peak_values_hist.extend(peak_values)

        if len(self._peak_indices_hist) == 1:
            return

        new_intervals_raw = np.diff(peak_indices)
        """
        kernel_size = 9
        if self._intervals_hist:
            pass
            new_intervals_raw.insert(0, self._intervals_hist[-1])
            new_intervals_raw.insert(0, self._intervals_hist[-1])
        """
        self._intervals_hist.extend(new_intervals_raw)

        not_denoise = False
        if not_denoise:
            self._intervals_denoised.extend(new_intervals_raw)
            return
        # get move median
        #mean_rollings = medfilt(new_intervals_raw, kernel_size=31)
        mean_rollings = []
        num_new_intervals = len(new_intervals_raw)
        num_intervals_hist = len(self._intervals_hist)
        def mean_interval(intervals):
            hist,bin_edges = np.histogram(intervals,bins=5,range=(300,750))
            ind = np.argmax(hist)
            min, max = bin_edges[ind], bin_edges[ind+1]
            cluster = []
            for interval in intervals:
                if interval >= min and interval <= max:
                    cluster.append(interval)
            return np.median(cluster)
        for ind in range(num_intervals_hist-num_new_intervals, num_intervals_hist):
            mean_rollings.append(mean_interval(self._intervals_hist[ind-15 if ind-15>=0 else 0:ind+15]))
        new_intervals_denoised = []
        for ind, new_interval in enumerate(new_intervals_raw):
            mean_rolling = mean_rollings[ind]
            new_interval_upper = int(mean_rolling + 0.10*mean_rolling)
            new_interval_lower = int(mean_rolling - 0.10*mean_rolling)
            new_interval_cur = new_interval
            if new_interval > new_interval_upper:
                #new_interval_cur = new_interval_upper + np.random.randint(-5,5)
                new_interval_cur = np.mean(new_intervals_raw[ind-5 if ind-5 >= 0 else 0 : ind+5])
                residual = new_interval - new_interval_cur
                new_interval = new_interval_upper
            if new_interval < new_interval_lower:
                #new_interval_cur = new_interval_lower + np.random.randint(-5, 5)
                new_interval_cur = np.mean(new_intervals_raw[ind-5 if ind-5 >= 0 else 0 : ind+5])
                residual = new_interval_cur - new_interval
                self._denoise_time_residual -= residual
            new_intervals_denoised.append(new_interval_cur)
        self._intervals_denoised.extend(new_intervals_denoised)

    @property
    def intervals(self):
        self._denoise_intervals()
        intervals = list(self._intervals_denoised)
        self._intervals_denoised.clear()

        if self._is_signal_end:
            ind = len(self._intervals_hist) - 1
            new_interval = self._intervals_hist[ind]
            self._denoise_time_residual -= new_interval
            while self._denoise_time_residual > 0:
                intervals.append(new_interval)
                ind -= 1
                new_interval = self._intervals_hist[ind]
                self._denoise_time_residual -= new_interval
        return intervals

    def reset(self):
        self._autopeaks.clear()

    def set_signal_end(self):
        pad_value = np.median(self._signal)
        end_of_index = len(self._signal)
        self._autopeaks.set_signal_end(pad_value, end_of_index)
        self._is_signal_end = True
        
    def findpeaks(self, sample):
        sample = self._bandpass_filter.filter([sample])[0]
        sample = self._notch_filter.filter([sample])[0]
        self._signal.append(sample)
        self._autopeaks.findpeaks(sample)




        
