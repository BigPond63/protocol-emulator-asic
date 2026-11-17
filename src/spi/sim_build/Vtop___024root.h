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
    VL_IN8(tx_data,7,0);
    VL_IN8(cipo,0,0);
    VL_OUT8(rx_data,7,0);
    VL_OUT8(copi,0,0);
    VL_OUT8(cs_n,0,0);
    VL_OUT8(sclk,0,0);
    VL_OUT8(done,0,0);
    CData/*0:0*/ spi_controller__DOT__clk;
    CData/*0:0*/ spi_controller__DOT__rst;
    CData/*0:0*/ spi_controller__DOT__start;
    CData/*7:0*/ spi_controller__DOT__tx_data;
    CData/*0:0*/ spi_controller__DOT__cipo;
    CData/*7:0*/ spi_controller__DOT__rx_data;
    CData/*0:0*/ spi_controller__DOT__copi;
    CData/*0:0*/ spi_controller__DOT__cs_n;
    CData/*0:0*/ spi_controller__DOT__sclk;
    CData/*0:0*/ spi_controller__DOT__done;
    CData/*1:0*/ spi_controller__DOT__state;
    CData/*7:0*/ spi_controller__DOT__tx_shift;
    CData/*7:0*/ spi_controller__DOT__rx_shift;
    CData/*1:0*/ spi_controller__DOT__div_cnt;
    CData/*2:0*/ spi_controller__DOT__bit_cnt;
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
    static constexpr CData/*0:0*/ spi_controller__DOT__CPOL = 1U;
    static constexpr CData/*0:0*/ spi_controller__DOT__CPHA = 1U;
    static constexpr CData/*1:0*/ spi_controller__DOT__DIV_MAX = 3U;
    static constexpr IData/*31:0*/ spi_controller__DOT__MODE = 3U;
    static constexpr IData/*31:0*/ spi_controller__DOT__CLK_DIV = 4U;
    static constexpr IData/*31:0*/ spi_controller__DOT__DIV_W = 2U;

    // CONSTRUCTORS
    Vtop___024root(Vtop__Syms* symsp, const char* v__name);
    ~Vtop___024root();
    VL_UNCOPYABLE(Vtop___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
