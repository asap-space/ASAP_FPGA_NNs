# Set project name and target device (modify these variables as needed)
set project_name "vae_hls_project"
set device_part "xczu7ev-ffvc1156-2-e"
set hls_ip_repo_path "[pwd]/../hls/vaemodel1_hls/solution1/impl/ip"

# Create project
create_project ${project_name} ./${project_name} -part ${device_part}

# Create block design
create_bd_design "design_1"
update_compile_order -fileset sources_1

# Add Zynq Processing System
create_bd_cell -type ip -vlnv xilinx.com:ip:zynq_ultra_ps_e:3.4 zynq_ultra_ps_e_0
apply_bd_automation -rule xilinx.com:bd_rule:zynq_ultra_ps_e -config {apply_board_preset "1" }  [get_bd_cells zynq_ultra_ps_e_0]


# Add IP repository and scan for IPs
puts ${hls_ip_repo_path}
set_property  ip_repo_paths  /home/pantunes/sandbox/FPGA_ASAP/HLS/VAENet/hls/vaemodel1_hls/solution1/impl/ip [current_project]
update_ip_catalog

# Add HLS IP (modify the IP name according to your HLS export)
set hls_ip_name "entry"
create_bd_cell -type ip -vlnv xilinx.com:hls:${hls_ip_name}:1.0 ${hls_ip_name}_0
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/zynq_ultra_ps_e_0/M_AXI_HPM0_LPD} Slave {/entry_0/s_axi_control} ddr_seg {Auto} intc_ip {New AXI Interconnect} master_apm {0}}  [get_bd_intf_pins entry_0/s_axi_control]

# Enable HP0 Port on Zynq
set_property -dict [list CONFIG.PSU__USE__S_AXI_GP2 {1}] [get_bd_cells zynq_ultra_ps_e_0]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {/zynq_ultra_ps_e_0/pl_clk0 (96 MHz)} Clk_slave {Auto} Clk_xbar {Auto} Master {/entry_0/m_axi_gmem} Slave {/zynq_ultra_ps_e_0/S_AXI_HP0_FPD} ddr_seg {Auto} intc_ip {New AXI SmartConnect} master_apm {0}}  [get_bd_intf_pins zynq_ultra_ps_e_0/S_AXI_HP0_FPD]

# Create HDL wrapper
make_wrapper -files [get_files /home/pantunes/sandbox/FPGA_ASAP/HLS/VAENet/proj/project_1/project_1.srcs/sources_1/bd/design_1/design_1.bd] -top
add_files -norecurse /home/pantunes/sandbox/FPGA_ASAP/HLS/VAENet/proj/project_1/project_1.gen/sources_1/bd/design_1/hdl/design_1_wrapper.v
set_property top design_1_wrapper [current_fileset]
update_compile_order -fileset sources_1

# set platform properties
set_property platform.default_output_type "sd_card" [current_project]
set_property platform.design_intent.embedded "true" [current_project]
set_property platform.design_intent.server_managed "false" [current_project]
set_property platform.design_intent.external_host "false" [current_project]
set_property platform.design_intent.datacenter "false" [current_project]

# call implement
launch_runs impl_1 -to_step write_bitstream -jobs 32
wait_on_run impl_1

# generate xsa
write_hw_platform -include_bit -force ./${overlay_name}.xsa
validate_hw_platform ./${overlay_name}.xsa

# Copy bitstream and hwh files to current directory for easy access
if {[file exists ./${project_name}/${project_name}.runs/impl_1/design_1_wrapper.bit]} {
    file copy -force ./${overlay_name}/${overlay_name}.runs/impl_1/${design_name}_wrapper.bit ${overlay_name}.bit
    file copy -force ./${overlay_name}/${overlay_name}.gen/sources_1/bd/${design_name}/hw_handoff/${design_name}.hwh ${overlay_name}.hwh
    puts "Bitstream and HWH files copied to current directory"
} else {
    puts "Bitstream generation failed"
}

puts "Script completed"