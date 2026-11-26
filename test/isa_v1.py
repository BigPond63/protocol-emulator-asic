
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

IN_SRC_PINS = 0b000
IN_SRC_X = 0b001 
IN_SRC_Y = 0b010 
IN_SRC_NULL = 0b011 
IN_SRC_OSR = 0b101 
# TODO -> 100, 110 and 111 left out for now

MSB_FIRST = 0
LSB_FIRST = 1

def JMP(cond, addr):
    return (OP_JMP << 13) | (cond << 5) | addr # Address between 0 and 31 inclusive

def SET(dst, value):
    return (OP_SET << 13) | (dst << 5) | value # Value between 0 and 31 inclusive

def WAIT(src, polarity, index):
    return (OP_WAIT << 13) | (src << 7) | (polarity << 6) | index

def IN(src, count, order):
    assert (1 <= count <= 8), f"Count not between 1 and 8, got: {count}"
    assert (0 <= src <= 7), f"Soure not between 0 and 7, got {src}"
    assert (0 <= order <= 1), f"Order not 0 or 1, got {order}"
    return (OP_IO << 13) | (0 << 7) | ((count & 0b111) << 4) | (src << 1) | order # mask for 8 -> 0b000

def PUSH():
    return (OP_PUSH_PULL << 13) | (0 << 7)

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

    got = int(dut.user_project.sm.X.value)
    assert got == 7, \
        f"Scratch register loading failure, expected: 7, got {got}"

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

async def check_dec_loop(dut, set_dest, jmp_cond, reg_name):
    await setup(dut)
    await load_instructional_memory(dut, [
        SET(set_dest, value=3),
        JMP(jmp_cond, addr=1),
        SET(SET_PINS_OUT, value=0x1F),
        JMP(JMP_ALWAYS, addr=3),
    ])
    await ClockCycles(dut.clk, 5)
    await FallingEdge(dut.clk)
    reg = int(getattr(dut.user_project.sm, reg_name).value)
    assert int(dut.user_project.sm.pc.value) == 2
    assert reg == 0xFFFFFFFF, f"{reg_name} should wrap to 0xFFFFFFFF, got {reg}"

    assert int(dut.uio_out.value) == 0, "SET PINS ran too early"

    await RisingEdge(dut.clk)   # SET PINS executes
    await FallingEdge(dut.clk)
    assert int(dut.uio_out.value) == 0x1F, "SET PINS didn't run after loop exit"

@cocotb.test()
async def test_jmp_x_dec_loop(dut):
    await check_dec_loop(dut, SET_X, JMP_XNEZD, "X")

@cocotb.test()
async def test_jmp_y_dec_loop(dut):
    await check_dec_loop(dut, SET_Y, JMP_YNEZD, "Y")


async def check_jmp(dut, prep, cond, taken, pins=0):
    """Run `prep` instructions, then one JMP. Check whether it jumped."""
    target = 20
    program = prep + [JMP(cond, addr=target)]

    await setup(dut)
    dut.uio_in.value = pins
    await load_instructional_memory(dut, program)

    await ClockCycles(dut.clk, len(program))   # one edge per instruction
    await FallingEdge(dut.clk)

    # Taken: If the jmp condition was true, pc jumps to the target
    # Not taken: JMP still runs but falls through to the next address,
    # which is just past the end of the program (len(program))
    expected = target if taken else len(program)
    got = int(dut.user_project.sm.pc.value)
    assert got == expected, f"cond={cond:03b} taken={taken}: pc={got}, expected {expected}"

@cocotb.test()
async def test_jmp_always(dut):
    await check_jmp(dut, [], JMP_ALWAYS, taken=True)

@cocotb.test()
async def test_jmp_yez_taken(dut):
    await check_jmp(dut, [], JMP_YEZ, taken=True)            # Y = 0 after reset

@cocotb.test()
async def test_jmp_yez_not_taken(dut):
    await check_jmp(dut, [SET(SET_Y, 1)], JMP_YEZ, taken=False)

