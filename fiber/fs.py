
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

from edfplus import Edfplus
from bcg import load_bcg
from scipy.signal import lfilter
from scipy.signal import resample_poly

import pdb

def load_ecg(filepath, filter=True, resp=False):
    #with open(filepath, "rb") as file:
    #    raw = file.read()
    #    print(raw[150:200])
    edf = Edfplus(filepath)
    if resp:
        signal = edf.signals["Resp chest"]
        signal = resample_poly(signal, 5, 1)
        return signal
    ecg = edf.signals['ECG LL-RA']
    if filter:
        ecg = notch_filter(ecg)
    return ecg

def notch_filter(signal):
    b = np.loadtxt("filter/ecg_notch_b.csv", delimiter=',')
    a = np.loadtxt("filter/ecg_notch_a.csv", delimiter=',')
    signal_filter = lfilter(b, a, signal)
    return signal_filter

def lowpass_filter(signal, fs=100):
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

if __name__ == '__main__':
    pass


