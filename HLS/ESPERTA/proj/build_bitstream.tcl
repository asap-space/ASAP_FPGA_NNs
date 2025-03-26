# Copyright (C) 2022 Xilinx, Inc
# SPDX-License-Identifier: BSD-3-Clause
# Edited by Pedro Antunes
if {$argc < 1} {
    puts "Error: Project name not provided as an argument"
    puts "Usage: vitis_hls -f script.tcl -tclargs <project_name>"
    exit 1
}

# Get the project name from the arguments
set overlay_name [lindex $argv 0]

# open block design
open_project ./${overlay_name}/${overlay_name}.xpr
open_bd_design ./${overlay_name}/${overlay_name}.srcs/sources_1/bd/${overlay_name}/${overlay_name}.bd

# Add top wrapper and xdc files
make_wrapper -files [get_files ./${overlay_name}/${overlay_name}.srcs/sources_1/bd/${overlay_name}/${overlay_name}.bd] -top
add_files -norecurse ./${overlay_name}/${overlay_name}.srcs/sources_1/bd/${overlay_name}/hdl/${overlay_name}_wrapper.v
set_property top ${overlay_name}_wrapper [current_fileset]
update_compile_order -fileset sources_1

# set platform properties
set_property platform.default_output_type "sd_card" [current_project]
set_property platform.design_intent.embedded "true" [current_project]
set_property platform.design_intent.server_managed "false" [current_project]
set_property platform.design_intent.external_host "false" [current_project]
set_property platform.design_intent.datacenter "false" [current_project]

# call implement
launch_runs impl_1 -to_step write_bitstream -jobs 4
wait_on_run impl_1

# generate xsa
write_hw_platform -fixed -include_bit -force -file ./${overlay_name}/${overlay_name}_wrapper.xsa
validate_hw_platform ./${overlay_name}/${overlay_name}_wrapper.xsa

# move and rename bitstream to final location
if {[file exists ./${overlay_name}/${overlay_name}.runs/impl_1/design_1_wrapper.bit]} {
    file copy -force ./${overlay_name}/${overlay_name}.runs/impl_1/${overlay_name}_wrapper.bit ${overlay_name}.bit
    file copy -force ./${overlay_name}/${overlay_name}.gen/sources_1/bd/${overlay_name}/hw_handoff/${overlay_name}.hwh ${overlay_name}.hwh
    puts "Bitstream and HWH files copied to current directory"
} else {
    puts "Bitstream generation failed"
}