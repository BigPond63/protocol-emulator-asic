/*
    hello this will be the first version of the ISA for the communication protocol

*/

module fifo (
    input logic data,
    output logic data2


);

    logic [7:0] OSR;
    logic [7:0] ISR;
    logic [7:0] X;
    logic [7:0] Y;
    logic [7:0] tx_fifo [0:3];
    logic [7:0] rx_fifo [0:3];

    logic [1:0] tx_wr_ptr;
    logic [1:0] tx_rd_ptr;
    logic [2:0] tx_cnt;

    logic [1:0] rx_wr_ptr;
    logic [1:0] rx_rd_ptr;
    logic [2:0] rx_cnt;


endmodule