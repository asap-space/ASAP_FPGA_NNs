# Copyright (C) 2022 Xilinx, Inc
# SPDX-License-Identifier: BSD-3-Clause
# Edited by Pedro Antunes

overlay_name := ESPERTA

all: hls_ip block_design bitstream check_timing
	@echo
	@tput setaf 2 ; echo "Built $(overlay_name) successfully!"; tput sgr0;
	@echo

hls_ip:
	vivado -notrace -mode batch -source build_ip.tcl -tclargs $(overlay_name)

block_design:
	vivado -notrace -mode batch -source build_design.tcl -tclargs $(overlay_name)

bitstream:
	vivado -notrace -mode batch -source build_bitstream.tcl -tclargs $(overlay_name)

check_timing:
	vivado -notrace -mode batch -source check_timing.tcl -tclargs $(overlay_name)

clean:
	rm -rf $(overlay_name) *.jou *.log NA .Xil ../hls/$(overlay_name)_hls ../hls/vitis_hls.log
