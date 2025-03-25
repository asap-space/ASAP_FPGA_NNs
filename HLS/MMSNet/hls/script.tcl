# Copyright (C) 2021 Xilinx, Inc
#
# SPDX-License-Identifier: BSD-3-Clause
set NN_name "BaselineNet"

open_project ${NN_name}_hls
set_top entry
add_files ${NN_name}_hls.c
add_files -tb ${NN_name}_hls_test.cpp
open_solution "solution1"
#set_property board_part xilinx.com:zcu104:part0:1.1 [current_project]
set_part {xczu7ev-ffvc1156-2-e}
create_clock -period 5 -name default
csynth_design
export_design -format ip_catalog -description "${NN_name} accelerator" -display_name "${NN_name}"
exit
