import sys, os
import torch
import torch.nn as nn
import torch.optim as optim
from spacepy import pycdf
import numpy as np

from vae_model_ext1 import vaemodel1

def test(net):
    # TO DO
    return


def load_pretrained_weights(net, weight_file):
    if not os.path.exists(weight_file):
        raise FileNotFoundError(f"Weight file not found: {weight_file}")

    try:
        net.load_state_dict(
            torch.load(weight_file, weights_only=True, map_location=torch.device("cpu"))
        )
    except RuntimeError as e:
        raise RuntimeError(f"Error loading weights: {e}")


def export_ONNX(model):
    tensor_x = torch.rand((1, 3, 128, 256), dtype=torch.float32)
    os.makedirs("ONNX_model", exist_ok=True)
    torch.onnx.export(
        model,
        (tensor_x,),
        f"ONNX_model/{model.__class__.__name__}.onnx",  # filename of the ONNX model
        input_names=["input"],  # Rename inputs for the ONNX model
        dynamo=False,  # True or False to select the exporter to use
    )


def usage(possible_NN):
    print(
        f"Usage: python NetGen.py (optional: --pretrained_weights <weight_file>) <model_name>"
    )
    print(f"Available models: {', '.join(possible_NN)}")


def main():
    # Dynamically select and call the appropriate network function/class
    net = vaemodel1()

    if "--pretrained_weights" in sys.argv:
        weight_file = sys.argv[sys.argv.index("--pretrained_weights") + 1]
        print(f"Using pre-trained weights from: {weight_file}")
        load_pretrained_weights(net, weight_file)

    if "--seed" in sys.argv:
        seed = int(sys.argv[sys.argv.index("--seed") + 1])
        # Setting seeds for reproducibility
        torch.manual_seed(seed)

    print(net)
    params = list(net.parameters())
    print(sum([p.numel() for p in params]))
    # print(params)
    # Create directory if it does not exist
    os.makedirs("PreTrained_Weights", exist_ok=True)
    torch.save(
        net.state_dict(), f"PreTrained_Weights/{net.__class__.__name__}.pth"
    )
    export_ONNX(net)
    test(net)
    exit()


if __name__ == "__main__":
    main()
