# Makefile for Vitis AI workflow

# Default neural network if not specified
NN ?= VAENet

# Paths
FINN_DIR ?= finn
NOTEBOOK_SRC := $(NN)/Gen_FINN.ipynb
NOTEBOOK_DEST_DIR := finn/notebooks/work_dir/$(NN)
COMMON_DIR := ../Common/$(NN)

.PHONY: run clean

# Main target
run: copy_notebook run_docker

# Copy the notebook file to Vitis-AI directory
copy_notebook:
	@echo "Copying $(NOTEBOOK_SRC) to $(NOTEBOOK_DEST_DIR)..."
	@if [ ! -f $(NOTEBOOK_SRC) ]; then \
		echo "Error: $(NOTEBOOK_SRC) does not exist"; \
		exit 1; \
	fi
	@mkdir -p $(NOTEBOOK_DEST_DIR)
	@cp $(NOTEBOOK_SRC) $(NOTEBOOK_DEST_DIR)
	@echo "Copying $(COMMON_DIR) data to $(NOTEBOOK_DEST_DIR)..."
	@if [ "$(NN)" = "VAENet" ]; then \
		cp $(COMMON_DIR)/pre_trained_w* $(NOTEBOOK_DEST_DIR); \
		cp -r $(COMMON_DIR)/dataset $(NOTEBOOK_DEST_DIR); \
	fi
	@if [ "$(NN)" = "CNet" ]; then \
		cp $(COMMON_DIR)/pre_trained_w.pt $(NOTEBOOK_DEST_DIR); \
	fi
	@echo "Copy complete."

# Run the docker container
run_docker:
	@echo "Running Vitis-AI in Docker..."
	@cd $(FINN_DIR) && ./run-docker.sh notebook
	@cp -r $(NOTEBOOK_DEST_DIR)/output_final/deploy $(NN)

# Clean up
clean:
	@echo "Cleaning up..."
	@rm -rf $(NOTEBOOK_DEST_DIR)
	@rm -rf $(NN)/deploy

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