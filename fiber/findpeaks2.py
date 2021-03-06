
import pdb
import numpy as np
from collections import namedtuple

# use namedtuple instead class because unmutable is more safe than mutable types
class Peak(namedtuple("Peak",
                  ["peak_index", "peak_value", 
                   "front_index", "front_value",
                   "front_front_index", "front_front_value",
                   "back_index", "back_value",
                   "back_back_index", "back_back_value",
                   "indicator_value", "direction", "peak_energy", "peak_score"])):
    def __gt__(self, other):
        if self.direction in ["up", "UP"]:
            peak_score = self.peak_value > other.peak_value
        elif self.direction in ["down", "DOWN"]:
            peak_score = self.peak_value < other.peak_value
        else:
            raise Exception("unexpected direction")
        level1_score = self.front_value + self.back_value > other.front_value + other.back_value
        #back_score = self.back_value >= other.back_value
        level2_score = self.front_front_value + self.back_back_value >= other.front_front_value + other.back_back_value
        #level2_score = self.peak_energy >= other.peak_energy
        #back_back_score = self.back_back_value > other.back_back_value
        score = int(peak_score) + int(level1_score) + int(level2_score)
        #pdb.set_trace()
        is_greater = True if score >= 2 else False
        return is_greater

    def __lt__(self, other):
        return not self.__gt__(other)

    def __eq__(self, other):
        state = self.peak_value == other.peak_value and \
                self.front_value == other.front_value and \
                self.front_front_value == other.front_front_value and \
                self.back_value == other.back_value and \
                self.back_back_value == other.back_back_value
        return state

Extrema = namedtuple("Extrema", ["index", "value", "category"])

