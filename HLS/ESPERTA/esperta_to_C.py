'''
This script performs exactly the same operations as your notebook cell, but in a standard Python script format with a main function. You can run it from the command line with `python extract_onnx_weights.py`.
'''
import os
import subprocess


def save_C_model():
    """
    Convert ONNX model to C code using onnx2c
    """
    output_dir = "C"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get absolute path to onnx2c executable
    onnx2c_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "onnx2c", "build", "onnx2c"))
    cmd = [onnx2c_path, '../../Common/ESPERTA/ESPERTA.onnx']
    
    output_file = f"{output_dir}/ESPERTA.c"
    with open(output_file, "w") as f:
        subprocess.run(cmd, stdout=f, check=True)
    
    print(f"C model saved to {output_file}")


def main():
    save_C_model()

if __name__ == "__main__":
    main()
