


# fwft fifo
# standard fifo


import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, RisingEdge, ReadOnly, Timer


# Steps to walk through
    # Make a clock
    # Reset state of FIFO
    # Instantiate FIFO module for RX and TX

# Tests to do
    # Initial state
    # Writing one data entry
    # Reading one data entry
    # Trying to write while fifo is full
    # Trying to read when fifo is empty
    # Read and write in the same cycle
    # Do nothing -> Stay the same 


RESET_CYCLES = 5
CLK_PERIOD_NS = 10

@cocotb.test()
async def test_clock(dut):
    clk = Clock(dut.clk, 10, unit="ns")

    cocotb.start_soon(clk.start())

    await ClockCycles(dut.clk, 5)


@cocotb.test()
async def test_reset(dut):
    Clock(dut.clk, CLK_PERIOD_NS, unit="ns").start()

    # Set inputs to 0
    dut.wr_en.value = 0
    dut.rd_en.value = 0
    dut.wr_data.value = 0
    
    # Set register value to non-initial state to check reset works
    dut.wr_ptr.value = 1

    dut.rst_n.value = 0 # Reset value, active low

    await ClockCycles(dut.clk, RESET_CYCLES)
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1

    await RisingEdge(dut.clk)
    await ReadOnly()

    assert dut.wr_ptr.value == 0, f"Reset failure, wr_ptr expected: 0, got {dut.wr_ptr.value}"

    # Create helper function for every new test done
async def setup(dut, reset_cycles=RESET_CYCLES):
    Clock(dut.clk, CLK_PERIOD_NS, unit="ns").start(start_high=False)
    dut.wr_en.value = 0
    dut.rd_en.value = 0
    dut.wr_data.value = 0

    dut.rst_n.value = 0

    await ClockCycles(dut.clk, reset_cycles)
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)



@cocotb.test()
async def test_full(dut):
    await setup(dut)
    
    # Place in first data value for fifo buffer
    dut.wr_en.value = 1
    dut.wr_data.value = 0b0000_0001
    dut.rd_en.value = 0
    dut.rst_n.value = 1

    await RisingEdge(dut.clk)

    await FallingEdge(dut.clk)
    dut.wr_data.value = 0b0000_0010 # 2nd data value 

    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    dut.wr_data.value = 0b0000_0011 # 3rd data value

    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    dut.wr_data.value = 0b0000_0100 # 4th data value

    await RisingEdge(dut.clk)
    await ReadOnly()

    assert dut.count.value == 4, f"Count not at max depth 4, got: {dut.count.value}"
    assert dut.full.value == 1, f"Fifo not showing full, got: {dut.full.value}"
    assert dut.empty.value == 0, f"Fifo should be empty, got: {dut.empty.value}"

    await ClockCycles(dut.clk, 3)


# Helper function to write data 
async def write_entry(dut, data):
    dut.wr_data.value = data
    dut.wr_en.value = 1
    await RisingEdge(dut.clk)
    dut.wr_en.value = 0

async def fill_fifo(dut, values, check_flags=False):
    if check_flags:
        assert dut.empty.value == 1, "empty should be high before any writes"
        assert dut.full.value == 0, "full should be low before any writes"

    for i, val in enumerate(values):
        await write_entry(dut, val)

        if check_flags:
            await FallingEdge(dut.clk)
            is_last = (i == len(values) - 1)
            assert dut.empty.value == 0, f"Write {i}: empty should be low after a write"
            assert dut.full.value == is_last, \
                f"Write {i}: full expected {int(is_last)}, got {dut.full.value}"


    

async def read_entry(dut):
    data = dut.rd_data.value

    dut.rd_en.value = 1
    await RisingEdge(dut.clk)
    dut.rd_en.value = 0
    await FallingEdge(dut.clk)
    
    return data

