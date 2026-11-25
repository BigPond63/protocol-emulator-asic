
"""
cocotb testbench for the FIFO in src/fifo_test.sv (module `fifo`).

DUT behaviour
-------------

First-word fall-through fifo: When not empty, rd_data already shows head entry. 
    Parameters: DEPTH = 4, WIDTH=8
    Active low reset (rst_n). Reset clears pointers, count and flags, but not memory, 
        but will be overwritten with new entries
    Writes only when full is logic 0
    Read only when fifo is not empty
    Simultaneous read and write behaviour:
        Partially full: Both happen
        Full: Only read happens
        Empty: Write happens, read ignored

Testbench conventions
---------------------
- Every test calls setup() first: starts the clock and resets the DUT.
  The simulator is not restarted between tests, so never rely on state
  left behind by a previous test.
- Inputs are driven and outputs sampled at the FALLING edge, so values
  have settled after the rising edge that updated them.
- Helpers (write_entry, read_entry, fill_fifo) drive the DUT; tests do
  the checking.
- test_deque_random compares the DUT against a collections.deque model.
  The model decides do_wr/do_rd from its own state before each edge.

Running
-------
    make                                    
    make COCOTB_TESTCASE=test_drain         
    gtkwave sim_build/rtl/fifo.fst &        
    make clean                             
"""


import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, RisingEdge, ReadOnly, Timer
import random
from collections import deque 


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
seed_deque = 7
depth_fifo = 4


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

async def wait_cycles(dut, n_cycles = 5):
    await ClockCycles(dut.clk, 5)


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
async def test_read_write_simultaneous_partial_full(dut):
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

    
    # Now test r/w simultaneously with empty fifo (claude)
@cocotb.test()
async def test_rw_simultaneous_empty(dut):
    """
    Read + write together on an empty FIFO:
    write goes through, read is ignored (do_rd blocked by empty).
    """
    await setup(dut)
    assert dut.empty.value == 1, f"Before r/w: empty expected 1, got {dut.empty.value}"

    # Read and write together. rd_data is stale while empty, so it isn't sampled or checked.
    dut.rd_en.value = 1
    await write_entry(dut, 0x5A)
    dut.rd_en.value = 0
    await FallingEdge(dut.clk)              # let the simultaneous edge land

    # Write happened, read was ignored: one entry in the FIFO
    assert dut.count.value == 1, f"After r/w: count expected 1, got {dut.count.value}"
    assert dut.empty.value == 0, f"After r/w: empty expected 0, got {dut.empty.value}"
    assert dut.full.value == 0,  f"After r/w: full expected 0, got {dut.full.value}"

    # The written value is now the head, and reading it empties the FIFO
    data_read = await read_entry(dut)
    assert data_read == 0x5A, f"Read back: expected 0x5a, got {data_read:x}"
    assert dut.empty.value == 1, f"After read: empty expected 1, got {dut.empty.value}"
    assert dut.count.value == 0, f"After read: count expected 0, got {dut.count.value}"
    
@cocotb.test()
async def test_rw_simultaneous_full(dut):
    """
    Read and write together on a full FIFO
    Expected behaviour: Write should fail, read goes through
    """

    await setup(dut)
    
    await fill_fifo(dut, [0xAB, 0xCD, 0xEF, 0xFA]) # Can do a rand here

    await FallingEdge(dut.clk)

    # Read / write data simultaneously
    data_read = dut.rd_data.value
    dut.rd_en.value = 1
    await write_entry(dut, 0x12)
    dut.rd_en.value = 0 
    await FallingEdge(dut.clk)

    assert data_read == 0xAB, f"Read wrong data value for FIFO, expected 0xAB, got: {data_read}"
    assert dut.full.value == 0, f"FIFO full flag incorrect, expected: 0, got: {dut.full.value}"
    assert dut.empty.value == 0, f"FIFO empty flag incorrect, expected 0, got : {dut.empty.value}"


    # Drain data to check that writing 0x12 was never done
    for i, val in enumerate([0xCD, 0xEF, 0xFA]):
        rd_now = await read_entry(dut)
        assert rd_now == val, f"Read data was incorrect for a r/w simultaneous, expected: {val:x}, got: {rd_now:x}"
        if (i + 1==len([0xCD, 0xEF, 0xFA])):
            assert dut.empty.value == 1, \
                f"Empty value is not set to 1 while simeltaneous r/w occurs, expected: 1, got {dut.empty.value}"
        else:
            assert dut.empty.value == 0, \
                f"Empty value is not set to 0 while simulataneous r/w occurs, expected: 0, got: {dut.empty.value}"
        assert dut.full.value == 0, \
            f"Full value is not set to 0 while simultaneous r/w occurs, expected: 0, got: {dut.full.value}"


