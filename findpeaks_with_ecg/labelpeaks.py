
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pdb
import numpy as np
import ecgpeaks
import autopeaks

from collections import deque

def candidate_peaks(bcg):
    auto_peaks = autopeaks.AutoPeaks(thres=0.65, min_dist=50, buffer_size=500)
    list(map(auto_peaks.findpeaks, bcg))
    indices, values = auto_peaks.peak_indexes, auto_peaks.peak_values
    return indices, values

def draft_peaks(bcg):
    auto_peaks = autopeaks.AutoPeaks(thres=0.72, min_dist=300, buffer_size=2000)
    list(map(auto_peaks.findpeaks, bcg))
    indices, values = auto_peaks.peak_indexes, auto_peaks.peak_values
    return indices, values

class Peak(object):

    def __init__(self, index, value):
        self.index = index
        self.value = value
        self.prev_peak = None
        self.next_peak = None

        self.is_r_peak = False
        self.j_peak = 0
        self.prev_R = 0
        self.next_R = 0

class PeakList(list):
    pass


class HeuristicPeaks(object):

    def __init__(self, bcg, ecg):
        self.bcg_peak_indices, self.bcg_peak_values = draft_peaks(bcg)
        self.ecg_peak_indices, self.ecg_peak_values = ecgpeaks.findpeaks_in_ecg(ecg)
        self.candidate_peak_indices, self.candidate_peak_values = candidate_peaks(bcg)

        self.indices_of_bcg_peak_indices = []
        #pdb.set_trace()
        bcg_peak_set = set(self.bcg_peak_indices)
        for ind, peak in enumerate(self.candidate_peak_indices):
            if peak in bcg_peak_set:
                self.indices_of_bcg_peak_indices.append(ind)
        
        self.num_ecg_peaks = len(self.ecg_peak_indices)
        self.num_candidate_peaks = len(self.candidate_peak_indices)

        self.bcg_peak_index_to_index_at_candidate = {}
        for ind, peak_index in enumerate(self.candidate_peak_indices):
            self.bcg_peak_index_to_index_at_candidate[peak_index] = ind
        
    def loss_macro(self):
        num_bcg_peaks = len(self.bcg_peak_indices)
        num_ecg_peaks = len(self.ecg_peak_indices)
        if num_bcg_peaks > num_ecg_peaks:
            self.bcg_peak_indices = self.bcg_peak_indices[:num_ecg_peaks]
            self.bcg_peak_values = self.bcg_peak_values[:num_ecg_peaks]
        if num_bcg_peaks < num_ecg_peaks:
            end_index = self.bcg_peak_indices[-1]
            end_value = self.bcg_peak_values[-1]
            for _ in range(num_ecg_peaks - num_bcg_peaks):
                self.bcg_peak_indices.append(end_index)
                self.bcg_peak_values.append(end_value)
        return np.sum(np.abs(np.diff(self.bcg_peak_indices) - np.diff(self.ecg_peak_indices)))

    def loss_micro(self, index_based_ecg_peak, cur_bcg_peak_ind):
        """
                           cur_bcg_peak_ind
        left_ecg_peak_ind, cur_ecg_peak_ind, right_ecg_peak_ind
                              OR
        left_bcg_peak_ind, cur_bcg_peak_ind, right_bcg_peak_ind
        left_ecg_peak_ind, cur_ecg_peak_ind, right_ecg_peak_ind
        """
        right_loss = 0
        left_loss = 0
        #cur_bcg_peak_ind = self.bcg_peak_indices[index_based_ecg_peak]
        cur_ecg_peak_ind = self.ecg_peak_indices[index_based_ecg_peak]
        if index_based_ecg_peak > 0:
            # left score
            left_bcg_peak_ind = self.bcg_peak_indices[index_based_ecg_peak-1]
            left_ecg_peak_ind = self.ecg_peak_indices[index_based_ecg_peak-1]
            left_bcg_interval = cur_bcg_peak_ind - left_bcg_peak_ind
            left_ecg_interval = cur_ecg_peak_ind - left_ecg_peak_ind
            left_loss = abs(left_bcg_interval - left_ecg_interval)
        if index_based_ecg_peak < self.num_ecg_peaks - 1:
            # right score
            right_bcg_peak_ind = self.bcg_peak_indices[index_based_ecg_peak+1]
            right_ecg_peak_ind = self.ecg_peak_indices[index_based_ecg_peak+1]
            right_bcg_interval = right_bcg_peak_ind - cur_bcg_peak_ind
            right_ecg_interval = right_ecg_peak_ind - cur_ecg_peak_ind
            right_loss = abs(right_bcg_interval - right_ecg_interval)
        loss = left_loss + right_loss
        return loss

    def optimize(self, epochs=100):
        for epoch in range(epochs):
            loss = self.loss_macro()
            print("epoch: {}, score_marco: {}".format(epoch, loss))
            self.optimize_single_epoch()
        
    def optimize_single_epoch(self):
        """
        TODO reformular to integer programming
        """
        for index_based_ecg_peak in range(self.num_ecg_peaks):
            from_bcg_peak_index = self.bcg_peak_indices[index_based_ecg_peak]
            cur_loss = self.loss_micro(index_based_ecg_peak, from_bcg_peak_index)
            ind_based_candidate_from_bcg_peak_index = \
                self.bcg_peak_index_to_index_at_candidate[from_bcg_peak_index]
            if ind_based_candidate_from_bcg_peak_index > 0:
                to_bcg_peak_index = \
                    self.candidate_peak_indices[ind_based_candidate_from_bcg_peak_index-1]
                to_bcg_peak_value = \
                    self.candidate_peak_values[ind_based_candidate_from_bcg_peak_index-1]
                update_loss = self.loss_micro(index_based_ecg_peak, to_bcg_peak_index)
                if update_loss < cur_loss:
                    self.bcg_peak_indices[index_based_ecg_peak] = to_bcg_peak_index
                    self.bcg_peak_values[index_based_ecg_peak] = to_bcg_peak_value
            if ind_based_candidate_from_bcg_peak_index < self.num_candidate_peaks - 1:
                to_bcg_peak_index = \
                    self.candidate_peak_indices[ind_based_candidate_from_bcg_peak_index+1]
                to_bcg_peak_value = \
                    self.candidate_peak_values[ind_based_candidate_from_bcg_peak_index+1]
                update_loss = self.loss_micro(index_based_ecg_peak, to_bcg_peak_index)
                if update_loss < cur_loss:
                    self.bcg_peak_indices[index_based_ecg_peak] = to_bcg_peak_index
                    self.bcg_peak_values[index_based_ecg_peak] = to_bcg_peak_value

def align_peaks(bcg_peaks, ecg_peaks):
    """
    default peak index match
    """
    pass


def identify_error_region(bcg_peaks, ecg_peaks):
    pass


def repair_error_region(bcg_peaks, ecg_peaks):
    pass


def find_closest_index(bcg_peaks_indices, ecg_peak_index):
    ind = np.argmin(np.abs(np.asarray(bcg_peaks_indices - ecg_peak_index)))
    return bcg_peaks_indices[ind]


def error_baseline(errors):
    num_error = len(errors)
    kernel_size = 60
    baseline = []
    for i in range(num_error):
        pass
        

def error_peaks(bcg_peaks_indices, ecg_peaks_indices):
    num_ecg_peaks = len(ecg_peaks_indices)
    errors = []
    for ecg_peak_index in ecg_peaks_indices:
        bcg_peak_index = find_closest_index(bcg_peaks_indices, ecg_peak_index)
        error = bcg_peak_index - ecg_peak_index
        errors.append(error)
    return errors





