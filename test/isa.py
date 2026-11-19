# SPDX-License-Identifier: Apache-2.0
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

# Test program: set x,3 / loop: jmp x--,1 / set pins,1 / end: jmp 3
PROGRAM = [
    0b010_00000_010_00011,  # 0: set x, 3
    0b100_00000_010_00001,  # 1: jmp x--, 1
    0b010_00000_000_00001,  # 2: set pins, 1
    0b100_00000_000_00011,  # 3: jmp 3
]

LOAD_EN = 1 << 0    # ui_in[0]
LOAD_DATA = 1 << 1  # ui_in[1]


async def load_program(dut, words):
    """Shift each 16-bit word in through ui_in[1], MSB first, with ui_in[0] held high."""
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
    pins = int(dut.uio_out.value)
    dut._log.info(f"uio_out = {pins:08b}")
    assert pins & 1 == 1, f"expected uio_out[0] = 1, got {pins:08b}"
    assert int(dut.uo_out.value) == 0, "uo_out should be unused (0)"