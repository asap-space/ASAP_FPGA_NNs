# Makefile for generating a deploy_ZCU104 directory and zipping it

# Define the source directories
COMMON_DIR = ../Common/$@
VitisAI_DIR = ../VitisAI/$@
HLS_DIR = ../HLS/$@
FINN_DIR = ../FINN/$@
DPU_PYNQ_DIR := DPU-PYNQ/boards/zcu104

# Define the deploy directory
BASE_DEPLOY_DIR := deploy_ZCU104
DEPLOY_DIR = $(BASE_DEPLOY_DIR)/$@

# Define the zip file name
ZIP_FILE := deploy_ZCU104.zip

# Default target
all: zip

# 
VAENet:
	@echo "Preparing $@ files..."
	@mkdir -p $(DEPLOY_DIR)
	cp -r $@/* $(DEPLOY_DIR)/
	cp $(COMMON_DIR)/pre_trained_w* $(DEPLOY_DIR)/
	mkdir -p $(DEPLOY_DIR)/dataset/vae45_Br_imgs/
	find $(COMMON_DIR)/dataset/vae45_Br_imgs/ -type f | shuf -n 1000 | xargs -I{} cp {} $(DEPLOY_DIR)/dataset/vae45_Br_imgs/
	@echo "Preparing HLS files... WIP"
	@mkdir -p $(DEPLOY_DIR)/hls_bitstream
	cp $(HLS_DIR)/design_1.hwh $(DEPLOY_DIR)/hls_bitstream
	cp $(HLS_DIR)/design_1_wrapper.bit $(DEPLOY_DIR)/hls_bitstream
	cp $(HLS_DIR)/vae_hls_driver.py $(DEPLOY_DIR)
	cp $(HLS_DIR)/weights_Conv_71.npy $(DEPLOY_DIR)
	cp $(HLS_DIR)/weights_Conv_74.npy $(DEPLOY_DIR)
	@echo "Preparing Vitis AI files..."
	cp $(VitisAI_DIR)/zcu104_vaemodel1.xmodel $(DEPLOY_DIR)
	@echo "Preparing FINN files... NOT SUPPORTED"

# 
ESPERTA:
	@echo "Preparing $@ files..."
	@mkdir -p $(DEPLOY_DIR)
	cp -r $@/* $(DEPLOY_DIR)/
	cp $(COMMON_DIR)/espertaTorch.py $(DEPLOY_DIR)/
	@echo "Preparing HLS files..."
	@mkdir -p $(DEPLOY_DIR)/hls_bitstream
	cp $(HLS_DIR)/$@.hwh $(DEPLOY_DIR)/hls_bitstream/
	cp $(HLS_DIR)/$@.bit $(DEPLOY_DIR)/hls_bitstream/
	@echo "Preparing Vitis AI files... NOT SUPPORTED"
	@echo "Preparing FINN files... NOT SUPPORTED"

# 
CNet:
	@echo "Preparing $@ files..."
	@mkdir -p $(DEPLOY_DIR)
	cp -r $@/* $(DEPLOY_DIR)/
	cp $(COMMON_DIR)/CNetPlusScalar.py $(DEPLOY_DIR)/
	cp $(COMMON_DIR)/pre_trained_w.pt $(DEPLOY_DIR)/
	@echo "Preparing Vitis AI files..."
	cp $(VitisAI_DIR)/zcu104_CNetPlusScalar.xmodel $(DEPLOY_DIR)
	@echo "Preparing HLS files... NOT SUPPORTED"
	@echo "Preparing Vitis AI files... NOT SUPPORTED"
	@echo "Preparing FINN files... NOT SUPPORTED"

# Create deploy target to use the new targets
deploy: VAENet ESPERTA CNet
	@echo "Creating deploy directory..."
	@mkdir -p $(BASE_DEPLOY_DIR)/vitisai_bitstream
	cp $(DPU_PYNQ_DIR)/dpu.bit $(BASE_DEPLOY_DIR)/vitisai_bitstream
	cp $(DPU_PYNQ_DIR)/dpu.hwh $(BASE_DEPLOY_DIR)/vitisai_bitstream
	cp $(DPU_PYNQ_DIR)/dpu.xclbin $(BASE_DEPLOY_DIR)/vitisai_bitstream

# Zip the deploy directory
zip: deploy
	@echo "Zipping the deploy directory..."
	@zip -r $(ZIP_FILE) $(BASE_DEPLOY_DIR)

# Clean the deploy directory and zip file
clean:
	@echo "Cleaning up..."
	@rm -rf $(BASE_DEPLOY_DIR) $(ZIP_FILE)

.PHONY: all deploy zip clean ESPERTA VAENet CNet