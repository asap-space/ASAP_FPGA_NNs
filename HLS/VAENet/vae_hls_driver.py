import numpy as np
import os
import time
from pynq import Overlay, allocate

class VAEOverlay(Overlay):
    def __init__(self, bitfile_name):
        super().__init__(bitfile_name)
        print("VAE Overlay loaded")
        self.vae_out_shape = (1, 12)
        # Load the weights file
        weights_path_Conv_71 = os.path.join(os.path.dirname(__file__), "weights_Conv_71.npy")
        weights_Conv_71 = np.load(weights_path_Conv_71)
        weights_path_Conv_74 = os.path.join(os.path.dirname(__file__), "weights_Conv_74.npy")
        weights_Conv_74 = np.load(weights_path_Conv_74)
        # Allocate memory for weights
        weights_buffer_Conv_71 = allocate(shape=weights_Conv_71.shape, dtype=np.float32)
        weights_buffer_Conv_74 = allocate(shape=weights_Conv_74.shape, dtype=np.float32)
        # Copy weights to the allocated buffer
        np.copyto(weights_buffer_Conv_71, weights_Conv_71)
        np.copyto(weights_buffer_Conv_74, weights_Conv_74)

    def run(self, input_data):
        # Allocate memory for input and output
        in_buffer = allocate(shape=(input_data.shape), dtype=np.float32)
        out_buffer = allocate(self.vae_out_shape, dtype=np.float32)
        # Copy input data to in_buffer
        np.copyto(in_buffer, input_data)
        # Run the accelerator
        start = time.time()
        self.entry_0.register_map.CTRL.AP_START=1
        while not self.entry_0.register_map.CTRL.AP_DONE:
            pass
        print(time.time()-start)
        # Copy output data to output_data
        output_data = np.copy(out_buffer)
        return output_data