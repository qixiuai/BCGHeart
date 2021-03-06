
import numpy as np


def transform_signal_by_energy(signal, window_size=0.3, fs=100):
    energy = []
    window_size = int(window_size*fs)
    for ind in range(len(signal)-window_size+1):
        window = signal[ind:ind+window_size]
        energy.append(np.dot(window, window))
    return np.asarray(energy)

def transform_signal_by_energy_l1(signal, fs=100):
    energy = []
    window_size = int(0.3*fs)
    for ind in range(len(signal)-window_size+1):
        window = signal[ind:ind+window_size]
        energy.append(np.sum(np.abs(window)))
    return np.asarray(energy)

def transform_signal_by_energy_l4(signal, fs=100):
    energy = []
    window_size = int(0.3*fs)
    for ind in range(len(signal)-window_size+1):
        window = signal[ind:ind+window_size]
        W = window
        energy.append(np.sum(W*W*W*W))
    return np.asarray(energy)

def findpeaks3(signal, min_dist=300, thres=0.70, direction="down"):
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
        peak_score = 0
        #direction = direction
        return Peak(peak_index, peak_value, front_index, front_value, front_front_index, front_front_value,
                    back_index, back_value, back_back_index, back_back_value, indicator_value, direction, peak_score)
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
