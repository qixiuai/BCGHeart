
FLAGS = -fpic
PYTHONI = -I/home/guo/anaconda3/include/python3.6m/
PYTHONL = -Xlinker -export-dynamic

all:
	#g++ -fPic -c capi.cc -o capi.o
	swig -c++ -python -o capi_wrap.cxx capi.i
	g++ ${FLAGS} ${PYTHONI} -c capi_wrap.cxx -o capi_wrap.o
	g++ ${PYTHONL} ${LIBDLAGS} -shared capi.o capi_wrap.o -o _monitor.so -lstdc++




