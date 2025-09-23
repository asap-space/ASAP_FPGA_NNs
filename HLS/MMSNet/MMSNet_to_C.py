import torch
import sys
import subprocess
import os

COMMON_PATH = "../../Common/MMSNet"
sys.path.append(COMMON_PATH)
try:
	from MMSNet import LogisticNet, ReducedNet, BaselineNet
except ModuleNotFoundError as e:
	print(f"Error: Could not import MMSNet modules. Check COMMON_PATH: {COMMON_PATH}")
	raise e


def save_C_model(model):
    """
    Convert ONNX model to C code using onnx2c
    """
    output_dir = "C"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get absolute path to onnx2c executable
    onnx2c_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "onnx2c", "build", "onnx2c"))
    cmd = [onnx2c_path, f"{model.__class__.__name__}.onnx"]
    
    output_file = f"{output_dir}/{model.__class__.__name__}.c"
    with open(output_file, "w") as f:
        subprocess.run(cmd, stdout=f, check=True)
    
    print(f"C model saved to {output_file}")


def main():
    model1 = LogisticNet()
    model2 = ReducedNet()
    model3 = BaselineNet()

    model1.load_state_dict(torch.load(f'{COMMON_PATH}/PreTrained_Weights/LogisticNet_84.pth', weights_only=True))
    model2.load_state_dict(torch.load(f'{COMMON_PATH}/PreTrained_Weights/ReducedNet_42.pth', weights_only=True))
    model3.load_state_dict(torch.load(f'{COMMON_PATH}/PreTrained_Weights/BaselineNet_336.pth', weights_only=True))

    tensor_x = torch.rand((1, 1, 32, 16, 32), dtype=torch.float32)
    for model in [model1, model2, model3]:
        torch.onnx.export(
            model,
            (tensor_x,),
            f"{model.__class__.__name__}.onnx",  # filename of the ONNX model
            input_names=["input"],  # Rename inputs for the ONNX model
            output_names=["output"],  # Rename outputs for the ONNX model
            dynamo=False,  # True or False to select the exporter to use
        )
        save_C_model(model)


if __name__ == "__main__":
    main()