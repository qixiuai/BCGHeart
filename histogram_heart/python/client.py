
import requests
import pdb

import numpy as np

def main():
    data = np.loadtxt("raw_hr.txt", delimiter=",")
    url = "http://127.0.0.1:8001/"
    param = {"sn":"1"}
    for interval in data:
        param["interval"] = str(int(interval))
        response = requests.post(url, json=param)#, headers={"Content-Type": "application/json"})
        print(response.json()["interval"])


if __name__ == '__main__':
    main()

