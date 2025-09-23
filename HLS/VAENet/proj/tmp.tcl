create_project project_1 /home/pantunes/sandbox/FPGA_ASAP/HLS/VAENet/proj/project_1 -part xczu7ev-ffvc1156-2-e
set_property board_part xilinx.com:zcu104:part0:1.1 [current_project]
update_compile_order -fileset sources_1
create_bd_cell -type ip -vlnv xilinx.com:ip:zynq_ultra_ps_e:3.4 zynq_ultra_ps_e_0
apply_bd_automation -rule xilinx.com:bd_rule:zynq_ultra_ps_e -config {apply_board_preset "1" }  [get_bd_cells zynq_ultra_ps_e_0]
set_property  ip_repo_paths  /home/pantunes/sandbox/FPGA_ASAP/HLS/VAENet/hls/vaemodel1_hls/solution1/impl/ip [current_project]
update_ip_catalog
create_bd_cell -type ip -vlnv xilinx.com:hls:entry:1.0 entry_0
set_property -dict [list CONFIG.PSU__USE__S_AXI_GP2 {1}] [get_bd_cells zynq_ultra_ps_e_0]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/zynq_ultra_ps_e_0/M_AXI_HPM0_FPD} Slave {/entry_0/s_axi_control} ddr_seg {Auto} intc_ip {New AXI Interconnect} master_apm {0}}  [get_bd_intf_pins entry_0/s_axi_control]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/entry_0/m_axi_gmem} Slave {/zynq_ultra_ps_e_0/S_AXI_HP0_FPD} ddr_seg {Auto} intc_ip {New AXI SmartConnect} master_apm {0}}  [get_bd_intf_pins zynq_ultra_ps_e_0/S_AXI_HP0_FPD]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {/zynq_ultra_ps_e_0/pl_clk0 (100 MHz)} Clk_xbar {/zynq_ultra_ps_e_0/pl_clk0 (100 MHz)} Master {/zynq_ultra_ps_e_0/M_AXI_HPM1_FPD} Slave {/entry_0/s_axi_control} ddr_seg {Auto} intc_ip {/ps8_0_axi_periph} master_apm {0}}  [get_bd_intf_pins zynq_ultra_ps_e_0/M_AXI_HPM1_FPD]
make_wrapper -files [get_files /home/pantunes/sandbox/FPGA_ASAP/HLS/VAENet/proj/project_1/project_1.srcs/sources_1/bd/design_1/design_1.bd] -top
add_files -norecurse /home/pantunes/sandbox/FPGA_ASAP/HLS/VAENet/proj/project_1/project_1.gen/sources_1/bd/design_1/hdl/design_1_wrapper.v
launch_runs synth_1 -jobs 32
launch_runs impl_1 -jobs 32
launch_runs impl_1 -to_step write_bitstream -jobs 32
