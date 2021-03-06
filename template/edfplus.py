
from datetime import date, datetime

from absl import flags
from absl import app
from absl import logging

import pdb

FLAGS = flags.FLAGS
flags.DEFINE_string("edf_path", "/home/guo/PSG/data/A2-PSG_1811142338.edf", "edf path")

class Edfplus(object):
    """ Edfplus file """

    def __init__(self, raw):
        self._parse(raw)
        
    def _parse(self, raw):
        # parse signal names
        self._starttime = datetime.strptime(str(raw[168:168+16], 'ascii'), '%d.%m.%y%H.%M.%S')
        self._num_records = int(str(raw[236:236+8], 'ascii'))
        self._num_signals = int(str(raw[252:252+4], 'ascii'))
        self._signal_names = []
        names = str(raw[256:256+self._num_signals*16], 'ascii').split('  ')
        for name in names:
            name = name.strip()
            if len(name) > 0:
                self._signal_names.append(name)
        self._signal_freqs = []
        st = 256 + self._num_signals * 216
        freqs = str(raw[st : st + self._num_signals * 8], 'ascii').split(' ')
        for freq in freqs:
            freq = freq.strip()
            if len(freq) > 0:
                self._signal_freqs.append(int(freq))

        # parse signals
        start_idx = 256 + len(self.signal_names) * 256
        raw_signal = raw[start_idx:]
        self._parse_signals(raw_signal)

    def _parse_signals(self, raw_signal):
        self._signals = {}
        for name in self.signal_names:
            self.signals[name] = []
        record_size = sum(self._signal_freqs*2)
        nbytes = len(raw_signal)
        for i in range(0, nbytes, record_size):
            raw_record = raw_signal[i:i+record_size]
            self._parse_record(raw_record)

    def _parse_record(self, record):
        samples = []
        for i in range(0, len(record), 2):
            sample = int.from_bytes(record[i:i+2], byteorder="little", signed=True)
            samples.append(sample)
        start_idx = 0
        for signal, freq in zip(self.signal_names, self.signal_freqs):
            self._signals[signal].extend(samples[start_idx:start_idx+freq])
            start_idx += freq

    @property
    def starttime(self):
        return self._starttime
            
    @property
    def num_signals(self):
        return self._num_signals
        
    @property
    def signal_freqs(self):
        return self._signal_freqs

    @property
    def signal_names(self):
        return list(self._signal_names)
    
    @property
    def signals(self):
        return self._signals


def main(unused_arg):
    del unused_arg
    with open(FLAGS.edf_path, "rb") as file:
        raw = file.read()
    edfplus = Edfplus(raw)
    logging.info(edfplus.num_signals)
    logging.info(edfplus.signal_freqs)
    logging.info(edfplus.starttime)
    for signal in edfplus.signal_names:
        signal_size = len(edfplus.signals[signal])
        logging.info("loaded {} with size {}".format(signal, signal_size))

        
if __name__ == '__main__':
    app.run(main)
