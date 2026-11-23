/*
    hello this will be the first version of the fifo for the communication protocol

*/

module fifo #(
    parameter int WIDTH = 8, // bits per entry
    parameter int DEPTH = 4 // how many entries, should be a power of two for circular buffer
) (
    input logic clk,
    input logic rst_n,
    input logic wr_en,
    input logic rd_en,
    input logic [WIDTH-1:0] wr_data,
    output logic [WIDTH-1:0] rd_data,
    output logic full,
    output logic empty
);

localparam int PTR_W = $clog2(DEPTH); // bits to index, depth slots (0, 1, 2, .... , depth-1)
localparam int CNT_W = $clog2(DEPTH + 1); // how much should the count go up to until fifo is full 

logic [WIDTH-1:0] mem [DEPTH];
logic [PTR_W-1:0] wr_ptr, rd_ptr;
logic [CNT_W-1:0] count;

logic do_wr, do_rd;


assign full = (count == CNT_W'(DEPTH));
assign empty = (count == '0);
assign do_wr = wr_en && !full;
assign do_rd = rd_en && !empty;

assign rd_data = mem[rd_ptr];

always_ff @(posedge clk) begin
    if (!rst_n) begin                           
        wr_ptr <= '0;
        rd_ptr <= '0;
        count <= '0;
    end else begin

        if (do_wr) begin

            // write logic
            mem[wr_ptr] <= wr_data;
            wr_ptr <= wr_ptr + 1'b1;

        end 
        
        if (do_rd) begin

            // read logic
            rd_ptr <= rd_ptr + 1'b1;

        end

        case ({do_wr, do_rd})
            2'b00: count <= count;
            2'b01: count <= count - 1'b1;
            2'b10: count <= count + 1'b1;
            2'b11: count <= count; // read and write make count stay the same
            default: count <= count;
        endcase

    end


end



endmodule 
