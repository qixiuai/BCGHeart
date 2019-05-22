
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

from absl import app
from collections import Counter

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