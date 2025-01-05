NN := LogisticNet

all:
	python3 nn.py $(NN)
	onnx2c/build/onnx2c ONNX_model/$(NN).onnx >> C_model/$(NN).c
