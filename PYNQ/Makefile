# Makefile for generating a deploy_ZCU104 directory and zipping it

# Define the neural network variable (default to VAENet)
NN ?= VAENet

# Define the source directories
COMMON_DIR = ../Common/$(NN)
VitisAI_DIR = ../VitisAI/$(NN)
HLS_DIR = ../HLS/$(NN)
FINN_DIR = ../FINN/$(NN)
DPU_PYNQ_DIR = DPU-PYNQ/boards/zcu104

# Define the deploy directory
DEPLOY_DIR = deploy_ZCU104

# Define the zip file name
ZIP_FILE = deploy_$(NN)_ZCU104.zip

# Default target
all: deploy zip

# HLS target to prepare HLS files
hls:
	@echo "Preparing HLS files for $(NN)..."
	@mkdir -p $(DEPLOY_DIR)/hls_bitstream
	@if [ "$(NN)" = "VAENet" ]; then \
		cp $(HLS_DIR)/design_1.hwh $(DEPLOY_DIR)/hls_bitstream/; \
		cp $(HLS_DIR)/design_1_wrapper.bit $(DEPLOY_DIR)/hls_bitstream/design_1.bit; \
		cp $(HLS_DIR)/vae_hls_driver.py $(DEPLOY_DIR)/; \
		cp $(HLS_DIR)/weights_Conv_71.npy $(DEPLOY_DIR)/; \
		cp $(HLS_DIR)/weights_Conv_74.npy $(DEPLOY_DIR)/; \
	fi

# VitisAI target to prepare Vitis AI files
vitisai:
	@echo "Preparing Vitis AI files for $(NN)..."
	@mkdir -p $(DEPLOY_DIR)/vitisai_bitstream
	@cp $(DPU_PYNQ_DIR)/dpu.bit $(DEPLOY_DIR)/vitisai_bitstream
	@cp $(DPU_PYNQ_DIR)/dpu.hwh $(DEPLOY_DIR)/vitisai_bitstream
	@cp $(DPU_PYNQ_DIR)/dpu.xclbin $(DEPLOY_DIR)/vitisai_bitstream
	@if [ "$(NN)" = "VAENet" ]; then \
		cp $(VitisAI_DIR)/zcu104_vaemodel1.xmodel $(DEPLOY_DIR)/; \
	fi

# FINN target to prepare FINN files
finn:
	@echo "Preparing FINN files for $(NN)..."
	@mkdir -p $(DEPLOY_DIR)/finn_bitstream
	@if [ "$(NN)" = "VAENet" ]; then \
		cp $(FINN_DIR)/deploy/bitfile/* $(DEPLOY_DIR)/finn_bitstream/; \
		cp $(FINN_DIR)/deploy/driver/driver_base.py $(DEPLOY_DIR)/finn_driver.py; \
		cp -r $(FINN_DIR)/deploy/driver/finn $(DEPLOY_DIR)/; \
		cp -r $(FINN_DIR)/deploy/driver/qonnx $(DEPLOY_DIR)/; \
	fi

# Create deploy target to use the new targets
deploy: hls vitisai finn
	@echo "Creating deploy directory for $(NN)..."
	@mkdir -p $(DEPLOY_DIR)
	@cp -r $(NN)/* $(DEPLOY_DIR)/
	@if [ "$(NN)" = "VAENet" ]; then \
		cp $(COMMON_DIR)/pre_trained_w* $(DEPLOY_DIR)/; \
		mkdir -p $(DEPLOY_DIR)/dataset/vae45_Br_imgs/; \
		find $(COMMON_DIR)/dataset/vae45_Br_imgs/ -type f | shuf -n 1000 | xargs -I{} cp {} $(DEPLOY_DIR)/dataset/vae45_Br_imgs/; \
	fi

# Zip the deploy directory
zip: deploy
	@echo "Zipping the deploy directory..."
	@zip -r $(ZIP_FILE) $(DEPLOY_DIR)

# Clean the deploy directory and zip file
clean:
	@echo "Cleaning up..."
	@rm -rf $(DEPLOY_DIR) $(ZIP_FILE)

.PHONY: all deploy zip clean hls vitisai finn