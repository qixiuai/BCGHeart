
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

from collections import deque


def best_jj_interval(intervals):
    hist, bin_edges = np.histogram(intervals)
    ind = np.argmax(hist)
    max_bin_start = bin_edges[ind]
    max_bin_end = bin_edges[ind+1]
    bin_intervals = []
    for interval in intervals:
        if (interval >= max_bin_start and interval <= max_bin_end):
            bin_intervals.append(interval)
    best_interval = np.median(bin_intervals)
    return best_interval


def refine_peaks(interval):
    pass


class PeakRefiner(object):

    def __init__(self):
        self.peak_buffer = []

    def refine(self, peak):
        self.peak_buffer.append(peak)
        
    def refine_peaks(self, peaks):
        pass


if __name__ == "__main__":
    pass



