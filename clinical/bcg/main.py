
import numpy as np
import pdb

from absl import app
from bcg import load_bcg
from bcgpeaks import BCGPeaks

import plotly.graph_objs as go
from plotly.offline import plot


def main(unused_args):
    del unused_args
    data_dir = "/home/guo/BCGHeart/data/bcg_ecg_data(500HZ)/"
    subject_file = "yjj_bcg_wave(500HZ)(03-15 145935).txt"
    signal = load_bcg(data_dir+subject_file, filter=False, notch=False)
    bcg_peaks = BCGPeaks(fs=500)
    for sample in signal:
        bcg_peaks.findpeaks(sample)
    bcg_peaks.set_signal_end()
    plot([go.Scatter(y=30000/np.asarray(bcg_peaks.intervals), mode="lines+markers")])
        
if __name__ == '__main__':
    app.run(main)
