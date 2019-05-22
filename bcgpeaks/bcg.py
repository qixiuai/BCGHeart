
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import numpy as np

from scipy.signal import lfilter


def _parse_integer(bytes):
    int_str = bytes.decode('ASCII')
    integers = []
    #try:
    #integers = list(map(int, int_str.split(',')))
    for s in int_str.split(','):
        try:
            integer = int(s)
        except:
            print(bytes)
            continue
        integers.append(integer)
    #except:
        #raise ValueError("")
    return integers
    
def _parse_bcg(bytes):
    data = []
    packet = []
    start_index = 0
    end_index = 0
    for ind, byte in enumerate(bytes):
        if byte == ord('#'):
            if end_index - start_index > 0:
                #print(start_index, end_index)
                integers = _parse_integer(bytes[start_index:end_index])
                data.extend(integers)
            start_index = ind + 1
            end_index = ind + 1
        if byte == ord('\r'):
            end_index = ind
    if end_index - start_index > 0:
        integers = _parse_integer(bytes[start_index:end_index])
        data.extend(integers)
    return data
    

def load_bcg(filepath, offset=0, filter=True):
    f = open(filepath, 'rb')
    raw = f.read()
    f.close()
    signal = _parse_bcg(raw)
    signal = signal[offset:]
    if filter:
        signal = bandpass_filter(signal)
    return signal
    

def bandpass_filter(signal):
    b = np.loadtxt("filter/bcg_bandpass_b.csv", delimiter=',')
    a = np.loadtxt("filter/bcg_bandpass_a.csv", delimiter=',')
    signal_filter = lfilter(b, a, signal)
    return signal_filter


