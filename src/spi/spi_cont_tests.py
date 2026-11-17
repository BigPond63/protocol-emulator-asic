# cocotb tests for spi_controller (all four SPI modes) using a Python peripheral model.
#
# MODE and CLK_DIV are compile-time parameters, so pick them with env vars and run
# the sim once per mode, e.g.:
#   make SPI_MODE=0     (then clean, and again with SPI_MODE=1, 2, 3)
# The Makefile must also pass the same values to the simulator

# Written by Claude Sonnet 5.5 Medium 17/11/2026

import os

import cocotb
from cocotb.triggers import RisingEdge, Timer

MODE = int(os.getenv("SPI_MODE", "0"))
CLK_DIV = int(os.getenv("SPI_CLK_DIV", "4"))
CPOL = (MODE >> 1) & 1
CPHA = MODE & 1

RESET_CYCLES = 5

# cs_n is low from the cycle after the start edge until FINISH:
# 16 sclk toggles * CLK_DIV cycles each, plus the FINISH cycle that raises cs_n.
FRAME_CYCLES = 16 * CLK_DIV + 1

# Same edge cases as the UART test:
#   0x00 / 0xFF -> copi stuck high / low
#   0x80 / 0x01 -> MSB first, LSB last
#   0xAA / 0x55 -> shifting and sampling on the right edges
#   0xF0 / 0x0F -> bit order
#   0xA3 / 0xCA -> asymmetric, catches a reversed byte
TEST_BYTES = [
    0b0000_0000,
    0b1111_1111,
    0b1000_0000,
    0b0000_0001,
    0b1010_1010,
    0b0101_0101,
    0b1111_0000,
    0b0000_1111,
    0b1010_0011,
    0b1100_1010,
]


async def run_clock(dut):
    while True:
        dut.clk.value = 1
        await Timer(10, "ns")
        dut.clk.value = 0
        await Timer(10, "ns")


async def wait_cycles(dut, n):
    for _ in range(n):
        await RisingEdge(dut.clk)
    await Timer(1, "ns")


def check(dut, **expected):
    for name, exp in expected.items():
        actual = int(getattr(dut, name).value)
        assert actual == exp, f"{name} = {actual:#x}, expected {exp:#x}"


class SpiPeripheralModel:
    """Software SPI peripheral. Watches sclk / cs_n / copi, drives cipo, and
    checks protocol rules that must hold on every cycle."""

    def __init__(self, dut):
        self.dut = dut
        self.cycle = 0
        self.tx_byte = 0          # byte this peripheral sends back to the controller
        self.done_pulses = 0      # total done pulses seen
        self._reset_frame()

    def _reset_frame(self):
        self.out_idx = 0
        self.rx_bits = []         # copi bits sampled by the peripheral, in order
        self.edge_cycles = []     # cycle number of every sclk edge in this frame
        self.cs_fall_cycle = None
        self.cs_low_cycles = 0

    def _next_bit(self):
        bit = (self.tx_byte >> (7 - self.out_idx)) & 1 if self.out_idx < 8 else 0
        self.out_idx += 1
        return bit

    async def run(self):
        dut = self.dut
        prev_cs, prev_sclk, prev_done = 1, CPOL, 0

        while True:
            await RisingEdge(dut.clk)
            await Timer(1, "ns")
            self.cycle += 1

            cs = int(dut.cs_n.value)
            sclk = int(dut.sclk.value)
            copi = int(dut.copi.value)
            done = int(dut.done.value)

            # ---- rules that must always hold ----
            if cs == 1:
                assert sclk == CPOL, f"sclk = {sclk} while cs_n high, idle should be {CPOL}"
            else:
                assert done == 0, "done high during a transfer"
            assert not (done and prev_done), "done held high for more than one cycle"

            if done and not prev_done:
                self.done_pulses += 1

            # ---- frame start ----
            if prev_cs == 1 and cs == 0:
                self._reset_frame()
                self.cs_fall_cycle = self.cycle
                if CPHA == 0:
                    # CPHA=0: first bit must already be on cipo before the first edge
                    dut.cipo.value = self._next_bit()

            # ---- inside a frame ----
            if cs == 0:
                self.cs_low_cycles += 1
                if sclk != prev_sclk:
                    self.edge_cycles.append(self.cycle)
                    leading = (prev_sclk == CPOL)
                    sample_edge = leading if CPHA == 0 else not leading
                    if sample_edge:
                        self.rx_bits.append(copi)
                    else:
                        dut.cipo.value = self._next_bit()

            # ---- frame end ----
            if prev_cs == 0 and cs == 1:
                dut.cipo.value = 0

            prev_cs, prev_sclk, prev_done = cs, sclk, done


async def setup(dut):
    """Start clock, reset the DUT, start the peripheral model."""
    cocotb.start_soon(run_clock(dut))
    dut.rst.value = 1
    dut.start.value = 0
    dut.tx_data.value = 0
    dut.cipo.value = 0
    await wait_cycles(dut, RESET_CYCLES)
    dut.rst.value = 0
    await wait_cycles(dut, 1)

    model = SpiPeripheralModel(dut)
    cocotb.start_soon(model.run())
    return model


