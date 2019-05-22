

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np


def find_template(signal, rr):
    return signal[200:400]


def conv(signal, template):
    scores = []
    template_length = len(template)
    signal_length = len(signal)
    for ind in range(signal_length-template_length):
        score = np.dot(signal[ind:ind+template_length], template)
        score = np.sqrt(score / template_length) - 300
        scores.append(score)
    return scores


def findpeaks(signal):
    pass


if __name__ == "__main__":
    pass
