
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app


class Metrics(object):

    def __init__(self):
        pass


def conv1d(template, signal):
    if len(template) == len(signal):
        return np.dot(template, signal)
    raise ValueError("input size should be equal")

def l2norm(vec):
    return np.sqrt(np.dot(vec, vec))


def best_templates(signal, template_length):
    scores = []
    # start_index, norm value
    # (template, score)
    num_samples = len(signal)
    for index in range(0, num_samples-template_length, template_length):
        vec = signal[index:index+template_length]
        s = l2norm(vec)
        scores.append((vec, s))
    scores.sort(by=lambda p : p[1])
    return scores


class Template(object):

    def __init__(self, signal, template_max_length=2000):
        pass

    @property
    def best_template_fixed_length(self, template_length=2000):
        pass

    @property
    def best_templates(self):
        pass

    @property
    def best_template(self):
        pass

    def predict(self, signal):
        pass


    

def main(args):
    del args

    
if __name__ == '__main__':
    app.run(main)

