# Copyright (C) 2021 Xilinx, Inc
#
# SPDX-License-Identifier: BSD-3-Clause

open_project ESPERTA_hls
set_top entry
add_files ESPERTA_hls.c
add_files -tb ESPERTA_hls_test.cpp
open_solution "solution1"
set_part {xczu7ev-ffvc1156-2-e}
create_clock -period 5 -name default
csynth_design
export_design -format ip_catalog -description "ESPERTA accelerator" -display_name "ESPERTA"
exit
