# Copyright (C) 2022 Xilinx, Inc
# SPDX-License-Identifier: BSD-3-Clause
# Edited by Pedro Antunes

# Rebuild HLS IP from source
set current_dir [pwd]
set source_dir "../vae_ip"
set item "vaemodel1_hls"
set solution_dir "${source_dir}/${item}/solution1"
cd $source_dir
if {[catch { glob -directory ${solution_dir}/impl/ip/ *.zip} zip_file]} {
# Build IP only if a packaged IP does not exist
    puts "Building $item IP"
    exec vitis_hls -f script.tcl
} else {
# Skip IP when a packaged IP exists in ip directory
    puts "Skipping building $item"
}
unset zip_file
# Testing the built IP
puts "Checking $item"
# Replace the report file opening with error checking
if {[catch {set fd [open ${solution_dir}/syn/report/${item}_csynth.rpt r]} err]} {
    puts "ERROR: Cannot open report file: $err"
    exit 1
}
set timing_flag 0
set latency_flag 0
while { [gets $fd line] >= 0 } {
# Check whether the timing has been met
  if [string match {+ Timing: } $line]  { 
    set timing_flag 1
    set latency_flag 0
    continue
  }
  if {$timing_flag == 1} {
    if [regexp {[0-9]+} $line]  {
      set period [regexp -all -inline {[0-9]*\.[0-9]*} $line]
      lassign $period target estimated uncertainty
      if {$target < $estimated} {
          puts "ERROR: Estimated clock period $estimated > target $target. (Estimated: $estimated, Target: $target)"
          puts "ERROR: Revise $item to be compatible with vitis_hls."
          exit 1
      }
    }
  }
# Check whether the II has been met
  if [string match {+ Latency: } $line]  { 
    set timing_flag 0
    set latency_flag 1
    continue
  }
  if {$latency_flag == 1} {
    if [regexp {[0-9]+} $line]  {
      set interval [regexp -all -inline {[0-9]*\.*[0-9]*} $line]
      lassign $interval lc_min lc_max la_min la_max achieved target
      if {$achieved != $target} {
          puts "ERROR: Achieved II $achieved != target $target. (Achieved: $achieved, Target: $target)"
          puts "ERROR: Revise $item to be compatible with vitis_hls."
          exit 1
      }
    }
  }
# Testing ends
  if [string match {== Utilization Estimates} $line]  { 
      unset timing_flag latency_flag period interval target estimated uncertainty lc_min lc_max la_min la_max achieved
      break
  }
}
# At the end of testing, before restoring the directory, close the file:
close $fd
unset fd
cd $current_dir
puts "HLS IP builds complete"
