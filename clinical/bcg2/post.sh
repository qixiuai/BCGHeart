#!/bin/bash

#HOST=http://localhost:800
HOST=http://127.0.0.1:8002
#HOST=http://192.168.17.129:8000

# post events
#curl -X POST -H "Content-Type: application/json" -d '{"d6323050b6d948ea685181f587b53e8671cd8b33d3772277afb957e41097f98b/Events/Stage/":"1,2,0,1\n"}' ${HOST}/${HEX}/Events/Stage/

curl -X POST -H "Content-Type: application/json" -d '{"signal":"1,2,3,3,4,5,6,7,8,9,10,1,12,3,4,5,6,7,8"}' ${HOST}/

#curl -X POST -H "Content-Type: application/json" -d '{"is_reset":"true"}' ${HOST}/
#curl -X POST -H "Content-Type: application/json" -d '{"is_signal_end":"true"}' ${HOST}/

#'{"intervals": "1000"}'#
