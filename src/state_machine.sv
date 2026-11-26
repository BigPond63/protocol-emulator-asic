
module state_machine #(
    parameter WIDTH = 32,
    parameter DEPTH = 4
)(
    input logic load_en,
    input logic load_data, 

    input logic clk,
    input logic rst_n,
    input logic [7:0] pins_in,
    output logic [7:0] pins_out,
    output logic [7:0] pindirs,

    input logic tx_en,
    input logic tx_data
);







logic [4:0] load_addr;

localparam logic [2:0] op_push_pull = 3'b000;
localparam logic [2:0] op_io = 3'b001;
localparam logic [2:0] op_set = 3'b010;
localparam logic [2:0] op_wait = 3'b011;
localparam logic [2:0] op_jmp = 3'b100;
localparam logic [2:0] op_mov = 3'b101;
localparam logic [2:0] op_irq = 3'b110;

localparam logic [2:0] set_pins_out = 3'b000;
localparam logic [2:0] set_pindirs = 3'b001;
localparam logic [2:0] set_x = 3'b010;
localparam logic [2:0] set_y = 3'b011;
localparam logic [2:0] set_pins_set = 3'b100;
localparam logic [2:0] set_pins_clr = 3'b101;

localparam logic [2:0] jmp_always = 3'b000;
localparam logic [2:0] jmp_xez = 3'b001;
localparam logic [2:0] jmp_xnezd = 3'b010;
localparam logic [2:0] jmp_yez = 3'b011;
localparam logic [2:0] jmp_ynezd = 3'b100;
localparam logic [2:0] jmp_xney = 3'b101;
localparam logic [2:0] jmp_pinh = 3'b110;
localparam logic [2:0] jmp_osrne = 3'b111;

localparam logic in_dir = 1'b0;
localparam logic out_dir = 1'b1;

localparam logic msb_first = 1'b0;
localparam logic lsb_first = 1'b1;

localparam logic [2:0] io_pins = 3'b000;
localparam logic [2:0] io_x    = 3'b001;
localparam logic [2:0] io_y    = 3'b010;
localparam logic [2:0] io_null = 3'b011;
localparam logic [2:0] io_isr = 3'b100;
localparam logic [2:0] io_pindirs  = 3'b101;
localparam logic [2:0] io_osr = 3'b110;



logic [WIDTH-1:0] X;
logic [WIDTH-1:0] Y;
logic [WIDTH-1:0] osr;
logic [WIDTH-1:0] isr;
logic [15:0] instruc_mem [0:31];
logic [4:0] pc;
logic [15:0] instruction;
logic [2:0] opcode;
logic [7:0] operand;

logic [$clog2(WIDTH):0] osr_cnt;
logic [3:0] delay_cnt;
logic [$clog2(WIDTH):0] isr_cnt;
logic [$clog2(WIDTH):0] isr_cnt_next;

logic [4:0] pc_next;
logic [WIDTH-1:0] x_next;
logic [WIDTH-1:0] y_next;
logic [7:0] pins_out_next;
logic [7:0] pindirs_next;

logic wr_en_rx;
logic [WIDTH-1:0] isr_next;

logic [3:0] shift_amt;
logic [WIDTH-1:0] shift_mask;

logic [WIDTH-1:0] in_data;

logic [WIDTH-1:0] osr_next;
logic [$clog2(WIDTH):0] osr_cnt_next;

logic [WIDTH-1:0] mov_data;

logic [WIDTH-1:0] out_data;


logic [15:0]      instr_word;
logic             instr_valid;
logic [WIDTH-1:0] tx_word;
logic             tx_valid;


fifo #(.WIDTH(WIDTH), .DEPTH(DEPTH)) rx_fifo  (
    .clk(clk),
    .rst_n(rst_n),
    .wr_en(wr_en_rx),
    .rd_en(),
    .wr_data(isr),
    .rd_data(),
    .full(),
    .empty()
);

fifo #(.WIDTH(WIDTH), .DEPTH(DEPTH)) tx_fifo  (
    .clk(clk),
    .rst_n(rst_n),
    .wr_en(tx_valid),
    .rd_en(),
    .wr_data(tx_word),
    .rd_data(),
    .full(),
    .empty()
);

assign instruction = instruc_mem[pc];
assign opcode = instruction[15:13];
assign operand = instruction[7:0];


// instructional memory loader block
serial_loader #(.WIDTH(16)) instr_loader (
    .clk(clk), .rst_n(rst_n), .en(load_en), .data(load_data),
    .word(instr_word), .valid(instr_valid)
);


// Instruction memory write
always_ff @(posedge clk) begin
    if (!rst_n || !load_en) begin
        load_addr <= '0;
    end else if (instr_valid) begin
        instruc_mem[load_addr] <= instr_word;
        load_addr <= load_addr + 1'b1;
    end
end

serial_loader #(.WIDTH(WIDTH)) tx_loader (
    .clk(clk), .rst_n(rst_n), .en(tx_en), .data(tx_data),
    .word(tx_word), .valid(tx_valid)
);


