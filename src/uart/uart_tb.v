`timescale 1ns/1ps

module uart_tx_tb;

    parameter CLKS_PER_BIT = 4;

    reg        clk;
    reg        rst;
    reg        start;
    reg  [7:0] data;
    wire       tx;
    wire       busy;

    uart_tx #(.CLKS_PER_BIT(CLKS_PER_BIT)) dut (
        .clk   (clk),
        .rst   (rst),
        .start (start),
        .data  (data),
        .tx    (tx),
        .busy  (busy)
    );

    // clock: period 10 ns
    initial clk = 1'b0;
    always #5 clk = ~clk;

    integer pass_count = 0;
    integer fail_count = 0;

    task send_and_check(input [7:0] expected);
        reg [7:0] received;
        reg       ok;
        integer   i;
        begin
            ok = 1'b1;

            // 1. send the byte
            data  = expected;
            start <= 1'b1;
            @(posedge clk);
            start <= 1'b0;

            // 2. wait for the start bit, then move to its middle
            wait (tx == 1'b0);
            repeat (CLKS_PER_BIT / 2) @(posedge clk);
            if (tx !== 1'b0) begin
                $display("FAIL (0x%h): start bit not low", expected);
                ok = 1'b0;
            end

            // 3. sample the 8 data bits, one per bit-time (LSB first)
            for (i = 0; i < 8; i = i + 1) begin
                repeat (CLKS_PER_BIT) @(posedge clk);
                received[i] = tx;
            end

            // 4. check the stop bit
            repeat (CLKS_PER_BIT) @(posedge clk);
            if (tx !== 1'b1) begin
                $display("FAIL (0x%h): stop bit not high", expected);
                ok = 1'b0;
            end

            // 5. compare and report
            if (received !== expected) begin
                $display("FAIL: expected 0x%h, got 0x%h", expected, received);
                ok = 1'b0;
            end

            if (ok) begin
                $display("PASS: 0x%h", expected);
                pass_count = pass_count + 1;
            end else begin
                fail_count = fail_count + 1;
            end

            // 6. let the DUT return to idle before the next byte
            wait (busy == 1'b0);
            @(posedge clk);
        end
    endtask

    initial begin
        $dumpfile("wave.vcd");
        $dumpvars(0, uart_tx_tb);

        // initial values and reset
        rst   = 1'b1;
        start = 1'b0;
        data  = 8'h00;
        repeat (3) @(posedge clk);
        rst = 1'b0;
        repeat (2) @(posedge clk);

        send_and_check(8'h41);
        send_and_check(8'h00);
        send_and_check(8'hFF);
        send_and_check(8'h55);
        send_and_check(8'hAA);

        $display("%0d passed, %0d failed", pass_count, fail_count);
        $finish;
    end

    // watchdog: stops the simulation if something hangs
    initial begin
        #1_000_000;
        $display("TIMEOUT: simulation hung");
        $finish;
    end

endmodule