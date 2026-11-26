// serial_loader.sv
// Shifts in one bit per clock (MSB first) while `en` is high.
// On the clock that carries the last bit, `valid` is high and `word` holds the full value.
// Dropping `en` resets the bit count, so each burst must be whole words.

module serial_loader #(
    parameter WIDTH = 16          // bits per word, must be >= 2
)(
    input  logic             clk,
    input  logic             rst_n,
    input  logic             en,
    input  logic             data,
    output logic [WIDTH-1:0] word,
    output logic             valid
);

    logic [WIDTH-2:0]         shift;   // holds the first WIDTH-1 bits
    logic [$clog2(WIDTH)-1:0] cnt;

    always_ff @(posedge clk) begin
        if (!rst_n || !en) begin
            cnt <= '0;
        end else begin
            shift <= {shift[WIDTH-3:0], data};
            cnt   <= cnt + 1'b1;   // wraps to 0 after the last bit
        end
    end

    // Combinational, so the consumer writes on the same edge as the last bit
    assign word  = {shift, data};
    assign valid = en && (cnt == ($clog2(WIDTH))'(WIDTH - 1));

endmodule