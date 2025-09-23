import torch
import torch.nn as nn
import sys
import hls4ml

COMMON_PATH = "../../Common/CNet"
sys.path.append(COMMON_PATH)
try:
	from CNetPlusScalar import CNetPlusScalar
except ModuleNotFoundError as e:
	print(f"Error: Could not import MMSNet modules. Check COMMON_PATH: {COMMON_PATH}")
	raise e

def main():
    model = CNetPlusScalar()
    model.load_state_dict(torch.load(f'{COMMON_PATH}/pre_trained_w.pt', weights_only=True))

    config = hls4ml.utils.config_from_pytorch_model(
        model, 
        input_shape=[(1, 512, 512), (1,1)],
        granularity='model', 
        backend='Vitis',
        )
    print("-----------------------------------")
    print("Configuration")
    print(config)
    print("-----------------------------------")
    hls_model = hls4ml.converters.convert_from_pytorch_model(
        model, hls_config=config,
        backend='Vitis',
        output_dir='model_1/hls4ml_prj',
        part='xcu250-figd2104-2L-e',
    )

    hls_model.compile()
    hls_model.build(csim=False)
	
if __name__ == '__main__':
	main()
