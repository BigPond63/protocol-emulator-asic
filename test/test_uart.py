# SPDX-License-Identifier: Apache-2.0
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

CLKS_PER_BIT = 4
EXPECTED_BYTE = 0x44


def tx(dut):
    return int(dut.uo_out.value) & 1


def busy(dut):
    return (int(dut.uo_out.value) >> 1) & 1


@cocotb.test()
async def test_uart_tx(dut):
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = EXPECTED_BYTE   # byte to send (works if data comes from uio_in or is hardwired 0x44)
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)

    # Idle: line high, not busy
    assert tx(dut) == 1, "TX should idle high"
    assert busy(dut) == 0, "Should not be busy when idle"

    # Pulse start for one clock
    dut.ui_in.value = 1
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0

    # Wait for the start bit (TX goes low)
    for _ in range(20):
        if tx(dut) == 0:
            break
        await ClockCycles(dut.clk, 1)
    else:
        assert False, "Start bit never appeared"

    # Move to the middle of the start bit
    await ClockCycles(dut.clk, CLKS_PER_BIT // 2)
    assert tx(dut) == 0, "Start bit should be 0"
    assert busy(dut) == 1, "Should be busy while sending"

    # Sample 8 data bits, LSB first
    received = 0
    for i in range(8):
        await ClockCycles(dut.clk, CLKS_PER_BIT)
        received |= tx(dut) << i
    dut._log.info(f"Received 0x{received:02X}")
    assert received == EXPECTED_BYTE, f"Expected 0x{EXPECTED_BYTE:02X}, got 0x{received:02X}"

    # Stop bit
    await ClockCycles(dut.clk, CLKS_PER_BIT)
    assert tx(dut) == 1, "Stop bit should be 1"

    # Back to idle
    await ClockCycles(dut.clk, CLKS_PER_BIT * 2)
    assert busy(dut) == 0, "Busy should clear after the stop bit"
    assert tx(dut) == 1, "TX should return to idle high"
