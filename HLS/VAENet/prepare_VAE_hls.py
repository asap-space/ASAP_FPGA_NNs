'''
This script performs exactly the same operations as your notebook cell, but in a standard Python script format with a main function. You can run it from the command line with `python extract_onnx_weights.py`.
'''
import onnx
import numpy as np
import torch
import torch.nn as nn
import os
import subprocess


class vaemodel1(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 16, 3, stride=2, padding=1),  # Increased channels, stride 2
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.Conv2d(16, 32, 3, stride=2, padding=1),  # Increased channels, stride 2
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 64, 3, stride=2, padding=1),  # Increased channels, stride 2
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 128, 3, stride=2, padding=1),  # Increased channels, stride 2
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 256, 3, stride=2, padding=1),  # Increased channels, stride 2
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1)),
        )
        self.mu = nn.Linear(256, 6)  # Reduced latent space size
        self.std = nn.Linear(256, 6)  # Reduced latent space size


    def forward(self, x):
        a = self.encoder(x).permute(0,2,3,1)
        a = torch.flatten(a, start_dim=1)
        mu = self.mu(a)
        lvar = self.std(a)
        out = torch.cat((mu, lvar), dim=1)
        return out


def save_onnx_model(onnx_model_name):
    model = vaemodel1()
    common_dir = "../../Common/VAENet"
    model.load_state_dict(torch.load(f"{common_dir}/pre_trained_w_encoder.pt", weights_only=True))
    tensor_x = torch.rand((1, 3, 128, 256), dtype=torch.float32)
    torch.onnx.export(
        model,
        (tensor_x,),
        onnx_model_name,  # filename of the ONNX model
        input_names=["input"],  # Rename inputs for the ONNX model
        output_names=["output"],  # Rename outputs for the ONNX model
        dynamo=False,  # True or False to select the exporter to use
    )


def save_C_model(onnx_model_name):
    """
    Convert ONNX model to C code using onnx2c
    """
    output_dir = "C"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get absolute path to onnx2c executable
    onnx2c_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "onnx2c", "build", "onnx2c"))
    cmd = [onnx2c_path, onnx_model_name]
    
    with open(f"{output_dir}/vaemodel1.c", "w") as f:
        subprocess.run(cmd, stdout=f, check=True)
    
    print(f"C model saved to {output_dir}/vaemodel1.c")


def save_weights_to_npy(onnx_model_name):
    # Load the ONNX model
    onnx_model = onnx.load(onnx_model_name)

    # Dictionary to store tensors
    weight_dict = {}

    # Extract all initializers (weights and biases)
    for initializer in onnx_model.graph.initializer:
        weight_dict[initializer.name] = onnx.numpy_helper.to_array(initializer)

    print(weight_dict.keys())
    
    # Extract and save the specific tensors
    if "onnx::Conv_71" in weight_dict:
        np.save("weights_Conv_71.npy", weight_dict["onnx::Conv_71"])
        print(f"Saved weights_Conv_71 with shape {weight_dict['onnx::Conv_71'].shape}")

    if "onnx::Conv_74" in weight_dict:
        np.save("weights_Conv_74.npy", weight_dict["onnx::Conv_74"])
        print(f"Saved weights_Conv_74 with shape {weight_dict['onnx::Conv_74'].shape}")


def main():
    onnx_model_name = "vaemodel1.onnx"
    save_onnx_model(onnx_model_name)
    save_C_model(onnx_model_name)
    save_weights_to_npy(onnx_model_name)

if __name__ == "__main__":
    main()
