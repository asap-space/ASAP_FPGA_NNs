.PHONY: all 

all: onnx2c/build/onnx2c

onnx2c/build/onnx2c:
	cd onnx2c && mkdir -p build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make onnx2c
