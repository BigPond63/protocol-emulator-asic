/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_MykiCard78 (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

/*
  // All output pins must be assigned. If not used, assign to 0.
  assign uo_out  = ui_in + uio_in;  // Example: ou_out is the sum of ui_in and uio_in
  assign uio_out = 0;
  assign uio_oe  = 0;
*/
wire [7:0] rx_data;
wire copi, cs_n, sclk, done;

assign uo_out  = {rx_data[3:0], done, sclk, cs_n, copi};
assign uio_out = {rx_data[7:4], 4'b0};
assign uio_oe  = 8'b1111_0000;     // uio[7:4] outputs, uio[3:0] inputs

/*
UART Transmission Test
uart_tx #(.CLKS_PER_BIT(4)) ins0 ( 
  .clk(clk),
  .rst(~rst_n),
  .start(ui_in[0]),
  .data(8'h44),
  .tx(tx_data),
  .busy(busy_sig)
);
*/

spi_controller #(.MODE(0), .CLK_DIV(4)) ins0 (
  .clk(clk),
  .rst(~rst_n),
  .start(ui_in[0]),
  .tx_data({uio_in[1:0], ui_in[7:2]}),
  .cipo(ui_in[1]),

  .rx_data(rx_data),
  .copi(copi),
  .cs_n(cs_n),
  .sclk(sclk),
  .done(done)
);

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, uio_in[7:2], 1'b0};

endmodule