always_comb begin : next_state_values
    pc_next = pc + 5'd1;

    x_next = X;
    y_next = Y;
    pins_out_next = pins_out;
    pindirs_next = pindirs;
    wr_en_rx = '0;
    isr_next = isr;
    isr_cnt_next = isr_cnt;
    shift_amt = '0;
    shift_mask = '0;
    in_data = '0;
    osr_next = osr;
    osr_cnt_next = osr_cnt;
    mov_data = '0;
    out_data = '0;

    case (opcode)
        default: ;

        op_push_pull: begin

                // push logic
            if (operand[7] == 0) begin
                // Data from the outside is given to the cpu 
                // pins -> in -> ISR -> push -> RX FIFO
                wr_en_rx = 1;
                isr_next = '0;
                isr_cnt_next = '0;

            end else begin
                // pull logic

                

            end
        end

        op_io: begin 
            shift_amt = {operand[6:4]==3'b000, operand[6:4]}; // 0b000 is shift by 8
            shift_mask = (WIDTH'(1) << shift_amt) -1; // shift mask for pins_in values

            case (operand[3:1])
                io_pins: in_data = WIDTH'(pins_in);
                io_x: in_data = X;
                io_y: in_data = Y;
                io_null: in_data = '0;
                io_osr: in_data = osr;
                default ;
            endcase

            if (operand[7] == in_dir) begin


                if (operand[0] == msb_first) begin


                    // shift isr and place lower pins as pins_in
                    isr_next = (isr << shift_amt) | (in_data & shift_mask); 
                    
                    isr_cnt_next = isr_cnt + {2'b00, shift_amt};
                end else begin 
                    // lsb first

                    // Use shift mask to ensure correct pins are shifted, then shift right, placing older isr values below 
                    isr_next = ((in_data & shift_mask) << (WIDTH - WIDTH'(shift_amt)) ) | (isr >> shift_amt); 
                    
                    isr_cnt_next = isr_cnt + {2'b00, shift_amt};
                end


            end else begin 
                // out direction logic 

                if (operand[0] == msb_first) begin
                    out_data = (osr >> WIDTH'(WIDTH-shift_amt)) & shift_mask; /* top n bits of osr, moved to bottom, masked */
                    osr_next = osr << shift_amt; /* osr shifted left by n, data value exits from top*/
                end else begin
                    out_data = osr & shift_mask; /* bottom n bits of osr, masked */
                    osr_next = osr >> shift_amt; /* osr shifted right by n, data value exits from bottom*/
                end
                osr_cnt_next = osr_cnt + {2'b00, shift_amt};

                case (operand[3:1])
                    io_pins: pins_out_next = (pins_out & ~shift_mask[7:0]) | out_data[7:0]; /* keep other pins, replace low n */
                    io_x:    x_next = out_data;
                    io_y:    y_next = out_data;
                    default: ;
                endcase


            end


        end

        op_set: begin

            case (operand[7:5]) // selecting which register to modify 
                set_pins_out: pins_out_next[4:0] = operand[4:0];
                set_pindirs: pindirs_next[4:0] = operand[4:0];
                set_x: x_next = {{(WIDTH-5){1'b0}}, operand[4:0]};
                set_y: y_next = {{(WIDTH-5){1'b0}}, operand[4:0]};
                set_pins_set: pins_out_next[4:0] = pins_out[4:0] | operand[4:0];
                set_pins_clr: pins_out_next[4:0] = pins_out[4:0] & ~operand[4:0];
                default: ; 
            endcase

        end


        op_jmp: begin

            case (operand[7:5]) // select which condition for jumping
                jmp_always: pc_next = operand[4:0];
                jmp_xez: pc_next = (X=='0) ? operand[4:0] : pc + 5'd1;

                jmp_xnezd: begin
                    pc_next = (X!='0) ? operand[4:0] : (pc + 5'd1);
                    x_next = X - 1'b1;
                end
                
                jmp_yez: pc_next = (Y=='0) ? operand[4:0] : pc + 5'd1;

                jmp_ynezd: begin
                    pc_next = (Y!='0) ? operand[4:0] : (pc + 5'd1);
                    y_next = Y - 1'b1;
                end

                jmp_xney: pc_next = (X!=Y) ? operand[4:0] : (pc + 5'd1);
                    
                jmp_pinh: pc_next = pins_in[0] ? operand[4:0] : pc + 5'd1; // TODO, jump pin from config in compiler 
                jmp_osrne: pc_next = (osr_cnt < WIDTH) ? operand[4:0] : (pc + 5'd1);
            endcase

        end

        op_mov: begin
            // Get data from source
            case (operand[2:0])
                io_pins: mov_data = WIDTH'(pins_in);
                io_x: mov_data = X;
                io_y: mov_data = Y;
                io_null: mov_data = '0;
                io_isr: mov_data = isr;
                io_osr: mov_data = osr;
                default ;
            endcase

            case (operand[7:5])
                io_pins: pins_out_next = mov_data[7:0];
                io_x: x_next = mov_data;
                io_y: y_next = mov_data;
                io_null: ;
                io_isr: begin
                    isr_next = mov_data;
                    isr_cnt_next = '0;
                end
                io_osr: begin
                    osr_next = mov_data;
                    osr_cnt_next = '0;
                end
                default ;
            endcase

        end

        op_wait: begin
            // src 0 = pin, src 1 = irq flag
            
                if (operand[7] == 1'b0) begin

                    // pins_in value through indexing not matching polarity in instruction
                    if (pins_in[operand[2:0]] != operand[6]) begin
                        // wait logic
                        pc_next = pc;
                        x_next = X;
                        y_next = Y;
                        pins_out_next = pins_out;
                        pindirs_next = pindirs;

                    end

                end else begin
                    // IRQ wait logic TODO
                end
        end

    endcase
end

always_ff @(posedge clk) begin

    if (!rst_n || load_en) begin
        X <= '0;
        Y <= '0;
        pc <= '0;
        pins_out <= '0;
        pindirs <= '0;
        isr <= '0;
        isr_cnt <= '0;
        osr <= '0;
        osr_cnt <= '0;
    end else begin
        X <= x_next;
        Y <= y_next;
        pc <= pc_next;
        pins_out <= pins_out_next;
        pindirs <= pindirs_next;
        isr <= isr_next;
        isr_cnt <= isr_cnt_next;
        osr <= osr_next;
        osr_cnt <= osr_cnt_next;
        
    end

end



endmodule