
import os
import sys
import pdb
import time
import numpy as np
import requests
import json

sys.path.append("/home/guo/BCGHeart/clinical/bcg")

from absl import app
from bcg import load_bcg
from fs import load_ecg
import plotly.graph_objs as go
from plotly.offline import plot
from glob import glob
import autopeaks

def find_bcg_peaks(signal):
    data = json.dumps({"signal": ",".join(map(str, signal)), "is_reset":"true", "is_signal_end":"true"})
    headers = {"content-type": "application/json"}
    json_response = requests.post('http://127.0.0.1:8002', data=data, headers=headers)
    text = json_response.text
    result = json.loads(text)
    intervals = result['intervals'].split(',')
    intervals = np.asarray(list(map(float, intervals)))
    plot(go.Figure(data=[go.Scatter(y=60000/intervals, mode="lines+markers")],
                   layout=go.Layout(yaxis=dict(range=[30,110]))))
    return intervals

def find_ecg_peaks(signal):
    auto_peaks = autopeaks.AutoPeaks(thres=0.7, min_dist=250, buffer_size=2*500)
    list(map(auto_peaks.findpeaks, signal))
    peak_indices, peak_values = auto_peaks.peak_indexes, auto_peaks.peak_values
    return peak_indices

def test_findpeaks(bcg_signal, ecg_signal):
    pass


def compare_by_plot(bcg, bcg_peak_indices, bcg_peak_values,
                    ecg, ecg_peak_indices, ecg_peak_values):
    data = [ go.Scatter(y=np.diff(bcg_peak_indices), mode="lines+markers"),
             go.Scatter(y=np.diff(ecg_peak_indices), mode="lines+markers")
    ]
    layout = go.Layout(yaxis=dict(range=[30,1000]))
    plot(go.Figure(data=data,layout=layout))


def main(unused_args):
    del unused_args
    data_dir = "/home/guo/physio/BCG_data/bcg_ecg_data/bcg_ecg_data(500HZ)/"
    bcg_files = glob(data_dir+"*.txt", recursive=False)
    ecg_files = glob(data_dir+"*.edf", recursive=False)
    bcg_files.sort()
    ecg_files.sort()

    for bcg_file,ecg_file in zip(bcg_files, ecg_files):
        #bcg_file = "/home/guo/physio/BCG_data/bcg_ecg_data/bcg_ecg_data(500HZ)/hwm_bcg_wave(500HZ)(03-15 200629).txt"
        #ecg_file = "/home/guo/physio/BCG_data/bcg_ecg_data/bcg_ecg_data(500HZ)/hwm_ecg.edf"
        print(bcg_file, ecg_file)
        bcg = load_bcg(bcg_file, filter=False, notch=False)
        #bcg = bcg[9*500*60:(9+8)*500*60]
        #plot([go.Scatter(y=bcg)])
        time.sleep(1)
        bcg_peak_indices = find_bcg_peaks(bcg)
        ecg = load_ecg(ecg_file, filter=False)
        ecg_peak_indices = find_ecg_peaks(ecg)
        #compare_by_plot(bcg, bcg_peak_indices, bcg_peak_values,
        #                ecg, ecg_peak_indices, ecg_peak_values)
        #time.sleep(1)
        #plot([go.Scatter(y=30000/np.diff(ecg_peak_indices), mode="lines+markers")])

    return


def test(unused_args):
    path = "/home/guo/gitlab/statedata.txt"
    signal = np.loadtxt(path, delimiter=',')
    signal = np.asarray(signal, dtype=np.int)
    intervals = find_bcg_peaks(signal)
    print(len(intervals))
    print(np.sum(intervals))
    
if __name__ == '__main__':
    app.run(test)

