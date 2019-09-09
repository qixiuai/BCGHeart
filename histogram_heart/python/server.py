
from flask import Flask, request
from flask_restful import Api, Resource, reqparse

import requests

import pdb

from heart_rate_inference import HeartRateInference

app = Flask(__name__)
api = Api(app)


class HeartRateInferenceHub(object):

    def __init__(self):
        self.hub = {}

    def filter(self, id, interval):
        if id not in self.hub:
            self.hub[id] = HeartRateInference()
        interval = self.hub[id].inference(interval)
        return interval


class HeartInferenceServer(Resource):

    hub = HeartRateInferenceHub()

    def post(self):
        param = request.json
        id = param['sn']
        interval = param['interval']
        if isinstance(interval, str):
            interval = int(interval)
        interval = self.hub.filter(id, interval)
        interval = str(interval)
        param["interval"] = interval
        return param

    def get(self):
        return "get demo for test usage"

api.add_resource(HeartInferenceServer, "/")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Heart rate inference server.')
    parser.add_argument('--ip', type=str, default="127.0.0.1",
                        help='an integer for the accumulator')
    parser.add_argument('--port', type=int, default=8001,
                        help='sum the integers (default: find the max)')
    args = parser.parse_args()
    ip, port = args.ip, args.port
    app.run(ip, port=port)