@cocotb.test()
async def test_jmp_xney_taken(dut):
    await check_jmp(dut, [SET(SET_X, 3), SET(SET_Y, 4)], JMP_XNEY, taken=True)

@cocotb.test()
async def test_jmp_xney_not_taken(dut):
    await check_jmp(dut, [SET(SET_X, 3), SET(SET_Y, 3)], JMP_XNEY, taken=False)

@cocotb.test()
async def test_jmp_pin_taken(dut):
    await check_jmp(dut, [], JMP_PINH, taken=True, pins=0b0000_0001)

@cocotb.test()
async def test_jmp_pin_not_taken(dut):
    await check_jmp(dut, [], JMP_PINH, taken=False, pins=0)
    

@cocotb.test()
async def test_in_opcode(dut):
    
    got = IN(IN_SRC_PINS, 1, MSB_FIRST)
    assert got == 0b001_00000_0_001_000_0, \
        f"'In' instruction encoding incorrect, expected: 0b001_00000_0_001_000_0, got {got:016b}"

    got = IN(IN_SRC_PINS, 8, MSB_FIRST)
    assert got == 0b001_00000_0_000_000_0, \
        f"'In' instruction encoding incorrect, expected: 0b001_00000_0_000_000_0, got {got:016b}"
    
    got = IN(IN_SRC_X, 8, LSB_FIRST)
    assert got == 0b001_00000_0_000_001_1, \
        f"'In' instruction encoding incorrect, expected: 0b001_00000_0_000_001_1, got {got:016b}"

@cocotb.test()
async def test_isr_shift_one(dut):
    await setup(dut)
    dut.uio_in.value = 0b1 

    await load_instructional_memory(dut, [
        IN(IN_SRC_PINS, 1, MSB_FIRST)
    ])
    # Run IN
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    # Check that in has shifted into the isr
    got = int(dut.user_project.sm.isr.value)
    assert got == 1, \
        f"ISR shifted value is not 1, got: {got}"
    got = int(dut.user_project.sm.isr_cnt.value)
    assert got == 1, \
    f"ISR count value is not 1, got: {got}"

@cocotb.test()
async def test_push_0xFF(dut):
    await setup(dut)
    dut.uio_in.value = 0b1 

    await load_instructional_memory(dut, 
        [IN(IN_SRC_PINS, count=1, order=MSB_FIRST)]*8 + 
        [PUSH(), JMP(JMP_ALWAYS, addr=9)]
    )

    # Execute the IN instructions, giving ISR value of 0xFF and isr_cnt 8
    await ClockCycles(dut.clk, num_cycles=8)
    await FallingEdge(dut.clk)

    got = int(dut.user_project.sm.isr.value)
    assert got == 255, f"After 8 INs: isr expected 0xFF, got {got:#x}"
    got = int(dut.user_project.sm.isr_cnt.value)
    assert got == 8, f"After 8 INs: isr_cnt expected 8, got {got}"

    # Execute PUSH, clearing isr and isr_cnt
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    got = int(dut.user_project.sm.isr.value)
    assert got == 0, f"After PUSH: isr should clear to 0, got {got:#x}"
    got = int(dut.user_project.sm.isr_cnt.value)
    assert got == 0, f"After PUSH: isr_cnt should clear to 0, got {got}"

    got = int(dut.user_project.sm.rx_fifo.rd_data.value) 
    assert got == 0xFF, \
        f"After PUSH: RX FIFO head expected 0xFF, got {got:#x}"