async def run_frame(dut, model, tx_byte, peripheral_byte, poke_start_at=None):
    """Send tx_byte while the peripheral returns peripheral_byte, then check everything.
    poke_start_at: cycle (after the real start) at which to pulse start again with
    different data, which the controller must ignore."""
    model.tx_byte = peripheral_byte
    pulses_before = model.done_pulses

    dut.tx_data.value = tx_byte
    dut.start.value = 1
    await wait_cycles(dut, 1)       # controller sees start on this edge
    dut.start.value = 0

    got_done = False
    rx_data = None
    for cycle in range(FRAME_CYCLES + 10):
        if cycle == poke_start_at:
            dut.tx_data.value = tx_byte ^ 0xFF
            dut.start.value = 1
        else:
            dut.start.value = 0

        if int(dut.done.value) == 1:
            got_done = True
            rx_data = int(dut.rx_data.value)
            break
        await wait_cycles(dut, 1)
    dut.start.value = 0

    assert got_done, f"done never asserted for {tx_byte:#04x} (timeout)"

    # let a few more cycles pass: no second frame, no repeated done
    await wait_cycles(dut, 2 * CLK_DIV)

    tag = f"[mode {MODE}, tx {tx_byte:#04x}, peripheral {peripheral_byte:#04x}]"

    assert model.done_pulses - pulses_before == 1, f"{tag} expected exactly one done pulse"

    # controller -> peripheral: copi bits, MSB first
    assert len(model.rx_bits) == 8, f"{tag} peripheral sampled {len(model.rx_bits)} bits, expected 8"
    sent = int("".join(str(b) for b in model.rx_bits), 2)
    assert sent == tx_byte, f"{tag} copi carried {sent:#04x}, bits {model.rx_bits}"

    # peripheral -> controller: cipo bits, captured in rx_data
    assert rx_data == peripheral_byte, f"{tag} rx_data = {rx_data:#04x}"

    # sclk: 8 pulses = 16 edges, each CLK_DIV cycles apart (first one CLK_DIV after cs_n falls)
    assert len(model.edge_cycles) == 16, f"{tag} {len(model.edge_cycles)} sclk edges, expected 16"
    marks = [model.cs_fall_cycle] + model.edge_cycles
    gaps = [b - a for a, b in zip(marks, marks[1:])]
    assert all(g == CLK_DIV for g in gaps), f"{tag} sclk edge spacing {gaps}, expected {CLK_DIV}"

    # cs_n low for exactly one frame
    assert model.cs_low_cycles == FRAME_CYCLES, (
        f"{tag} cs_n low for {model.cs_low_cycles} cycles, expected {FRAME_CYCLES}"
    )

    check(dut, cs_n=1, sclk=CPOL, done=0)


@cocotb.test()
async def test_idle_after_reset(dut):
    """Outputs are in their idle state after reset, and nothing happens without start."""
    await setup(dut)
    check(dut, cs_n=1, sclk=CPOL, done=0, copi=0)
    await wait_cycles(dut, 10 * CLK_DIV)
    check(dut, cs_n=1, sclk=CPOL, done=0, copi=0)


@cocotb.test()
async def test_tx_rx_patterns(dut):
    """Each edge-case byte goes out on copi; the inverted byte comes back on cipo."""
    model = await setup(dut)
    for value in TEST_BYTES:
        await run_frame(dut, model, value, (~value) & 0xFF)


@cocotb.test()
async def test_back_to_back(dut):
    """Start again as soon as done is seen: registers must not carry over between frames."""
    model = await setup(dut)
    pairs = [(0xA5, 0x3C), (0x3C, 0xA5), (0xFF, 0x00), (0x00, 0xFF), (0x81, 0x7E)]
    for tx, peripheral in pairs:
        await run_frame(dut, model, tx, peripheral)


@cocotb.test()
async def test_start_ignored_mid_transfer(dut):
    """A start pulse (with different tx_data) during a transfer must not restart or corrupt it."""
    model = await setup(dut)
    await run_frame(dut, model, 0xA5, 0x3C, poke_start_at=3 * CLK_DIV + 1)
    await run_frame(dut, model, 0x0F, 0xF0, poke_start_at=9 * CLK_DIV + 1)


@cocotb.test()
async def test_reset_mid_transfer(dut):
    """Reset in the middle of a frame: cs_n high, sclk idle, done low, and it works again after."""
    model = await setup(dut)

    model.tx_byte = 0xA5
    dut.tx_data.value = 0xFF
    dut.start.value = 1
    await wait_cycles(dut, 1)
    dut.start.value = 0
    await wait_cycles(dut, 6 * CLK_DIV + 2)      # roughly 3 bits in
    assert int(dut.cs_n.value) == 0, "transfer should be in progress before reset"

    dut.rst.value = 1
    await wait_cycles(dut, 2)
    dut.rst.value = 0
    check(dut, cs_n=1, sclk=CPOL, done=0, copi=0)

    await wait_cycles(dut, 3 * CLK_DIV)
    check(dut, cs_n=1, sclk=CPOL, done=0)        # no leftover transfer

    await run_frame(dut, model, 0x3C, 0xC3)      # and the controller still works