// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vtop__pch.h"
#include "Vtop.h"
#include "Vtop___024root.h"

// FUNCTIONS
Vtop__Syms::~Vtop__Syms()
{

    // Tear down scope hierarchy
    __Vhier.remove(0, &__Vscope_uart_tx);

}

Vtop__Syms::Vtop__Syms(VerilatedContext* contextp, const char* namep, Vtop* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup module instances
    , TOP{this, namep}
{
        // Check resources
        Verilated::stackCheck(33);
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-9);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
    // Setup scopes
    __Vscope_TOP.configure(this, name(), "TOP", "TOP", "<null>", 0, VerilatedScope::SCOPE_OTHER);
    __Vscope_uart_tx.configure(this, name(), "uart_tx", "uart_tx", "uart_tx", -9, VerilatedScope::SCOPE_MODULE);

    // Set up scope hierarchy
    __Vhier.add(0, &__Vscope_uart_tx);

    // Setup export functions
    for (int __Vfinal = 0; __Vfinal < 2; ++__Vfinal) {
        __Vscope_TOP.varInsert(__Vfinal,"busy", &(TOP.busy), false, VLVT_UINT8,VLVD_OUT|VLVF_PUB_RW,0,1 ,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"clk", &(TOP.clk), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,1 ,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"data", &(TOP.data), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_TOP.varInsert(__Vfinal,"rst", &(TOP.rst), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,1 ,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"start", &(TOP.start), false, VLVT_UINT8,VLVD_IN|VLVF_PUB_RW,0,1 ,0,0);
        __Vscope_TOP.varInsert(__Vfinal,"tx", &(TOP.tx), false, VLVT_UINT8,VLVD_OUT|VLVF_PUB_RW,0,1 ,0,0);
        __Vscope_uart_tx.varInsert(__Vfinal,"CLKS_PER_BIT", const_cast<void*>(static_cast<const void*>(&(TOP.uart_tx__DOT__CLKS_PER_BIT))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,0,1 ,31,0);
        __Vscope_uart_tx.varInsert(__Vfinal,"CNT_MAX", const_cast<void*>(static_cast<const void*>(&(TOP.uart_tx__DOT__CNT_MAX))), true, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,1,0);
        __Vscope_uart_tx.varInsert(__Vfinal,"CNT_W", const_cast<void*>(static_cast<const void*>(&(TOP.uart_tx__DOT__CNT_W))), true, VLVT_UINT32,VLVD_NODIR|VLVF_PUB_RW,0,1 ,31,0);
        __Vscope_uart_tx.varInsert(__Vfinal,"DATA", const_cast<void*>(static_cast<const void*>(&(TOP.uart_tx__DOT__DATA))), true, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,3,0);
        __Vscope_uart_tx.varInsert(__Vfinal,"IDLE", const_cast<void*>(static_cast<const void*>(&(TOP.uart_tx__DOT__IDLE))), true, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,3,0);
        __Vscope_uart_tx.varInsert(__Vfinal,"START", const_cast<void*>(static_cast<const void*>(&(TOP.uart_tx__DOT__START))), true, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,3,0);
        __Vscope_uart_tx.varInsert(__Vfinal,"STOP", const_cast<void*>(static_cast<const void*>(&(TOP.uart_tx__DOT__STOP))), true, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,3,0);
        __Vscope_uart_tx.varInsert(__Vfinal,"baud_counter", &(TOP.uart_tx__DOT__baud_counter), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,1,0);
        __Vscope_uart_tx.varInsert(__Vfinal,"bit_index", &(TOP.uart_tx__DOT__bit_index), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,2,0);
        __Vscope_uart_tx.varInsert(__Vfinal,"busy", &(TOP.uart_tx__DOT__busy), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,0,0);
        __Vscope_uart_tx.varInsert(__Vfinal,"clk", &(TOP.uart_tx__DOT__clk), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,0,0);
        __Vscope_uart_tx.varInsert(__Vfinal,"data", &(TOP.uart_tx__DOT__data), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_uart_tx.varInsert(__Vfinal,"rst", &(TOP.uart_tx__DOT__rst), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,0,0);
        __Vscope_uart_tx.varInsert(__Vfinal,"shift_reg", &(TOP.uart_tx__DOT__shift_reg), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,7,0);
        __Vscope_uart_tx.varInsert(__Vfinal,"start", &(TOP.uart_tx__DOT__start), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,0,0);
        __Vscope_uart_tx.varInsert(__Vfinal,"state", &(TOP.uart_tx__DOT__state), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,3,0);
        __Vscope_uart_tx.varInsert(__Vfinal,"tx", &(TOP.uart_tx__DOT__tx), false, VLVT_UINT8,VLVD_NODIR|VLVF_PUB_RW,0,1 ,0,0);
    }
}