def findpeaks2(signal, min_dist=300, thres=0.70, direction="down", energy_window=75):
    if isinstance(signal, list):
        signal = np.asarray(signal)
    diff1_signal = np.diff(signal)
    diff1_abs_signal = np.abs(diff1_signal)
    diff2_signal = np.diff(diff1_abs_signal)

    maximas = np.where((np.hstack([diff2_signal, 0]) <= 0)
                       & (np.hstack([0, diff2_signal]) > 0))[0] + 1
    
    thres_signal = 0.5 * (np.max(signal) - np.min(signal)) + np.min(signal)
    if direction in ["UP", "up"]:
        minimas = np.where((np.hstack([diff1_signal, 0]) <= 0)
                           & (np.hstack([0, diff1_signal]) > 0)
                           & (np.greater(signal, thres_signal)))[0]
    elif direction in ["DOWN", "down"]:
        minimas = np.where((np.hstack([diff1_signal, 0]) >= 0)
                           & (np.hstack([0, diff1_signal]) < 0)
                           & (np.less(signal, thres_signal)))[0]
    else:
        # auto direction
        #minimas = np.where((np.hstack([diff2_signal, 0]) >= 0)
        #                   & (np.hstack([0, diff2_signal]) < 0))[0] + 1
        raise Exception("must offer direction")

    maximas = list(map(lambda x:Extrema(x, diff1_abs_signal[x-1], "max"), maximas))
    # only keep 50% maximas, because A cycle at least has 8 maximas, we only need 4
    maximas.sort(key=lambda maxima:maxima.value,reverse=True)
    num_maximax = len(maximas)
    maximas = maximas[:int(num_maximax*0.8+1)]
    
    minimas = list(map(lambda x:Extrema(x, 0, "min"), minimas))
    extremas = maximas + minimas
    extremas.sort(key=lambda x:x.index)
    if len(extremas) < 5:
        return np.asarray([])
    
    def make_peak(zero_extrema, front_extrema, front_front_extrema, back_extrema, back_back_extrema):
        peak_index = zero_extrema.index
        peak_value = signal[peak_index]
        front_index = front_extrema.index
        front_value = diff1_abs_signal[front_index-1]
        front_front_index = front_front_extrema.index
        front_front_value = diff1_abs_signal[front_front_index-1]
        back_index = back_extrema.index
        back_value = diff1_abs_signal[back_index-1]
        back_back_index = back_back_extrema.index
        back_back_value = diff1_abs_signal[back_back_index-1]
        #indicator_value = front_value + front_front_value + back_value + back_back_value
        indicator_value = front_value + back_value
        window_st = peak_index - energy_window
        window_st = window_st if window_st >= 0 else 0
        window_ed = peak_index + energy_window
        window = diff1_abs_signal[window_st:window_ed]
        peak_energy = np.dot(window, window)
        peak_score = 0
        #direction = direction
        return Peak(peak_index, peak_value, front_index, front_value, front_front_index, front_front_value,
                    back_index, back_value, back_back_index, back_back_value, indicator_value, direction, peak_energy, peak_score)
    raw_extremas = extremas.copy()

    def find_maxima(range_indices):
        for index in range_indices:
            extrema = extremas[index]
            if extrema.category == "max":
                return extrema
        return None

    peaks = []
    end_extrema_index = len(extremas)
    for ind in range(2, len(extremas)-2):
        curr_extrema = extremas[ind]
        if curr_extrema.category != "min":
            continue
        prev_extrema = find_maxima(range(ind-1,-1,-1))
        if prev_extrema is None:
            continue
        prev_prev_extrema = find_maxima(range(ind-2,-1,-1))
        if prev_prev_extrema is None:
            continue
        next_extrema = find_maxima(range(ind+1,end_extrema_index))
        if next_extrema is None:
            continue
        next_next_extrema = find_maxima(range(ind+2,end_extrema_index))
        if next_next_extrema is None:
            continue
        peak = make_peak(curr_extrema, prev_extrema, prev_prev_extrema, next_extrema, next_next_extrema)
        peaks.append(peak)

    # add peak score
    peaks_with_score = []
    for curr_peak in peaks:
        score = 0
        for peak in peaks:
            if curr_peak > peak:
                score += 1
        args = list(curr_peak)
        args[-1] = score
        peaks_with_score.append(Peak(*args))
        #pdb.set_trace()
    peaks = peaks_with_score
    raw_peaks = peaks.copy()

    if not peaks:
        return [], [], [], 0
    
    # apply thres
    max_indicator = max(peaks,key=lambda peak:peak.indicator_value).indicator_value
    min_indicator = min(peaks,key=lambda peak:peak.indicator_value).indicator_value
    thres_abs = min_indicator + thres * (max_indicator - min_indicator)
    peaks = list(filter(lambda peak:peak.indicator_value >= thres_abs, peaks))
    
    # apply min_dist
    #peaks.sort(key=lambda peak:peak.peak_index)
    #num_masks = len(masks)
    highest_peaks = peaks.copy()
    masks = np.ones(len(signal), dtype=np.bool)
    highest_peaks.sort(key=lambda peak:peak.peak_score, reverse=True)
    for peak in highest_peaks:
        peak_index = peak.peak_index
        if masks[peak_index]:
            sl = slice(max(0, peak_index-min_dist), peak_index + min_dist + 1)
            masks[sl] = False
            masks[peak_index] = True
    peak_indices = np.arange(len(signal))[masks]
    j_peaks = list(filter(lambda peak:peak.peak_index in peak_indices, peaks))
    return j_peaks, raw_extremas, raw_peaks, thres_abs
    """
    def mask_neghbour_peaks(peak_index_min, peak_index_max, center_peak):
        for ind in range(num_masks):
            mask = masks[ind]
            if mask:
                peak = peaks[ind]
                peak_index = peak.peak_index
                if peak_index >= peak_index_min and peak_index <= peak_index_max:
                    #if center_peak > peak:
                    masks[ind] = False
            
    for mask_index, peak in highest_peaks:
        if masks[mask_index]:
            peak_index = peak.peak_index
            peak_index_min = max(0, peak_index - min_dist)
            peak_index_max = peak_index + min_dist
            mask_neghbour_peaks(peak_index_min, peak_index_max, peak)
            masks[mask_index] = True
    j_peaks = []
    for ind in range(num_masks):
        mask = masks[ind]
        if mask:
            j_peaks.append(peaks[ind])
    """
    
    """
    def find_next_peak(ind):
        while True:
            if ind >= num_masks:
                return None, ind
            mask = masks[ind]
            if mask:
                break
            ind += 1
        return peaks[ind], ind

    curr_ind = 0
    while True:
        curr_peak, curr_ind = find_next_peak(curr_ind)
        if curr_peak is None:
            break
        next_peak, next_ind = find_next_peak(curr_ind+1)
        if next_peak is None:
            break
        dist = next_peak.peak_index - curr_peak.peak_index
        if dist < min_dist:
            if curr_peak > next_peak:
                masks[next_ind] = False
            else:
                masks[curr_ind] = False
        else:
            curr_ind += 1
    """

