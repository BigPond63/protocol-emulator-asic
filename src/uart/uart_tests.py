# Test the uart transmission with cocotb

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

import random


CLKS_PER_BIT = 4

async def run_clock(dut):
    while True:
        dut.clk.value = 1
        await Timer(10, "ns")
        dut.clk.value = 0
        await Timer(10, "ns")
# end test_clock

# Decorator or not, it is a coroutine

@cocotb.test() # This line registers something as a test (without the decorator, it is just a helper)
async def test_clock_concurrent(dut):
    # Start clock running concurrently to main test coroutine
    cocotb.start_soon(run_clock(dut))

    # Hand control back to the simulator, do other things while clock is running
    await Timer(100, "ns")

# decorator 
@cocotb.test()
async def test_reset(dut):
    # start clock in the background along with current test
    cocotb.start_soon(run_clock(dut))


    # load in values to be tested
    dut.start.value = 1
    dut.rst.value = 1
    dut.data.value = 0

    exp_tx = 1
    exp_busy = 0
    exp_baud = 0
    exp_bit_index = 0

    # pause test until next rising edge
    await RisingEdge(dut.clk)
    await Timer(1, "ns") # await 1ns in simulation
    
    assert dut.tx.value == exp_tx, f"tx = {dut.tx.value}, expected {exp_tx}"
    assert dut.busy.value == exp_busy, f"busy = {dut.busy.value}, expected {exp_busy}"
    assert dut.baud_counter.value == exp_baud, f"baud_counter = {dut.baud_counter.value}, expected {exp_baud}"
    assert dut.bit_index.value == exp_bit_index, f"bit_index = {dut.bit_index.value}, expected {exp_bit_index}"

# helper coroutine -> reset after every test
async def reset(dut):
    dut.start.value = 0
    dut.data.value = 0
    dut.rst.value = 1

    for _ in range(CLKS_PER_BIT - 1):
        await RisingEdge(dut.clk)
    dut.rst.value = 0



async def check_single_frame(dut, data):
    # Clock in parallel to testing 'START' state
    
    await reset(dut)

    dut.data.value = data

    dut.start.value = 1

    await RisingEdge(dut.clk)
    await Timer(1, "ns")


    dut.start.value = 0


    # Check 'idle to start' state values 
    exp_tx = 0
    exp_busy = 1
    exp_baud = 0
    exp_bit_index = 0
    

    exp_tx_data = 1
    exp_baud_start = CLKS_PER_BIT - 1
    exp_bit_index_start = 0
    exp_shift_reg = data

    assert dut.tx.value == exp_tx, f"tx = {dut.tx.value}, expected {exp_tx}"
    assert dut.busy.value == exp_busy, f"busy = {dut.busy.value}, expected {exp_busy}"
    assert dut.baud_counter.value == exp_baud, f"baud counter = {dut.baud_counter.value}, expected {exp_baud}"
    assert dut.bit_index.value == exp_bit_index, f"bit index = {dut.bit_index.value}, expected {exp_bit_index}"

    # check everything is correct in start state

    # wait until the very last iteration of 'START'
    for _ in range(CLKS_PER_BIT - 1):
        await RisingEdge(dut.clk)
    await Timer(1, "ns")

    # check values are correct
    assert dut.baud_counter.value == exp_baud_start, f"baud counter = {dut.baud_counter.value}, expected {exp_baud_start}"
    assert dut.shift_reg.value == exp_shift_reg, f"shift register = {dut.shift_reg.value}, expected {exp_shift_reg}"
    assert dut.tx.value == exp_tx, f"tx = {dut.tx.value}, expected {exp_tx}"

    # 4th edge, getting into 'DATA' state
    await RisingEdge(dut.clk)
    await Timer(1, "ns")
    assert dut.baud_counter.value == exp_baud, f"baud counter = {dut.baud_counter.value}, expected {exp_baud}"
    assert dut.tx.value == (exp_shift_reg & 1), f"tx = {dut.tx.value}, expected {exp_shift_reg & 1}"
    assert dut.shift_reg.value == (exp_shift_reg >> 1), f"shift register = {dut.shift_reg.value}, expected {exp_shift_reg >> 1}"
    assert dut.state.value == 0b0100, f"state = {dut.state.value}, expected DATA (0b0100)"


    # now in data
    for i in range(1,8):
            

        for _ in range(CLKS_PER_BIT):
            await RisingEdge(dut.clk)
        await Timer(1, "ns")
        assert dut.baud_counter.value == exp_baud, f"baud counter = {dut.baud_counter.value}, expected {exp_baud}"
        assert dut.shift_reg.value == (exp_shift_reg >> (i+1)), f"shift register = {dut.shift_reg.value}, expected {(exp_shift_reg >> (i+1))}"
        assert dut.tx.value == ((exp_shift_reg >> (i)) & 1), f"tx = {dut.tx.value}, expected {((exp_shift_reg >> (i)) & 1)}"

    # Transition to stop
    for _ in range(CLKS_PER_BIT):
        await RisingEdge(dut.clk)
    await Timer(1, "ns")
    assert dut.state.value == 0b1000, f"state = {dut.state.value}, expected 4b1000"
    assert dut.baud_counter.value == exp_baud, f"baud counter = {dut.baud_counter.value}, expected {exp_baud}"
    assert dut.tx.value == 1, f"tx = {dut.tx.value}, expected 1"
    assert dut.busy.value == exp_busy, f"busy = {dut.busy.value}, expected {exp_busy}"

    # Test 'STOP' state

    for _ in range(CLKS_PER_BIT):
        await RisingEdge(dut.clk)
    await Timer(1, "ns")

    assert dut.busy.value == 0, f"busy = {dut.busy.value}, expected 0"
    assert dut.state.value == 0b0001, f"state = {dut.state.value}, expected 0b0001"
    assert dut.tx.value == 1, f"tx = {dut.tx.value}, expected 1"

@cocotb.test()
async def test_patterns(dut):
    cocotb.start_soon(run_clock(dut))
    for value in [0x00, 0xFF, 0x55, 0xAA, 0x01, 0x80, 0xA5]:
        await check_single_frame(dut, value)


@cocotb.test()
async def test_random(dut):
    cocotb.start_soon(run_clock(dut))
    for _ in range(500):
        
        await check_single_frame(dut, random.randint(0,255))
    



