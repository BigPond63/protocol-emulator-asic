// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vtop__pch.h"
#include "Vtop.h"
#include "Vtop___024root.h"

// FUNCTIONS
Vtop__Syms::~Vtop__Syms()
{

    // Tear down scope hierarchy
    __Vhier.remove(0, &__Vscope_spi_controller);

}

Vtop__Syms::Vtop__Syms(VerilatedContext* contextp, const char* namep, Vtop* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup module instances
    , TOP{this, namep}
{
        // Check resources
        Verilated::stackCheck(37);
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-9);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    __Vscope_TOP.configure(this, name(), "TOP", "TOP", "<null>", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_spi_controller.configure(this, name(), "spi_controller", "spi_controller", "spi_controller", -9, VerilatedScope::SCOPE_MODULE);

    // Set up scope hierarchy
    __Vhier.add(0, &__Vscope_spi_controller);

    // Setup export functions
    for (int __Vfinal = 0; __Vfinal < 2; ++__Vfinal) {
        __Vscope_TOP.varInsert(__Vfinal,"cipo", &(TOP.cipo), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"clk", &(TOP.clk), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"copi", &(TOP.copi), false, VLVT_UINT8,VLVD_OUT|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"cs_n", &(TOP.cs_n), false, VLVT_UINT8,VLVD_OUT|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"done", &(TOP.done), false, VLVT_UINT8,VLVD_OUT|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"rst", &(TOP.rst), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"rx_data", &(TOP.rx_data), false, VLVT_UINT8,VLVD_OUT|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_TOP.varInsert(__Vfinal,"sclk", &(TOP.sclk), false, VLVT_UINT8,VLVD_OUT|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"start", &(TOP.start), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"tx_data", &(TOP.tx_data), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_spi_controller.varInsert(__Vfinal,"CLK_DIV", const_cast<void*>(static_cast<const void*>(&(TOP.spi_controller__DOT__CLK_DIV))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY,0,1 ,31,0);
        __Vscope_spi_controller.varInsert(__Vfinal,"CPHA", const_cast<void*>(static_cast<const void*>(&(TOP.spi_controller__DOT__CPHA))), true, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY,0,0);
        __Vscope_spi_controller.varInsert(__Vfinal,"CPOL", const_cast<void*>(static_cast<const void*>(&(TOP.spi_controller__DOT__CPOL))), true, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY,0,0);
        __Vscope_spi_controller.varInsert(__Vfinal,"DIV_MAX", const_cast<void*>(static_cast<const void*>(&(TOP.spi_controller__DOT__DIV_MAX))), true, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,1,0);
        __Vscope_spi_controller.varInsert(__Vfinal,"DIV_W", const_cast<void*>(static_cast<const void*>(&(TOP.spi_controller__DOT__DIV_W))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY,0,1 ,31,0);
        __Vscope_spi_controller.varInsert(__Vfinal,"MODE", const_cast<void*>(static_cast<const void*>(&(TOP.spi_controller__DOT__MODE))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW|VLVF_DPI_CLAY,0,1 ,31,0);
        __Vscope_spi_controller.varInsert(__Vfinal,"bit_cnt", &(TOP.spi_controller__DOT__bit_cnt), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,2,0);
        __Vscope_spi_controller.varInsert(__Vfinal,"cipo", &(TOP.spi_controller__DOT__cipo), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_spi_controller.varInsert(__Vfinal,"clk", &(TOP.spi_controller__DOT__clk), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_spi_controller.varInsert(__Vfinal,"copi", &(TOP.spi_controller__DOT__copi), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_spi_controller.varInsert(__Vfinal,"cs_n", &(TOP.spi_controller__DOT__cs_n), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_spi_controller.varInsert(__Vfinal,"div_cnt", &(TOP.spi_controller__DOT__div_cnt), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,1,0);
        __Vscope_spi_controller.varInsert(__Vfinal,"done", &(TOP.spi_controller__DOT__done), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_spi_controller.varInsert(__Vfinal,"rst", &(TOP.spi_controller__DOT__rst), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_spi_controller.varInsert(__Vfinal,"rx_data", &(TOP.spi_controller__DOT__rx_data), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_spi_controller.varInsert(__Vfinal,"rx_shift", &(TOP.spi_controller__DOT__rx_shift), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_spi_controller.varInsert(__Vfinal,"sclk", &(TOP.spi_controller__DOT__sclk), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_spi_controller.varInsert(__Vfinal,"start", &(TOP.spi_controller__DOT__start), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,0);
        __Vscope_spi_controller.varInsert(__Vfinal,"state", &(TOP.spi_controller__DOT__state), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,1,0);
        __Vscope_spi_controller.varInsert(__Vfinal,"tx_data", &(TOP.spi_controller__DOT__tx_data), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_spi_controller.varInsert(__Vfinal,"tx_shift", &(TOP.spi_controller__DOT__tx_shift), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
    }
}
