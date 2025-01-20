NN := Logistic
SEED := 84
PRETRAIMED_WEIGHTS := --pretrained_weights ../PreTrained_Weights/$(NN)_$(SEED).pth

.PHONY: all convert_model build_model clean ensure_dirs

all: ensure_dirs build_model

onnx2c/build/onnx2c:
	cd onnx2c && mkdir -p build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make onnx2c

ensure_dirs:
	mkdir -p ONNX_model C_model

convert_model:
	python3 NetGen.py $(PRETRAIMED_WEIGHTS) $(NN)

build_model: convert_model onnx2c/build/onnx2c
	onnx2c/build/onnx2c ONNX_model/$(NN)Net.onnx > C_model/$(NN)Net.c

clean:
	rm -f ONNX_model/$(NN).onnx C_model/$(NN).c