@cocotb.test()
async def test_wrap_around(dut):
    """
    Test wraparound behaviour, write 3 and read 3 values 
    """
    await setup(dut)
    values_test = list(range(99)) # Test 99 values, from 0 to 98

    length_list = len(values_test)

    burst = 3 # read and write 3 values each time -> check wrap-around through full/empty flags

    for i in range(0, length_list, burst):
        # Get the chunk of data to r/w
        chunk = values_test[i:i+burst]

        # write data values into fifo
        for val in chunk:
            await write_entry(dut, val)
            await FallingEdge(dut.clk)
            assert dut.empty.value == 0, \
                f"FIFO empty flag incorrect when testing wrap around (writing phase), expected: 0, got {dut.empty.value}"
        
        

        # read data values into fifo, check empty and full flags each time
        for j,val in enumerate(chunk):
            read_value = await read_entry(dut)
            
            if (j== len(chunk)-1):
                assert dut.empty.value == 1, f"Fifo empty flag not 1 when testing wrap around, expected 1, got: {dut.empty.value}"
            else:
                assert dut.empty.value == 0, f"FIFO empty flag incorrect when testing wrap around, expected 0, got: {dut.empty.value}"
            
            assert dut.full.value == 0, f"FIFO full flag incorrect when testing wrap around, expected 0, got: {dut.full.value}"
            assert read_value == val, f"FIFO incorrectly read value when testing wrap around, expected: {val}, got: {read_value}"
        


@cocotb.test()
async def test_deque_random(dut, prob_bit=0.5):
    await setup(dut)
    random.seed(seed_deque)
    dut._log.info(f"Random seed: {seed_deque}")

    # Create object from class 
    deque_model = deque()

    for i in range(1000):
        # Set to integer from a random float b/w 0 and 1
        wr_rand = int(random.random() < prob_bit) 
        rd_rand = int(random.random() < prob_bit)
        wr_data = random.getrandbits(8)

        dut.wr_en.value = wr_rand
        dut.rd_en.value = rd_rand
        dut.wr_data.value = wr_data

        do_wr = (len(deque_model) !=depth_fifo) and wr_rand
        do_rd = (len(deque_model)!=0 and rd_rand)

        # Read front of list if read is set
        if do_rd:
            read_data = dut.rd_data.value
            
            assert read_data == deque_model[0], \
                f"Read data from FIFO and deque not the same, expected (deque): {deque_model[0]}, got (fifo): {read_data:d}"
            deque_model.popleft()

        await RisingEdge(dut.clk)
        await FallingEdge(dut.clk)

        if do_wr:
            deque_model.append(wr_data)


        fifo_count_cur = dut.count.value
        deque_count_cur = len(deque_model)
        deque_full_flag = (len(deque_model) == depth_fifo)

        assert deque_count_cur == fifo_count_cur, \
            f"FIFO and deque model count not the same, expected (deque): {deque_count_cur}, got (fifo): {fifo_count_cur:d}"
        
        if deque_count_cur == 0:
            assert dut.empty.value == 1, f"Empty flag not set when comparing to deque model, expected 1, got: {dut.empty.value}"
        else:
            assert dut.empty.value == 0, f"Empty flag incorrect when comparing to deque model, expected 0, got{dut.empty.value}"

        assert dut.full.value == deque_full_flag, f"Full flag incorrect when comparing to deque model, expected: {deque_full_flag}, got: {dut.full.value}"
        


@cocotb.test()
async def test_reset_from_full(dut):
    await setup(dut)

    data_fill = [0xFF, 0xFA, 0xAF, 0xBE]
    await fill_fifo(dut, data_fill)

    await FallingEdge(dut.clk)
    dut.rst_n.value = 0
    await wait_cycles(dut, 5)
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1

    # Check that read and write pointers are working correctly after reset
    await write_entry(dut, 0x23)
    await FallingEdge(dut.clk)

    read_data = await read_entry(dut)

    assert read_data == 0x23, \
        f"Read data incorrect from testing reset, expected 0x23, got:{read_data}"
    assert dut.empty.value == 1,\
     f"After reset: empty expected 1, got {dut.empty.value}"
    assert dut.full.value == 0, \
     f"After reset: full expected 0, got {dut.full.value}"
    assert dut.count.value == 0, \
    f"After reset: count expected 0, got {dut.count.value}"














    


