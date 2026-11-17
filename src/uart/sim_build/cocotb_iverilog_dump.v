module cocotb_iverilog_dump();
initial begin
    $dumpfile("sim_build/uart_tx.fst");
    $dumpvars(0, uart_tx);
end
endmodule
