
from scipy.signal import lfilter
import numpy as np

def bandpass_filter(signal):
    b = np.loadtxt("filter/bcg_bandpass_b.csv", delimiter=',')
    a = np.loadtxt("filter/bcg_bandpass_a.csv", delimiter=',')
    signal_filter = lfilter(b, a, signal)
    return signal_filter

def notch_filter(signal):
    b = np.loadtxt("filter/ecg_notch_b.csv", delimiter=',')
    a = np.loadtxt("filter/ecg_notch_a.csv", delimiter=',')
    signal_filter = lfilter(b, a, signal)
    return signal_filter

def lowpass_filter(signal, fs=500):
    if fs == 100:
        b = np.loadtxt("filter/lowpass0.4_b_100.csv", delimiter=',')
        a = np.loadtxt("filter/lowpass0.4_a_100.csv", delimiter=',')
    elif fs == 500:
        b = np.loadtxt("filter/lowpass0.4_b_500.csv", delimiter=',')
        a = np.loadtxt("filter/lowpass0.4_a_500.csv", delimiter=',')
    else:
        raise Exception("unexpected fs {}".format(fs))
    signal_filter = lfilter(b, a, signal)
    return signal_filter
