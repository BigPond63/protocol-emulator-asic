`default_nettype none
`timescale 1ns / 1ps

/* This testbench just instantiates the module and makes some convenient wires
   that can be driven / tested by the cocotb test.py.
*/
module tb ();

  // Dump the signals to a FST file. You can view it with gtkwave or surfer.
  initial begin
    $dumpfile("tb.fst");
    $dumpvars(0, tb);
    #1;
  end

  // Wire up the inputs and outputs:
  // Signals driven by the cocotb test (same names as spi_controller's ports)
  reg clk;
  reg rst;
  reg start;
  reg cipo;
  reg [7:0] tx_data;

  // Map them onto the Tiny Tapeout pins (must match info.yaml)
  wire       rst_n  = ~rst;
  wire       ena    = 1'b1;
  wire [7:0] ui_in  = {tx_data[5:0], cipo, start};
  wire [7:0] uio_in = {6'b0, tx_data[7:6]};
  wire [7:0] uo_out;
  wire [7:0] uio_out;
  wire [7:0] uio_oe;

  // Outputs the test reads
  wire       copi    = uo_out[0];
  wire       cs_n    = uo_out[1];
  wire       sclk    = uo_out[2];
  wire       done    = uo_out[3];
  wire [7:0] rx_data = {uio_out[7:4], uo_out[7:4]};

  // Replace tt_um_example with your module name:
  tt_um_MykiCard78 user_project (
      .ui_in  (ui_in),    // Dedicated inputs
      .uo_out (uo_out),   // Dedicated outputs
      .uio_in (uio_in),   // IOs: Input path
      .uio_out(uio_out),  // IOs: Output path
      .uio_oe (uio_oe),   // IOs: Enable path (active high: 0=input, 1=output)
      .ena    (ena),      // enable - goes high when design is selected
      .clk    (clk),      // clock
      .rst_n  (rst_n)     // not reset
  );

endmodule
