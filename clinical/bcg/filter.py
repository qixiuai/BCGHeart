
import numpy as np
from scipy.signal import lfilter

def bandpass_filter(signal, fs=500):
    b = np.loadtxt("filter/bcg_bandpass_b_" + str(fs) + ".csv", delimiter=',')
    a = np.loadtxt("filter/bcg_bandpass_a_" + str(fs) + ".csv", delimiter=',')
    signal = lfilter(b, a, signal)
    return signal

def notch_filter(signal, fs=500):
    b = np.loadtxt("filter/ecg_notch_b_" + str(fs) + ".csv", delimiter=',')
    a = np.loadtxt("filter/ecg_notch_a_" + str(fs) + ".csv", delimiter=',')
    signal = lfilter(b, a, signal)
    return signal





