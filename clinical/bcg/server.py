
from flask import Flask, request
from flask_restful import Api, Resource, reqparse

import requests

import pdb

from bcgpeaks import BCGPeaks

app = Flask(__name__)
api = Api(app)

bcgpeaks = BCGPeaks()

class BCGPeaksRest(Resource):

    def post(self):
        signal = request.json['signal']
        is_reset = request.json['is_reset']
        is_signal_end = request.json['is_signal_end']
        if is_reset == 'true':
            bcgpeaks.reset()
        if is_signal_end == 'true':
            bcgpeaks.set_signal_end()
        if type(signal) is str:
            signal = list(map(int, signal.split(',')))
        list(map(bcgpeaks.findpeaks, signal))
        intervals = bcgpeaks.intervals
        intervals = ",".join(list(map(str, intervals)))
        return {"interals": intervals}

    def get(self):
        return "get demo for test usage"

api.add_resource(BCGPeaksRest, "/")


if __name__ == '__main__':
    app.run('127.0.0.1', port=8002)
