
from flask import Flask, request
from flask_restful import Api, Resource, reqparse

import requests

import pdb

from bcgpeaks import BCGPeaks

app = Flask(__name__)
api = Api(app)

bcgpeaks = BCGPeaks(1000)
#bcgpeaks = BCGPeaks(500)

class BCGPeaksRest(Resource):

    def post(self):
        signal = request.json.get('signal', "")
        is_reset = request.json.get('is_reset', 'false')
        is_signal_end = request.json.get('is_signal_end', 'false')
        if is_reset == 'true':
            bcgpeaks.reset()
        if isinstance(signal, str) and signal:
            signal = list(map(int, signal.split(',')))
            list(map(bcgpeaks.findpeaks, signal))
        if is_signal_end == 'true':
            bcgpeaks.set_signal_end()
        intervals = bcgpeaks.intervals
        intervals = ",".join(list(map(str, intervals)))
        return {"intervals": intervals}

    def get(self):
        return "get demo for test usage"

api.add_resource(BCGPeaksRest, "/")


if __name__ == '__main__':
    #ip = '192.168.4.27'
    ip = '127.0.0.1'
    app.run(ip, port=8002)

