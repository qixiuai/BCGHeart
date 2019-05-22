
import autopeaks
import numpy as np

from collections import deque
from scipy.signal import medfilt


class BCGPeaks(object):

    def __init__(self, fs=500):
        self._fs = fs
        self._signal = []
        
        self._peak_indices_hist = []
        self._peak_values_hist = []
        self._intervals_hist = []
        self._intervals_denoised = deque()
        self._autopeaks = autopeaks.AutoPeaks(thres=0.72, min_dist=int(0.6*fs), buffer_size=2*fs)

        self._is_signal_end = False
        self._denoise_time_residual = 0
                
    def _denoise_intervals(self):
        peak_indices = self._autopeaks.peak_indexes
        peak_values = self._autopeaks.peak_values
        if not peak_indices:
            return

        self._peak_indices_hist.extend(peak_indices)
        self._peak_values_hist.extend(peak_values)

        if self._peak_indices_hist:
            peak_indices.insert(0, self._peak_indices_hist[-1])

        new_intervals_raw = np.diff(peak_indices)
        new_intervals_denoised = []
        num_intervals_hist = len(self._intervals_hist)
        mean_rolling = np.median(
            self._intervals_hist[-10:] if num_intervals_hist >= 10 else self._intervals_hist)
        new_interval_upper = mean_rolling + 0.10*mean_rolling
        new_interval_lower = mean_rolling - 0.10*mean_rolling
        for new_interval in new_intervals_raw:
            if new_interval > new_interval_upper:
                residual = new_interval_upper - new_interval
                self._denoise_time_residual -= residual
                new_interval = new_interval_upper
            if new_interval < new_interval_lower:
                residual = new_interval - new_interval_lower
                self._denoise_time_residual += residual
                new_interval = new_interval_lower
            new_intervals_denoised.append(new_interval)
        self._intervals_hist.extend(new_intervals_raw)
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
                self._denoise_time_residual - new_interval
        return intervals

    def reset(self):
        self._autopeaks.clear()

    def set_signal_end(self):
        pad_value = np.median(self._signal)
        end_of_index = len(self._signal)
        self._autopeaks.set_signal_end(pad_value, end_of_index)
        self._is_signal_end = True
        
    def findpeaks(self, sample):
        self._signal.append(sample)
        self._autopeaks.findpeaks(sample)


        
