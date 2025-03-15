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

set fd [open ./${overlay_name}/${overlay_name}.runs/impl_1/${overlay_name}_wrapper_timing_summary_routed.rpt r]
set timing_met 0
while { [gets $fd line] >= 0 } {
    if [string match {All user specified timing constraints are met.} $line]  { 
        set timing_met 1
        break
    }
}
if {$timing_met == 0} {
    puts "ERROR: ${overlay_name} bitstream generation does not meet timing."
    exit 1
}
puts "Timing constraints are met."