@cocotb.test()
async def test_drain(dut):
    await setup(dut)
    values_ascending = [
        0b0000_0001, 
        0b0000_0010, 
        0b0000_0011, 
        0b0000_0100
        ]
    
    await fill_fifo(dut, values_ascending)
    await FallingEdge(dut.clk)

    for i, expected in enumerate(values_ascending):
        got = await read_entry(dut)

        is_last = (i == len(values_ascending)-1)
        if not is_last:
            assert dut.empty.value == 0, f"FIFO not shown empty, expected 0, got: {dut.empty.value}"
        else:
            assert dut.empty.value == 1, f"FIFO empty flag error, expected 1, got: {dut.empty.value}"

        assert got == expected, f"Read {i}: expected {expected}, got {got}"

@cocotb.test()
async def test_overflow(dut):
    """
    OVERFLOW TEST:
        Fill values up to the maximum depth of the FIFO
        Try to write another value into the fifo, see if any of the other values change
        Check full flag throughout
    """
    values_descending = [
        0b0000_0100,
        0b0000_0011,
        0b0000_0010,
        0b0000_0001
    ]
    await setup(dut)

    await fill_fifo(dut, values_descending, check_flags=True)

    await write_entry(dut, 0b1000_1000)
    await FallingEdge(dut.clk)
    assert dut.full.value == 1, f"Full dropped after a rejected write"

    # Drain, to check the values and see that an overwrite did not happen
    for i, val in enumerate(values_descending):
        got = await read_entry(dut)

        # Check flags and also entry just read
        assert got == val, f"Wrong fifo data drain, expected: {val}, got: {got}"
    
    # Exact data entries came out, so overflow write was not queued
    assert dut.empty.value == 1, f"Overflow write occured, expected empty: 1, got: {dut.empty.value}"
    
@cocotb.test()
async def test_underflow(dut):
    """Reading while empty is ignored: pointers don't move, next write/read still works."""
    await setup(dut)
    assert dut.empty.value == 1, f"Empty flag not set to 1 when no values in FIFO"

    await read_entry(dut)        # underflow attempt, data discarded
    assert dut.empty.value == 1, f"Empty flag not set to 1 when no values in FIFO"
    assert dut.full.value == 0, f"Full flag not set to 0 when no values in FIFO"
    assert dut.count.value == 0, f"Count register not set to 0 when no values in FIFO"
    

    # write one value (e.g. 0x5A), FallingEdge
    await write_entry(dut, 0x5A)
    await FallingEdge(dut.clk)
    assert dut.empty.value == 0, \
    f"Empty flag not set to 0 when data value inside, got: {dut.empty.value}"
    assert dut.count.value == 1, f"After write: count expected 1, got {dut.count.value}"


    # read it back, assert it equals 0x5A
    data_read = await read_entry(dut)
    assert data_read == 0x5A, f"Data read incorrect, expected: 0x5A, got {data_read}"
    assert dut.empty.value == 1, f"Empty flag not set to 1 when no values in FIFO"
    assert dut.full.value == 0, f"Full flag not set to 0 when no values in FIFO"
    assert dut.count.value == 0, f"After read: count expected 0, got {dut.count.value}"

@cocotb.test()
async def test_read_write_simultaneous(dut):
    """
    Check all cases
        - Partially full with read and write
        - Full, what happens when read and write enabled?
        - Empty, what happens when read and write enabled?
    """
    await setup(dut)

    # Partially full
    await fill_fifo(dut, [0xAB, 0xDF])
    await FallingEdge(dut.clk)

    # Read and write together
    data_read = dut.rd_data.value
    dut.rd_en.value = 1
    await write_entry(dut, 0xFB)
    dut.rd_en.value = 0
    await FallingEdge(dut.clk)

    # Count should stay the same, data is now [ _____, 0xDF,    0xFB,   ______ ]
    #                                                 rd_ptr            wr_ptr

    assert data_read == 0xAB, \
        f"Simultaneous read/write error, data read expected: 0xAB, got: {data_read}"
    assert dut.count.value == 2, \
        f"Simultaneous read/write error for count, expected: 2, got {dut.count.value}"

    # Drain to check other two FIFO values

    for i, val in enumerate([0xDF, 0xFB]):
        data_read = await read_entry(dut)
        assert data_read == val, f"FIFO drained, data incorrect, expected: {val:x}, got: {data_read:x}"

    





    





    