@cocotb.test()
async def test_push_0xA5(dut): #0b1010_0101

    test_value = 0b1010_0101
    await setup(dut)
    

    await load_instructional_memory(dut, 
        [IN(IN_SRC_PINS, count=1, order=MSB_FIRST)]*8 + 
        [PUSH(), JMP(JMP_ALWAYS, addr=9)]
    )

    # Execute the IN instructions, giving ISR value of 0xA5 and isr_cnt 8
    for i in range(7, -1, -1):
        dut.uio_in.value = (test_value >> i) & 1 # mask to get the bit at position 0 
        await RisingEdge(dut.clk)
        await FallingEdge(dut.clk)


    got = int(dut.user_project.sm.isr.value)
    assert got == 0xA5, f"After 8 INs: isr expected 0xA5, got {got:#x}"
    got = int(dut.user_project.sm.isr_cnt.value)
    assert got == 8, f"After 8 INs: isr_cnt expected 8, got {got:#x}"

    # Execute PUSH, clearing isr and isr_cnt
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    got = int(dut.user_project.sm.isr.value)
    assert got == 0, f"After PUSH: isr should clear to 0, got {got:#x}"
    got = int(dut.user_project.sm.isr_cnt.value)
    assert got == 0, f"After PUSH: isr_cnt should clear to 0, got {got:#x}"

    got = int(dut.user_project.sm.rx_fifo.rd_data.value) 
    assert got == 0xA5, \
        f"After PUSH: RX FIFO head expected 0xA5, got {got:#x}"

@cocotb.test()
async def test_pins_in_count_three(dut):
    await setup(dut)

    await load_instructional_memory(dut, [
        IN(IN_SRC_PINS, count=3, order=MSB_FIRST),
        JMP(JMP_ALWAYS, addr=1)
    ])

    # Mask should also make the shifted value 0b0000_0101
    dut.uio_in.value = 0b0000_1101 

    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    got_isr = int(dut.user_project.sm.isr.value)
    assert got_isr == 5, f"isr value incorrect, expected: 5, got {got_isr:08b}"

    got_isr_cnt = int(dut.user_project.sm.isr_cnt.value)
    assert got_isr_cnt == 3, f"isr_cnt value incorrect, expected: 3, got {got_isr_cnt:08b}"

@cocotb.test()
async def test_pins_in_lsb(dut):
    await setup(dut)

    await load_instructional_memory(dut, [
        IN(IN_SRC_PINS, count=8, order=LSB_FIRST),
        JMP(JMP_ALWAYS, addr=1)
    ])

    dut.uio_in.value = 0b1010_0101 
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    got_isr = int(dut.user_project.sm.isr.value)
    assert got_isr == 0xA500_0000, f"isr value incorrect, expected: 0xA500_0000, got {got_isr:#010x}"

    got_isr_cnt = int(dut.user_project.sm.isr_cnt.value)
    assert got_isr_cnt == 8, f"isr_cnt value incorrect, expected: 8, got {got_isr_cnt:08b}"

async def check_in_pins(dut, count, order, pin_values, expected_isr):
    """Run one IN per entry in pin_values, then check isr and isr_cnt."""
    await setup(dut)
    n = len(pin_values)
    await load_instructional_memory(dut,
        [IN(IN_SRC_PINS, count, order)] * n + [JMP(JMP_ALWAYS, addr=n)]
    )

    for v in pin_values:
        dut.uio_in.value = v
        await RisingEdge(dut.clk)
        await FallingEdge(dut.clk)

    got = int(dut.user_project.sm.isr.value)
    assert got == expected_isr, f"isr: expected {expected_isr:#010x}, got {got:#010x}"
    got = int(dut.user_project.sm.isr_cnt.value)
    assert got == count * n, f"isr_cnt: expected {count * n}, got {got}"

@cocotb.test()
async def test_in_serial_lsb(dut):
    bits = [(0xA5 >> i) & 1 for i in range(8)] # Place bits into a list 1010_0101
    await check_in_pins(dut, 1, LSB_FIRST, bits, 0xA500_0000)

@cocotb.test()
async def test_in_parallel_lsb(dut):
    await check_in_pins(dut, 8, LSB_FIRST, [0xA5], 0xA500_0000)

@cocotb.test()
async def test_in_count3_mask(dut):
    await check_in_pins(dut, 3, MSB_FIRST, [0b1101], 0b101)