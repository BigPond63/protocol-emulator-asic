`default_nettype none
`timescale 1ns / 1ps

module tb_state_machine;

    logic clk = 0;
    logic rst_n = 0;
    logic load_en = 0;
    logic load_data = 0;
    logic [7:0] pins_in = '0;
    logic [7:0] pins_out;
    logic [7:0] pindirs;

    state_machine dut (
        .clk      (clk),
        .rst_n    (rst_n),
        .load_en  (load_en),
        .load_data(load_data),
        .pins_in  (pins_in),
        .pins_out (pins_out),
        .pindirs  (pindirs)
    );

    always #5 clk = ~clk;   // 10 ns clock period

    // Send one 16-bit instruction, MSB first, one bit per clock
    task send_word(input logic [15:0] w);
        for (int i = 15; i >= 0; i--) begin
            load_data = w[i];
            @(posedge clk); #1;
        end
    endtask

    initial begin
        $dumpfile("tb_state_machine.vcd");
        $dumpvars(0, tb_state_machine);

        // 1. Reset
        #20 rst_n = 1;

        // 2. Load the program (engine is held while load_en = 1)
        load_en = 1;
        send_word(16'b010_00000_010_00011);   // 0: set x, 3
        send_word(16'b100_00000_010_00001);   // 1: jmp x--, 1
        send_word(16'b010_00000_000_00001);   // 2: set pins, 1
        send_word(16'b100_00000_000_00011);   // 3: jmp 3
        load_en = 0;                          // engine starts from PC = 0

        // 3. Let it run, then check the result
        repeat (20) @(posedge clk);
        #1;
        if (dut.X == 8'd255 && pins_out[0] == 1'b1 && dut.pc == 5'd3)
            $display("PASS: X=%0d pins_out=%b pc=%0d", dut.X, pins_out, dut.pc);
        else
            $display("FAIL: X=%0d pins_out=%b pc=%0d", dut.X, pins_out, dut.pc);

        $finish;
    end

endmodule