# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

# Makefile

# The simulator we want to run our tests with.
SIM = verilator # or icarus (doesn't work here due to .sv)

# The top-level language of the design (verilog or vhdl).
TOPLEVEL_LANG = verilog

# List of Verilog source files.
VERILOG_SOURCES += $(PWD)/spi_controller.sv

# The name of the toplevel module/entity in your design.
COCOTB_TOPLEVEL = spi_controller

# The Python modules which contain your testcases.
# The current directory is included in the Python path,
# so you can just specify the module name without the .py extension.
COCOTB_TEST_MODULES = spi_cont_tests

# Enable waveform generation.
WAVES = 1

SPI_MODE ?= 0
SPI_CLK_DIV ?= 4
COMPILE_ARGS += -GMODE=$(SPI_MODE) -GCLK_DIV=$(SPI_CLK_DIV)
export SPI_MODE SPI_CLK_DIV

# Includes cocotb's Makefiles which define the build and simulation flows for each supported simulator.
# This must be included *after* all of the variables above are defined.
include $(shell cocotb-config --makefiles)/Makefile.sim

