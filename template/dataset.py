
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt

from absl import app
from collections import Counter
from edfplus import Edfplus
from glob import glob
from scipy.signal import resample_poly


def _parse_integer(bytes):
    int_str = bytes.decode('ASCII')
    integers = []
    try:
        integers = list(map(int, int_str.split(',')))
    except e:
        print(int_str)
        raise e
    return integers
    
def parse_bcg(bytes):
    data = []
    packet = []
    start_index = 0
    end_index = 0
    for ind, byte in enumerate(bytes):
        if byte == ord('#'):
            if end_index - start_index > 0:
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

def load_bcg(filepath):
    with open(filepath, "rb") as file:
        data = file.read()
    bcg = parse_bcg(data)
    return bcg

def load_ecg(filepath, resample=True):
    with open(filepath, "rb") as file:
        data = file.read()
    edf = Edfplus(data)
    ecg = edf.signals['ECG LL-RA']
    if resample:
        ecg = resample_poly(ecg, 2, 1)
    return ecg


class Dataset(object):

    def __init__(self, data_dir="/home/guo/BCGHeart/data/", have_ecg=False):
        self.bcg_files = glob(data_dir+"*.txt")
        self.ecg_files = glob(data_dir+"*.edf")
        self.bcg_files.sort()
        self.ecg_files.sort()
        self.have_ecg = have_ecg
    
    def generate_data(self):
        pass

    def __call__(self, seqlen=60000):
        # set debug seqlen large to 10min = 1000*60*10
        for bcg_file, ecg_file in zip(self.bcg_files, self.ecg_files):
            bcg = load_bcg(bcg_file)
            ecg = load_ecg(ecg_file) if self.have_ecg else bcg
            num_samples = min(len(bcg), len(ecg))
            for index in range(0, num_samples-seqlen+1, seqlen):
                bcg_example = bcg[index:index+seqlen]
                ecg_example = ecg[index:index+seqlen]
                yield bcg_example, ecg_example

def distribution(signal, whitening=False):
    x = signal - np.mean(signal)
    x = x / np.std(signal)
    min = np.min(x)
    max = np.max(x)
    counter = Counter()
    for val in x:
        counter[x] += 1
    #TODO
    return 
        
        
                
def main(args):
    del args
    dataset = Dataset()
    for bcg, ecg in dataset():
        print(len(bcg), len(ecg))
        plt.plot(whiten(bcg))
        plt.show()
        break
        
if __name__ == "__main__":
    app.run(main)


