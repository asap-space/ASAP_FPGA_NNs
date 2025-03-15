# Makefile for generating a deploy_ZCU104 directory and zipping it

# Define the source directories
COMMON_DIR = ../Common
VitisAI_DIR = ../VitisAI
HLS_DIR = ../HLS
FINN_DIR = ../FINN
DPU_PYNQ_DIR = DPU-PYNQ/boards/zcu104

# Define the deploy directory
DEPLOY_DIR = deploy_ZCU104
# Define the NN directories
VAENET_DEPLOY_DIR = $(deploy_ZCU104)/VAENet
ESPERTA_DEPLOY_DIR = $(deploy_ZCU104)/ESPERTA

# Define the zip file name
ZIP_FILE = deploy_ZCU104.zip

# Default target
all: deploy zip

# 
VAENet:
	@echo "Preparing VAENet files..."
	@mkdir -p $(VAENET_DEPLOY_DIR)/VAENet
	@echo "Preparing HLS files..."
	cp $(HLS_DIR)/VAENet/design_1.hwh $(VAENET_DEPLOY_DIR)/hls_bitstream/
	cp $(HLS_DIR)/VAENet/design_1_wrapper.bit $(VAENET_DEPLOY_DIR)/hls_bitstream/
	cp $(HLS_DIR)/VAENet/vae_hls_driver.py $(VAENET_DEPLOY_DIR)/
	cp $(HLS_DIR)/VAENet/weights_Conv_71.npy $(VAENET_DEPLOY_DIR)/
	cp $(HLS_DIR)/VAENet/weights_Conv_74.npy $(VAENET_DEPLOY_DIR)/
	@echo "Preparing Vitis AI files..."
	cp $(VitisAI_DIR)/zcu104_vaemodel1.xmodel $(VAENET_DEPLOY_DIR)/
	@echo "Preparing FINN files..."
	cp $(FINN_DIR)/deploy/bitfile/* $(VAENET_DEPLOY_DIR)/finn_bitstream/
	cp $(FINN_DIR)/deploy/driver/driver_base.py $(VAENET_DEPLOY_DIR)/finn_driver.py
	cp -r $(FINN_DIR)/deploy/driver/finn $(VAENET_DEPLOY_DIR)/
	cp -r $(FINN_DIR)/deploy/driver/qonnx $(VAENET_DEPLOY_DIR)/
	@echo "Creating deploy directory for VAENet..."
	cp -r VAENet/* $(VAENET_DEPLOY_DIR)/
	cp $(COMMON_DIR)/pre_trained_w* $(VAENET_DEPLOY_DIR)/
	mkdir -p $(VAENET_DEPLOY_DIR)/dataset/vae45_Br_imgs/
	find $(COMMON_DIR)/dataset/vae45_Br_imgs/ -type f | shuf -n 1000 | xargs -I{} cp {} $(VAENET_DEPLOY_DIR)/dataset/vae45_Br_imgs/

# 
ESPERTA:
	@echo "Preparing ESPERTA files..."

# Create deploy target to use the new targets
deploy: VAENet ESPERTA
	@echo "Creating deploy directory..."
	@mkdir -p $(DEPLOY_DIR)/vitisai_bitstream
	cp $(DPU_PYNQ_DIR)/dpu.bit $(DEPLOY_DIR)/vitisai_bitstream
	cp $(DPU_PYNQ_DIR)/dpu.hwh $(DEPLOY_DIR)/vitisai_bitstream
	cp $(DPU_PYNQ_DIR)/dpu.xclbin $(DEPLOY_DIR)/vitisai_bitstream

# Zip the deploy directory
zip: deploy
	@echo "Zipping the deploy directory..."
	@zip -r $(ZIP_FILE) $(DEPLOY_DIR)

# Clean the deploy directory and zip file
clean:
	@echo "Cleaning up..."
	@rm -rf $(DEPLOY_DIR) $(ZIP_FILE)

.PHONY: all deploy zip clean hls vitisai finn