
from collections import deque
import numpy as np


class HeartRateInference(object):

    def __init__(self,
                 window_size_base=60*2,
                 window_size_instant=60*1,
                 amplitude_deviation_threshold=0.1,
                 base_heart_method="histogram"):
        self.window_size_base = window_size_base
        self.window_size_instant = window_size_instant
        self.amplitude_deviation_threshold = amplitude_deviation_threshold
        self.base_heart_method = base_heart_method
        self.base_pool = deque(maxlen=window_size_base)
        self.instant_pool = deque(maxlen=window_size_instant)

    @property
    def base_heart(self):
        base = 0
        if self.base_heart_method == "median":
            base = np.median(self.base_pool)
        elif self.base_heart_method == "histogram":
            hists, edges = np.histogram(self.base_pool,bins=5)
            ind = np.argmax(hists)
            min_edge, max_edge = edges[ind], edges[ind+1]
            bucket = []
            for interval in self.base_pool:
                if interval >= min_edge and interval <= max_edge:
                    bucket.append(interval)
            base = np.median(bucket)
        else:
            raise Exception("unexpected base heart method: {}".format(self.base_heart_method))
        return base

    @property
    def mean_instant_heart(self):
        return np.median(self.instant_pool)

    def is_normal(self, interval):
        flag = True
        if len(self.base_pool) < self.window_size_base:
            return flag
        deviation = np.abs(interval - self.base_heart) / self.base_heart
        if deviation > self.amplitude_deviation_threshold:
            flag = False
        return flag

    def add_to_base_pool(self, interval):
        self.base_pool.append(interval)

    def add_to_instant_pool(self, interval):
        self.instant_pool.append(interval)

    def inference(self, interval):
        self.add_to_base_pool(interval)
        if self.is_normal(interval):
            self.add_to_instant_pool(interval)
            interval = interval
        else:
            interval = self.mean_instant_heart
        return interval



