
import numpy as np
from scipy.signal import lfilter
from scipy.signal import lfilter_zi
from collections import deque


def bandpass_filter(signal, fs=500):
    b = np.loadtxt("filter/bandpass_b_" + str(fs) + ".csv", delimiter=',')
    a = np.loadtxt("filter/bandpass_a_" + str(fs) + ".csv", delimiter=',')
    signal = lfilter(b, a, signal)
    return signal

def notch_filter(signal, fs=500):
    b = np.loadtxt("filter/notch_b_" + str(fs) + ".csv", delimiter=',')
    a = np.loadtxt("filter/notch_a_" + str(fs) + ".csv", delimiter=',')
    signal = lfilter(b, a, signal)
    return signal


class Medfilter(object):

    def __init__(self, kernel_size=9):
        self.kernel_size = kernel_size
        self.buffer = deque(maxlen=kernel_size)

    def medfilt(signal):
        if not isinstance(signal, list):
            signal = [signal]
        self.buffer.extend(signal)
        return np.median(self.buffer)

class BandpassFilter(object):

    def __init__(self, fs=500):
        self.b = np.loadtxt("filter/bandpass_b_" + str(fs) + ".csv", delimiter=',')
        self.a = np.loadtxt("filter/bandpass_a_" + str(fs) + ".csv", delimiter=',')
        self.zi = lfilter_zi(self.b, self.a)
        
    def filter(self, signal):
        signal, self.zi = lfilter(self.b, self.a, signal, zi=self.zi)
        return signal


class NotchFilter(object):

    def __init__(self, fs=500):
        self.b = np.loadtxt("filter/notch_b_" + str(fs) + ".csv", delimiter=',')
        self.a = np.loadtxt("filter/notch_a_" + str(fs) + ".csv", delimiter=',')
        self.zi = lfilter_zi(self.b, self.a)
        
    def filter(self, signal):
        signal, self.zi = lfilter(self.b, self.a, signal, zi=self.zi)
        return signal
