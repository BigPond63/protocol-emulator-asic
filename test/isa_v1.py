
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, RisingEdge

import random

RESET_CYCLES = 5
CLOCK_PERIOD_NS = 10
INSTRUCTIONAL_MEMORY_DEPTH = 32
INSTRUCTIONAL_MEMORY_WORD_SIZE = 16
SEED = 7

random.seed(SEED)

OP_PUSH_PULL = 0b000
OP_IO = 0b001 
OP_SET = 0b010 
OP_WAIT = 0b011 
OP_JMP = 0b100 
OP_MOV = 0b101 
OP_IRQ = 0b110 

JMP_ALWAYS = 0b000
JMP_XEZ = 0b001 
JMP_XNEZD = 0b010 
JMP_YEZ = 0b011 
JMP_YNEZD = 0b100 
JMP_XNEY = 0b101 
JMP_PINH = 0b110 
JMP_OSRNE = 0b111 

SET_PINS_OUT = 0b000 
SET_PINDIRS = 0b001 
SET_X = 0b010 
SET_Y = 0b011 

PIN_SOURCE = 0 

def JMP(cond, addr):
    return (OP_JMP << 13) | (cond << 5) | addr # Address between 0 and 31 inclusive

def SET(dst, value):
    return (OP_SET << 13) | (dst << 5) | value # Value between 0 and 31 inclusive

def WAIT(src, polarity, index):
    return (OP_WAIT << 13) | (src << 7) | (polarity << 6) | index


async def setup(dut, reset_cycles = RESET_CYCLES):
    Clock(dut.clk, CLOCK_PERIOD_NS, unit="ns").start(start_high=False)

    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.ena.value = 1
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, reset_cycles)
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1


async def load_instruction(dut, words:list[int]):
    for instr in words:
        for i in range(15, -1, -1): # MSB first
            dut.ui_in[0].value = 1 # enable signal on 
            dut.ui_in[1].value = (instr >> i) & 0b1 # data bit shifted in 
            await RisingEdge(dut.clk)
    dut.ui_in[0].value = 0


async def load_instructional_memory(dut, instr_list =[0xA5C3]):
    
    await load_instruction(dut, instr_list)
    await FallingEdge(dut.clk)

    for addr, instruction in enumerate(instr_list):
        got = int(dut.user_project.sm.instruc_mem[addr].value)
        assert got == instruction, f"instruc_mem[{addr}]: expected {instruction:#06x}, got {got:#06x}"

@cocotb.test()
async def test_load_random(dut):
    await setup(dut)
    rand_instr_list = []
    for i in range(INSTRUCTIONAL_MEMORY_DEPTH):
        rand_instr_list.append(random.getrandbits(INSTRUCTIONAL_MEMORY_WORD_SIZE))
    
    await load_instructional_memory(dut, rand_instr_list)


@cocotb.test()
async def test_set_x_seven(dut):
    await setup(dut)

    set_x_seven = 0b010_00000_010_00111
    await load_instructional_memory(dut, [set_x_seven])

    # Execute instruction, setting scratch register X to 7
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    got = dut.user_project.sm.X.value
    assert got == 7, \
        f"Scratch register loading failure, expected 7:, got {dut.user_project.sm.X.value}"

@cocotb.test()
async def test_jmp_xez(dut):
    await setup(dut)
    pc_jmp_to = 6

    # Encode instruction
    jmp_xez = JMP(JMP_XEZ, pc_jmp_to)

    await load_instructional_memory(dut, [jmp_xez])

    # Execute instruction
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    
    got_pc_ptr = int(dut.user_project.sm.pc.value)
    assert got_pc_ptr == pc_jmp_to, \
        f"Jump instruction xez failed, got: {got_pc_ptr:d}, expected: {pc_jmp_to:d}"


@cocotb.test()
async def test_jmp_xez_not_taken(dut):
    await setup(dut)

    await load_instructional_memory(dut, [
        SET(SET_X, 1),        # 0: make X non-zero
        JMP(JMP_XEZ, 6),      # 1: should NOT jump
    ])

    await RisingEdge(dut.clk)   # SET X executes
    await RisingEdge(dut.clk)   # JMP executes
    await FallingEdge(dut.clk)

    got_pc = int(dut.user_project.sm.pc.value)
    assert got_pc == 2, f"JMP xez jumped with X=1: pc={got_pc}, expected 2"


@cocotb.test()
async def test_wait(dut):
    await setup(dut)
    dut.uio_in.value = 0

    await load_instructional_memory(dut, [
        WAIT(PIN_SOURCE, polarity=1, index=2),
        SET(SET_X, 5)
    ])

    # Stall: pin 2 low, so WAIT holds
    await ClockCycles(dut.clk, num_cycles=5)
    await FallingEdge(dut.clk)
    assert int(dut.user_project.sm.pc.value) == 0, "WAIT didn't stall"
    assert int(dut.user_project.sm.X.value) == 0, "SET ran while WAIT should be stalling"

    # Release: raise pin 2 on a falling edge
    dut.uio_in.value = 0b0000_0100
    await RisingEdge(dut.clk)          # WAIT sees pin high, completes
    await FallingEdge(dut.clk)
    assert int(dut.user_project.sm.pc.value) == 1, "WAIT didn't release on the first edge"

    await RisingEdge(dut.clk)          # SET X executes
    await FallingEdge(dut.clk)
    assert int(dut.user_project.sm.X.value) == 5