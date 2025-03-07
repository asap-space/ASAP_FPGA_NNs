# Copyright (C) 2021 Xilinx, Inc
#
# SPDX-License-Identifier: BSD-3-Clause

open_project vaemodel1_hls
set_top entry
add_files vaemodel1_hls.cpp
add_files -tb vaemodel1_hls_test.cpp
open_solution "solution1"
set_part {xczu7ev-ffvc1156-2-i}
create_clock -period 5 -name default
config_interface -m_axi_alignment_byte_size 64 -m_axi_latency 64 -m_axi_max_widen_bitwidth 512
csynth_design
export_design -format ip_catalog -description "Ekaterina VAE encoder accelerator" -display_name "VAENet (encoder accelerator)"
exit
