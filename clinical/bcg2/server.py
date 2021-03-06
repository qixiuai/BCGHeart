
from flask import Flask, request
from flask_restful import Api, Resource, reqparse

import requests
import sys
import pdb

from autopeaks2 import FindPeaksMaster

app = Flask(__name__)
api = Api(app)

#bcgpeaks = FindPeaksMaster(fs=1000)
bcgpeaks = FindPeaksMaster(fs=500)

class BCGPeaksRest(Resource):

    def post(self):
        signal = request.json.get('signal', '')
        is_reset = request.json.get('is_reset', 'false')
        error_code = ""
        global bcgpeaks
        try:
            if is_reset == 'true':
                bcgpeaks = FindPeaksMaster(fs=1000)
            if isinstance(signal, str) and signal:
                signal = list(map(float, signal.split(',')))
                list(map(bcgpeaks.findpeaks, signal))
            intervals = bcgpeaks.peak_intervals
            intervals = ",".join(list(map(str, intervals)))
        except:
            intervals = ""
            error_code = str(sys.exc_info()[0])
            print(error_code)
        return {"intervals": intervals, "error_msg": error_code}

    def get(self):
        return "get demo for test usage"

api.add_resource(BCGPeaksRest, "/")


if __name__ == '__main__':
    #ip = '192.168.4.27'
    ip = '127.0.0.1'
    app.run(ip, port=8002)

