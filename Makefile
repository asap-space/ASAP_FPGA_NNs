NN := Logistic

.PHONY: all convert_model build_model clean ensure_dirs

all: ensure_dirs build_model

ensure_dirs:
	mkdir -p ONNX_model C_model

convert_model:
	python3 NetGen.py $(NN)

build_model: convert_model
	onnx2c/build/onnx2c ONNX_model/$(NN)Net.onnx >> C_model/$(NN)Net.c

clean:
	rm -f ONNX_model/$(NN).onnx C_model/$(NN).c
