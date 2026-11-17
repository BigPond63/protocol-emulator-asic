// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vtop.h for the primary calling header

#ifndef VERILATED_VTOP___024ROOT_H_
#define VERILATED_VTOP___024ROOT_H_  // guard

#include "verilated.h"


class Vtop__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vtop___024root final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    VL_IN8(clk,0,0);
    VL_IN8(rst,0,0);
    VL_IN8(start,0,0);
    VL_IN8(data,7,0);
    VL_OUT8(tx,0,0);
    VL_OUT8(busy,0,0);
    CData/*0:0*/ uart_tx__DOT__clk;
    CData/*0:0*/ uart_tx__DOT__rst;
    CData/*0:0*/ uart_tx__DOT__start;
    CData/*7:0*/ uart_tx__DOT__data;
    CData/*0:0*/ uart_tx__DOT__tx;
    CData/*0:0*/ uart_tx__DOT__busy;
    CData/*3:0*/ uart_tx__DOT__state;
    CData/*2:0*/ uart_tx__DOT__bit_index;
    CData/*7:0*/ uart_tx__DOT__shift_reg;
    CData/*1:0*/ uart_tx__DOT__baud_counter;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __VicoFirstIteration;
    CData/*0:0*/ __Vtrigprevexpr___TOP__clk__0;
    CData/*0:0*/ __VactContinue;
    IData/*31:0*/ __VactIterCount;
    VlTriggerVec<1> __VstlTriggered;
    VlTriggerVec<1> __VicoTriggered;
    VlTriggerVec<1> __VactTriggered;
    VlTriggerVec<1> __VnbaTriggered;

    // INTERNAL VARIABLES
    Vtop__Syms* const vlSymsp;

    // PARAMETERS
    static constexpr CData/*3:0*/ uart_tx__DOT__IDLE = 1U;
    static constexpr CData/*3:0*/ uart_tx__DOT__START = 2U;
    static constexpr CData/*3:0*/ uart_tx__DOT__DATA = 4U;
    static constexpr CData/*3:0*/ uart_tx__DOT__STOP = 8U;
    static constexpr CData/*1:0*/ uart_tx__DOT__CNT_MAX = 3U;
    static constexpr IData/*31:0*/ uart_tx__DOT__CLKS_PER_BIT = 4U;
    static constexpr IData/*31:0*/ uart_tx__DOT__CNT_W = 2U;

    // CONSTRUCTORS
    Vtop___024root(Vtop__Syms* symsp, const char* v__name);
    ~Vtop___024root();
    VL_UNCOPYABLE(Vtop___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
