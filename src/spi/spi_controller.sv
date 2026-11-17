


module spi_controller 
    import spi_pkg::*; // import within module header more portable for icarus
#(
    parameter int MODE = MODE0,
    parameter int CLK_DIV = 4
) (
    input logic clk,
    input logic rst,
    input logic start, 
    input logic [7:0] tx_data,
    input logic cipo, 
    

    output logic [7:0] rx_data,
    output logic copi, 
    output logic cs_n,
    output logic sclk,
    output logic done
);

/*
                    top (loopback)
┌──────────────────────────────────────────┐
│  spi_controller          spi_peripheral  │
│  ┌──────────┐  SCLK     ┌──────────┐     │
│  │          │──────────▶│          │     │
│  │          │  COPI     │          │     │
│  │          │──────────▶│          │     │
│  │          │  CIPO     │          │     │
│  │          │◀──────────│          │     │
│  │          │  CS_n     │          │     │
│  │          │──────────▶│          │     │
│  └──────────┘           └──────────┘     │
│  tx_data, start,        rx_data, tx_data,│
│  rx_data, done          rx_valid         │
└──────────────────────────────────────────┘


CPOL = 0: idles LOW     ___┌─┐_┌─┐_┌─┐_┌─┐___
                           first edge = rising

CPOL = 1: idles HIGH    ‾‾‾└─┘‾└─┘‾└─┘‾└─┘‾‾‾
                           first edge = falling



CPHA = 0

CS_n  ‾‾‾\____________________________________/‾‾‾
SCLK  ________┌──┐__┌──┐__┌──┐ ... ┌──┐__________     (CPOL=0)
COPI  ----< b7  >< b6  >< b5  > ... < b0  >-------
              ↑     ↑     ↑        ↑
            sample sample sample  sample  (rising)
           data changes on the falling edges



CPHA = 1
CS_n  ‾‾‾\____________________________________/‾‾‾
SCLK  ______┌──┐__┌──┐__┌──┐ ... ┌──┐____________     (CPOL=0)
COPI  ------< b7  >< b6  >< b5 ... < b0  >--------
               ↑     ↑     ↑         ↑
             sample sample sample  sample  (falling)
           data changes on the rising edges
*/


// parameters / inputs: CPOL, CPHA, CLK_DIV, tx_data[7:0], start

// IDLE
    // sclk = CPOL (idle level), cs_n = 1, done = 0
    // wait for start
    // on start: load tx_shift <= tx_data, bit_cnt <= 0, cs_n <= 0
    //           if CPHA==0: copi <= tx_data[7]   (MSB ready before first edge)

// TRANSFER
    // clk_div counter -> toggle SCLK every CLK_DIV cycles
    // on each toggle:
    //   if this is a "sample" edge  -> rx_shift <= {rx_shift[6:0], cipo}
    //   if this is a "shift" edge   -> tx_shift <= tx_shift << 1; copi <= next MSB

// FINISH
    // sclk = CPOL, cs_n = 1
    // rx_data <= rx_shift
    // done <= 1 (one-cycle pulse)
    // -> IDLE


// create states through type enumerated definition
typedef enum logic [1:0] {
    IDLE, TRANSFER, FINISH
} state_t;

state_t state;

localparam bit CPOL = MODE[1]; // MODE 0 -> Idle low
localparam bit CPHA = MODE[0]; // MODE 0 -> data sampled on first clk edge 

logic [7:0] tx_shift;
logic [7:0] rx_shift;

localparam int DIV_W = $clog2(CLK_DIV);
localparam logic [DIV_W-1:0] DIV_MAX = DIV_W'(CLK_DIV - 1);

logic [DIV_W-1:0] div_cnt;


logic [2:0] bit_cnt;


always_ff @(posedge clk) begin
    
    // Reset logic for ASIC
    if (rst) begin
        state <= IDLE;
        sclk <= CPOL;
        cs_n <= 1'b1;
        copi <= 1'b0;
        done <= 1'b0;
        rx_data <= 8'b0;
        bit_cnt <= 3'b0;
        div_cnt <= {{$clog2(CLK_DIV)}{1'b0}};
        rx_shift <= 8'b0;
        tx_shift <= 8'b0;

    end else begin

        case (state)

            default: state <= IDLE;

            IDLE: begin
                sclk <= CPOL; // start on idle
                cs_n <= 1'b1;
                done <= 1'b0;

                if (start) begin
                    tx_shift <= tx_data;
                    rx_shift <= 8'b0; // received logic to be sent to higher logic
                    if (!CPHA) copi <= tx_data[7]; // Drives data at the first leading edge if CPHA=0
                    state <= TRANSFER;
                    cs_n <= 1'b0;
                    bit_cnt <= 3'b0;
                    div_cnt <= {{$clog2(CLK_DIV)}{1'b0}};
                end

            end

            TRANSFER: begin
                // start sclk, do logic every edge
                if (div_cnt == DIV_MAX) begin
                    div_cnt <= 0;
                    sclk <= ~sclk;

                    if (sclk == CPOL) begin
                        // leading edge logic
                        
                        if (!CPHA) begin
                            rx_shift <= {rx_shift[6:0], cipo}; // sample if CPHA = 0
                        end else begin
                            copi <= tx_shift[7];
                            tx_shift <= {tx_shift[6:0], 1'b0}; // shift data 
                        end


                    end else begin 
                        // trailing edge logic

                        if (CPHA) begin
                            // sample logic
                            rx_shift <= {rx_shift[6:0], cipo};
                        end else if (bit_cnt != 3'd7) begin
                            // shift logic
                            copi <= tx_shift[6];
                            tx_shift <= {tx_shift[6:0], 1'b0};
                        end

                        bit_cnt <= bit_cnt + 3'd1;
                        if (bit_cnt == 3'd7) state <= FINISH;
                    end
                end else begin
                    div_cnt <= div_cnt + 1'b1; 
                end
            end

            FINISH: begin
                cs_n <= 1'b1;
                done <= 1'b1;
                copi <= 1'b0;
                rx_data <= rx_shift;
                state <= IDLE;
            end

        endcase

    end
end


endmodule