# Check if project name name is provided as an argument
if {$argc < 1} {
    puts "Error: Project name not provided as an argument"
    puts "Usage: vitis_hls -f script.tcl -tclargs <project_name>"
    exit 1
}

# Get the project name from the arguments and set the device part
set overlay_name [lindex $argv 0]
set current_dir [pwd]
set device_part "xczu7ev-ffvc1156-2-e"
set board_part "xilinx.com:zcu104:part0:1.1"
# Create project
create_project $overlay_name  $current_dir/$overlay_name -part $device_part
set_property board_part $board_part [current_project]
# Create block design
create_bd_design "${overlay_name}"
update_compile_order -fileset sources_1

set ps_unit "zynq_ultra_ps_e"
# Add Zynq Processing System
create_bd_cell -type ip -vlnv xilinx.com:ip:${ps_unit}:3.4 ${ps_unit}_0
apply_bd_automation -rule xilinx.com:bd_rule:${ps_unit} -config {apply_board_preset "1" }  [get_bd_cells ${ps_unit}_0]


set hls_ip_repo_path [file join $current_dir ".." "hls" "${overlay_name}_hls" "solution1" "impl" "ip"]
# Add IP repository and scan for IPs
set_property  ip_repo_paths $hls_ip_repo_path [current_project]
update_ip_catalog
create_bd_cell -type ip -vlnv xilinx.com:hls:entry:1.0 entry_0

apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/${ps_unit}_0/M_AXI_HPM0_FPD} Slave {/entry_0/s_axi_control} ddr_seg {Auto} intc_ip {New AXI Interconnect} master_apm {0}}  [get_bd_intf_pins entry_0/s_axi_control]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {/${ps_unit}_0/pl_clk0 (100 MHz)} Clk_xbar {/${ps_unit}_0/pl_clk0 (100 MHz)} Master {/${ps_unit}_0/M_AXI_HPM1_FPD} Slave {/entry_0/s_axi_control} ddr_seg {Auto} intc_ip {/ps8_0_axi_periph} master_apm {0}}  [get_bd_intf_pins ${ps_unit}_0/M_AXI_HPM1_FPD]
set_property -dict [list CONFIG.PSU__MAXIGP0__DATA_WIDTH {32} CONFIG.PSU__MAXIGP1__DATA_WIDTH {32}] [get_bd_cells zynq_ultra_ps_e_0]

connect_bd_net [get_bd_pins entry_0/interrupt] [get_bd_pins ${ps_unit}_0/pl_ps_irq0]



# Create HDL wrapper
make_wrapper -files [get_files $current_dir/$overlay_name/${overlay_name}.srcs/sources_1/bd/${overlay_name}/${overlay_name}.bd] -top
add_files -norecurse add_files -norecurse $current_dir/$overlay_name/${overlay_name}.gen/sources_1/bd/${overlay_name}/hdl/${overlay_name}_wrapper.v

puts "Script completed"