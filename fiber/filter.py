
from scipy.signal import lfilter
import numpy as np

def bandpass_filter(signal):
    b = np.loadtxt("filter/bcg_bandpass_b.csv", delimiter=',')
    a = np.loadtxt("filter/bcg_bandpass_a.csv", delimiter=',')
    signal_filter = lfilter(b, a, signal)
    return signal_filter

def bandpass_filter2(signal):
    b = np.loadtxt("filter/bandpass_b_500.csv", delimiter=',')
    a = np.loadtxt("filter/bandpass_a_500.csv", delimiter=',')
    signal_filter = lfilter(b, a, signal)
    return signal_filter

def notch_filter(signal):
    b = np.loadtxt("filter/ecg_notch_b.csv", delimiter=',')
    a = np.loadtxt("filter/ecg_notch_a.csv", delimiter=',')
    signal_filter = lfilter(b, a, signal)
    return signal_filter

def highpass_filter(signal, cut_freq=1):
    b = np.loadtxt("filter/highpass{}_b_500.csv".format(cut_freq), delimiter=',')
    a = np.loadtxt("filter/highpass{}_a_500.csv".format(cut_freq), delimiter=',')
    signal_filter = lfilter(b, a, signal)
    return signal_filter

def lowpass_filter(signal, fs=500, cut_freq=30):
    if fs == 100:
        b = np.loadtxt("filter/lowpass0.4_b_100.csv", delimiter=',')
        a = np.loadtxt("filter/lowpass0.4_a_100.csv", delimiter=',')
    elif fs == 500:
        if cut_freq == 30:
            b = np.loadtxt("filter/lowpass35_b_500.csv", delimiter=',')
            a = np.loadtxt("filter/lowpass35_a_500.csv", delimiter=',')
        else:
            b = np.loadtxt("filter/lowpass0.4_b_500.csv", delimiter=',')
            a = np.loadtxt("filter/lowpass0.4_a_500.csv", delimiter=',')
    else:
        raise Exception("unexpected fs {}".format(fs))
    signal_filter = lfilter(b, a, signal)
    return signal_filter
