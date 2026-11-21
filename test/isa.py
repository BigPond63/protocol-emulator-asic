# SPDX-License-Identifier: Apache-2.0
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

NUM_SLOTS = 32
JMP_SELF_3 = 0b100_00000_000_00011  # jmp 3 (used as padding)

# Test program: set x,3 / loop: jmp x--,1 / set pins,1 / end: jmp 3
PROGRAM = [
    0b010_00000_010_00011,  # 0: set x, 3
    0b100_00000_010_00001,  # 1: jmp x--, 1
    0b010_00000_000_00001,  # 2: set pins, 1
    0b100_00000_000_00011,  # 3: jmp 3
]

PROGRAM_WAIT = [
    0b011_00000_010_00000, # 0: wait 1 pin 0
    0b010_00000_000_00001, # 1: set pins, 1
    0b100_00000_000_00010, # 2: jmp 2

]

LOAD_EN = 1 << 0    # ui_in[0]
LOAD_DATA = 1 << 1  # ui_in[1]


async def load_program(dut, words):
    """Shift every slot in through ui_in[1], MSB first, with ui_in[0] held high.
    Unused slots are padded so no instruction memory is left as X in
    gate-level simulation."""
    words = list(words) + [JMP_SELF_3] * (NUM_SLOTS - len(words))
    for word in words:
        for i in range(15, -1, -1):
            bit = (word >> i) & 1
            dut.ui_in.value = LOAD_EN | (LOAD_DATA if bit else 0)
            await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0  # drop load_en: engine starts from PC 0


@cocotb.test()
async def test_set_and_jmp(dut):
    dut._log.info("Start")
    cocotb.start_soon(Clock(dut.clk, 100, unit="ns").start())  # 10 MHz

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1

    # Load and run
    await load_program(dut, PROGRAM)
    await ClockCycles(dut.clk, 20)

    # After the loop finishes, set pins,1 should have driven pin 0 high
    val = dut.uio_out.value
    dut._log.info(f"uio_out = {val}")
    assert val.is_resolvable, f"uio_out has X/Z bits: {val}"
    assert int(val) & 1 == 1, f"expected uio_out[0] = 1, got {val}"
    assert dut.uo_out.value.is_resolvable and int(dut.uo_out.value) == 0, \
        f"uo_out should be unused (0), got {dut.uo_out.value}"

@cocotb.test()
async def test_wait(dut):
    cocotb.start_soon(Clock(dut.clk, 100, unit="ns").start())

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0          # pin 0 starts LOW
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1

    await load_program(dut, PROGRAM_WAIT)

    # 1. Pin low: WAIT must stall, so set pins,1 never runs
    await ClockCycles(dut.clk, 10)
    val = dut.uio_out.value
    assert val.is_resolvable, f"uio_out has X/Z bits: {val}"
    assert int(val) & 1 == 0, f"WAIT didn't stall: uio_out = {val}"

    # 2. Raise pin 0: WAIT releases, set pins,1 runs
    dut.uio_in.value = 0b0000_0001
    await ClockCycles(dut.clk, 5)
    val = dut.uio_out.value
    assert val.is_resolvable, f"uio_out has X/Z bits: {val}"
    assert int(val) & 1 == 1, f"WAIT didn't release: uio_out = {val}"