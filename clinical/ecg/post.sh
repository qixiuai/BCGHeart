#!/bin/bash

#HOST=http://localhost:800
HOST=http://127.0.0.1:8001
#HOST=http://192.168.17.129:8000
# put edfdata
#
#curl -X PUT -H "Content-Type: application/octet-stream"  -T "/home/guo/data/psg/physio/psg_test.edf"  ${HOST}

#exit 0

#HEX="d6323050b6d948ea685181f587b53e8671cd8b33d3772277afb957e41097f98b"
#HEX="c13d716138b77a78f42ca91b778a73857b41ea9b2d9d6cd7d612c559ea18592f"
# post events
#curl -X POST -H "Content-Type: application/json" -d '{"d6323050b6d948ea685181f587b53e8671cd8b33d3772277afb957e41097f98b/Events/Stage/":"1,2,0,1\n"}' ${HOST}/${HEX}/Events/Stage/

curl -X POST -H "Content-Type: application/json" -d '{"signal":"1,2,3,3,4,5,6,7,8,9,10"}' ${HOST}/


