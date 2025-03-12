# Makefile for Vitis AI workflow

# Default neural network if not specified
NN ?= VAENet

# Paths
VITIS_AI_DIR ?= Vitis-AI
NOTEBOOK_SRC := $(NN)/Gen_ISA.ipynb
NOTEBOOK_DEST_DIR := $(VITIS_AI_DIR)/work_dir
NOTEBOOK_DEST := $(NOTEBOOK_DEST_DIR)/Gen_ISA.ipynb
COMMON_DIR := ../Common/$(NN)

.PHONY: run clean

# Main target
run: copy_notebook run_docker

# Copy the notebook file to Vitis-AI directory
copy_notebook:
	@echo "Copying $(NOTEBOOK_SRC) to $(VITIS_AI_DIR)..."
	@if [ ! -f $(NOTEBOOK_SRC) ]; then \
		echo "Error: $(NOTEBOOK_SRC) does not exist"; \
		exit 1; \
	fi
	@mkdir -p $(NOTEBOOK_DEST_DIR)
	@cp $(NOTEBOOK_SRC) $(NOTEBOOK_DEST)
	@echo "Copying $(COMMON_DIR) data to $(VITIS_AI_DIR)..."
	@if [ "$(NN)" = "VAENet" ]; then \
		cp $(COMMON_DIR)/pre_trained_w* $(NOTEBOOK_DEST_DIR)/; \
		mkdir -p $(NOTEBOOK_DEST_DIR)/dataset/vae45_Br_imgs/; \
		find $(COMMON_DIR)/dataset/vae45_Br_imgs/ -type f | shuf -n 1000 | xargs -I{} cp {} $(NOTEBOOK_DEST_DIR)/dataset/vae45_Br_imgs/; \
	fi
	@echo "Copy complete."

# Run the docker container
run_docker:
	@echo "Running Vitis-AI in Docker..."
	@cd $(VITIS_AI_DIR) && ./docker_run.sh xilinx/vitis-ai-cpu:2.5

# Clean up
clean:
	@echo "Cleaning up..."
	@rm -rf $(NOTEBOOK_DEST_DIR)

# Help
help:
	@echo "Usage:"
	@echo "  make [NN=<network_name>] [VITIS_AI_DIR=<path>] run    - Copy notebook and run docker"
	@echo "  make clean                                        - Remove copied notebook"
	@echo "  make help                                         - Show this help"
	@echo ""
	@echo "Default values:"
	@echo "  NN = $(NN)"
	@echo "  VITIS_AI_DIR = $(VITIS_AI_DIR)"