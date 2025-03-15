# Create a new Vitis HLS project for the ESPERTA accelerator
set overlay_name "ESPERTA"

open_project ${overlay_name}_hls
set_top entry
add_files ${overlay_name}_hls.c
add_files -tb ${overlay_name}_hls_test.cpp
open_solution "solution1"
set_part {xczu7ev-ffvc1156-2-e}
create_clock -period 5 -name default
csynth_design
export_design -format ip_catalog -description "${overlay_name} accelerator" -display_name "${overlay_name}"
exit
