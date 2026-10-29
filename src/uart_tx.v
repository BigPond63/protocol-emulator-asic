module uart_tx(
    input [0:0] clk,
    input [0:0] rst,
    input [0:0] start,
    input [7:0] data,
    output reg [0:0] tx,
    output reg [0:0] busy
);

parameter CLKS_PER_BIT = 4;        // 115,200 baud rate, 50mhz/115200 = 434 clock cycles per bit
localparam IDLE = 4'b0001;
localparam START = 4'b0010;
localparam DATA = 4'b0100;
localparam STOP = 4'b1000;

reg [3:0] state;
reg [16:0] baud_counter;    // parametrise later on, can fit the 115,200 baud rate currently
reg [2:0] bit_index;         // indicate which bit we are currently on 
reg [7:0] shift_reg;         // initial assignment of data, can change after 'start' is asserted



/*
    state
        IDLE
        START 
        DATA 
        STOP

    baud counter
        count from current bit, from 0 to (CLKS_PER_BIT - 1)

    bit index
        count which data bit you're on

    shift register (8 bits)
        holds the byte being sent

    logic for each state

    
*/
    always @(posedge clk) begin

        if (rst == 1'b1) begin
            state <= IDLE;
            tx <= 1'b1;
            busy <= 1'b0;
            baud_counter <= 17'b0;
            bit_index <= 3'b0;
        end else begin

            case (state)

                IDLE: begin

                    if (start) begin
                        shift_reg <= data;
                        busy <= 1'b1;
                        baud_counter <= 17'b0;
                        bit_index <= 3'b000;
                        state <= START;
                        tx <= 1'b0;
                    end else begin
                        
                        tx <= 1'b1;
                    end

                end

                START: begin

                    tx <= 1'b0;

                    if (baud_counter == CLKS_PER_BIT - 1) begin
                        baud_counter <= 17'b0;
                        tx <= shift_reg[0];
                        shift_reg <= {1'b0, shift_reg[7:1]};
                        state <= DATA;
                    end else begin
                        baud_counter <= baud_counter + 17'b1;
                    end



                end


                DATA: begin

                    if (baud_counter == CLKS_PER_BIT - 1) begin
                        tx <= shift_reg[0];
                        shift_reg <= {1'b0, shift_reg[7:1]};        // concatenate shift
                        bit_index <= bit_index + 3'b1;
                        baud_counter <= 17'b0;

                        if (bit_index == 3'd7) begin
                            state <= STOP;
                            baud_counter <= 17'b0;
                            tx <= 1'b1;
                        end
                    end else begin
                        baud_counter <= baud_counter + 17'b1;
                    end




                end

                STOP: begin

                    if (baud_counter == CLKS_PER_BIT - 1 ) begin
                        state <= IDLE;
                        busy <= 1'b0;
                    end else begin
                        baud_counter <= baud_counter + 17'b1;
                    end

                end

            default: begin
                state <= IDLE;
            end



                
            
            endcase

        end

    end





endmodule