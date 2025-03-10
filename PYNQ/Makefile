# Makefile for generating a deploy_ZCU104 directory and zipping it

# Define the neural network variable (default to VAENet)
NN ?= VAENet

# Define the source directories
COMMON_DIR = ../Common/$(NN)
VitisAI_DIR = ../VitisAI/$(NN)

# Define the deploy directory
DEPLOY_DIR = deploy_ZCU104

# Define the zip file name
ZIP_FILE = deploy_$(NN)_ZCU104.zip

# Default target
all: deploy zip

# Create the deploy directory and copy the contents based on the NN variable
deploy:
	@echo "Creating deploy directory and copying contents of $(NN)..."
	@mkdir -p $(DEPLOY_DIR)
	@if [ "$(NN)" = "VAENet" ]; then \
		cp -r $(NN)/* $(DEPLOY_DIR)/; \
		cp $(COMMON_DIR)/pre_trained_w* $(DEPLOY_DIR)/; \
		cp -r $(COMMON_DIR)/dataset $(DEPLOY_DIR)/; \
		cp $(VitisAI_DIR)/V2_5/zcu104_vaemodel1.xmodel $(DEPLOY_DIR)/; \
	elif [ "$(NN)" = "CNet" ]; then \
		cp -r $(NN)/* $(DEPLOY_DIR)/; \
	elif [ "$(NN)" = "MMSNet" ]; then \
		cp -r $(NN)/* $(DEPLOY_DIR)/; \
	else \
		echo "Unknown NN value: $(NN)"; \
		exit 1; \
	fi

# Zip the deploy directory
zip: deploy
	@echo "Zipping the deploy directory..."
	@zip -r $(ZIP_FILE) $(DEPLOY_DIR)

# Clean the deploy directory and zip file
clean:
	@echo "Cleaning up..."
	@rm -rf $(DEPLOY_DIR) $(ZIP_FILE)

.PHONY: all deploy zip clean