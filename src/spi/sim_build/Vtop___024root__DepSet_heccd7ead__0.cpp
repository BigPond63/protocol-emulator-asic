// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vtop.h for the primary calling header

#include "Vtop__pch.h"
#include "Vtop___024root.h"

void Vtop___024root___ico_sequent__TOP__0(Vtop___024root* vlSelf);

void Vtop___024root___eval_ico(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_ico\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VicoTriggered.word(0U))) {
        Vtop___024root___ico_sequent__TOP__0(vlSelf);
    }
}

VL_INLINE_OPT void Vtop___024root___ico_sequent__TOP__0(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___ico_sequent__TOP__0\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.spi_controller__DOT__clk = vlSelfRef.clk;
    vlSelfRef.spi_controller__DOT__rst = vlSelfRef.rst;
    vlSelfRef.spi_controller__DOT__start = vlSelfRef.start;
    vlSelfRef.spi_controller__DOT__tx_data = vlSelfRef.tx_data;
    vlSelfRef.spi_controller__DOT__cipo = vlSelfRef.cipo;
    vlSelfRef.rx_data = vlSelfRef.spi_controller__DOT__rx_data;
    vlSelfRef.copi = vlSelfRef.spi_controller__DOT__copi;
    vlSelfRef.cs_n = vlSelfRef.spi_controller__DOT__cs_n;
    vlSelfRef.sclk = vlSelfRef.spi_controller__DOT__sclk;
    vlSelfRef.done = vlSelfRef.spi_controller__DOT__done;
}

void Vtop___024root___eval_triggers__ico(Vtop___024root* vlSelf);

bool Vtop___024root___eval_phase__ico(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__ico\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VicoExecute;
    // Body
    Vtop___024root___eval_triggers__ico(vlSelf);
    __VicoExecute = vlSelfRef.__VicoTriggered.any();
    if (__VicoExecute) {
        Vtop___024root___eval_ico(vlSelf);
    }
    return (__VicoExecute);
}

void Vtop___024root___eval_act(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_act\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

void Vtop___024root___nba_sequent__TOP__0(Vtop___024root* vlSelf);

void Vtop___024root___eval_nba(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_nba\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VnbaTriggered.word(0U))) {
        Vtop___024root___nba_sequent__TOP__0(vlSelf);
    }
}

VL_INLINE_OPT void Vtop___024root___nba_sequent__TOP__0(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___nba_sequent__TOP__0\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*1:0*/ __Vdly__spi_controller__DOT__state;
    __Vdly__spi_controller__DOT__state = 0;
    CData/*0:0*/ __Vdly__spi_controller__DOT__sclk;
    __Vdly__spi_controller__DOT__sclk = 0;
    CData/*2:0*/ __Vdly__spi_controller__DOT__bit_cnt;
    __Vdly__spi_controller__DOT__bit_cnt = 0;
    CData/*1:0*/ __Vdly__spi_controller__DOT__div_cnt;
    __Vdly__spi_controller__DOT__div_cnt = 0;
    CData/*7:0*/ __Vdly__spi_controller__DOT__rx_shift;
    __Vdly__spi_controller__DOT__rx_shift = 0;
    CData/*7:0*/ __Vdly__spi_controller__DOT__tx_shift;
    __Vdly__spi_controller__DOT__tx_shift = 0;
    // Body
    __Vdly__spi_controller__DOT__state = vlSelfRef.spi_controller__DOT__state;
    __Vdly__spi_controller__DOT__bit_cnt = vlSelfRef.spi_controller__DOT__bit_cnt;
    __Vdly__spi_controller__DOT__div_cnt = vlSelfRef.spi_controller__DOT__div_cnt;
    __Vdly__spi_controller__DOT__rx_shift = vlSelfRef.spi_controller__DOT__rx_shift;
    __Vdly__spi_controller__DOT__tx_shift = vlSelfRef.spi_controller__DOT__tx_shift;
    __Vdly__spi_controller__DOT__sclk = vlSelfRef.spi_controller__DOT__sclk;
    if (vlSelfRef.rst) {
        __Vdly__spi_controller__DOT__state = 0U;
        __Vdly__spi_controller__DOT__sclk = 1U;
        vlSelfRef.spi_controller__DOT__cs_n = 1U;
        vlSelfRef.spi_controller__DOT__copi = 0U;
        vlSelfRef.spi_controller__DOT__done = 0U;
        vlSelfRef.spi_controller__DOT__rx_data = 0U;
        __Vdly__spi_controller__DOT__bit_cnt = 0U;
        __Vdly__spi_controller__DOT__div_cnt = 0U;
        __Vdly__spi_controller__DOT__rx_shift = 0U;
        __Vdly__spi_controller__DOT__tx_shift = 0U;
    } else if ((0U == (IData)(vlSelfRef.spi_controller__DOT__state))) {
        __Vdly__spi_controller__DOT__sclk = 1U;
        vlSelfRef.spi_controller__DOT__cs_n = 1U;
        vlSelfRef.spi_controller__DOT__done = 0U;
        if (vlSelfRef.start) {
            __Vdly__spi_controller__DOT__tx_shift = vlSelfRef.tx_data;
            __Vdly__spi_controller__DOT__rx_shift = 0U;
            __Vdly__spi_controller__DOT__state = 1U;
            vlSelfRef.spi_controller__DOT__cs_n = 0U;
            __Vdly__spi_controller__DOT__bit_cnt = 0U;
            __Vdly__spi_controller__DOT__div_cnt = 0U;
        }
    } else if ((1U == (IData)(vlSelfRef.spi_controller__DOT__state))) {
        if ((3U == (IData)(vlSelfRef.spi_controller__DOT__div_cnt))) {
            __Vdly__spi_controller__DOT__sclk = (1U 
                                                 & (~ (IData)(vlSelfRef.spi_controller__DOT__sclk)));
            __Vdly__spi_controller__DOT__div_cnt = 0U;
            if (vlSelfRef.spi_controller__DOT__sclk) {
                vlSelfRef.spi_controller__DOT__copi 
                    = (1U & ((IData)(vlSelfRef.spi_controller__DOT__tx_shift) 
                             >> 7U));
                __Vdly__spi_controller__DOT__tx_shift 
                    = (0xfeU & ((IData)(vlSelfRef.spi_controller__DOT__tx_shift) 
                                << 1U));
            } else {
                __Vdly__spi_controller__DOT__rx_shift 
                    = ((0xfeU & ((IData)(vlSelfRef.spi_controller__DOT__rx_shift) 
                                 << 1U)) | (IData)(vlSelfRef.cipo));
                __Vdly__spi_controller__DOT__bit_cnt 
                    = (7U & ((IData)(1U) + (IData)(vlSelfRef.spi_controller__DOT__bit_cnt)));
                if ((7U == (IData)(vlSelfRef.spi_controller__DOT__bit_cnt))) {
                    __Vdly__spi_controller__DOT__state = 2U;
                }
            }
        } else {
            __Vdly__spi_controller__DOT__div_cnt = 
                (3U & ((IData)(1U) + (IData)(vlSelfRef.spi_controller__DOT__div_cnt)));
        }
    } else if ((2U == (IData)(vlSelfRef.spi_controller__DOT__state))) {
        vlSelfRef.spi_controller__DOT__cs_n = 1U;
        vlSelfRef.spi_controller__DOT__done = 1U;
        vlSelfRef.spi_controller__DOT__copi = 0U;
        vlSelfRef.spi_controller__DOT__rx_data = vlSelfRef.spi_controller__DOT__rx_shift;
        __Vdly__spi_controller__DOT__state = 0U;
    } else {
        __Vdly__spi_controller__DOT__state = 0U;
    }
    vlSelfRef.spi_controller__DOT__state = __Vdly__spi_controller__DOT__state;
    vlSelfRef.spi_controller__DOT__bit_cnt = __Vdly__spi_controller__DOT__bit_cnt;
    vlSelfRef.spi_controller__DOT__div_cnt = __Vdly__spi_controller__DOT__div_cnt;
    vlSelfRef.spi_controller__DOT__rx_shift = __Vdly__spi_controller__DOT__rx_shift;
    vlSelfRef.spi_controller__DOT__tx_shift = __Vdly__spi_controller__DOT__tx_shift;
    vlSelfRef.spi_controller__DOT__sclk = __Vdly__spi_controller__DOT__sclk;
    vlSelfRef.sclk = vlSelfRef.spi_controller__DOT__sclk;
    vlSelfRef.cs_n = vlSelfRef.spi_controller__DOT__cs_n;
    vlSelfRef.copi = vlSelfRef.spi_controller__DOT__copi;
    vlSelfRef.done = vlSelfRef.spi_controller__DOT__done;
    vlSelfRef.rx_data = vlSelfRef.spi_controller__DOT__rx_data;
}

void Vtop___024root___eval_triggers__act(Vtop___024root* vlSelf);

bool Vtop___024root___eval_phase__act(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__act\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    VlTriggerVec<1> __VpreTriggered;
    CData/*0:0*/ __VactExecute;
    // Body
    Vtop___024root___eval_triggers__act(vlSelf);
    __VactExecute = vlSelfRef.__VactTriggered.any();
    if (__VactExecute) {
        __VpreTriggered.andNot(vlSelfRef.__VactTriggered, vlSelfRef.__VnbaTriggered);
        vlSelfRef.__VnbaTriggered.thisOr(vlSelfRef.__VactTriggered);
        Vtop___024root___eval_act(vlSelf);
    }
    return (__VactExecute);
}

bool Vtop___024root___eval_phase__nba(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_phase__nba\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = vlSelfRef.__VnbaTriggered.any();
    if (__VnbaExecute) {
        Vtop___024root___eval_nba(vlSelf);
        vlSelfRef.__VnbaTriggered.clear();
    }
    return (__VnbaExecute);
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__ico(Vtop___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__nba(Vtop___024root* vlSelf);
#endif  // VL_DEBUG
#ifdef VL_DEBUG
VL_ATTR_COLD void Vtop___024root___dump_triggers__act(Vtop___024root* vlSelf);
#endif  // VL_DEBUG

void Vtop___024root___eval(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    IData/*31:0*/ __VicoIterCount;
    CData/*0:0*/ __VicoContinue;
    IData/*31:0*/ __VnbaIterCount;
    CData/*0:0*/ __VnbaContinue;
    // Body
    __VicoIterCount = 0U;
    vlSelfRef.__VicoFirstIteration = 1U;
    __VicoContinue = 1U;
    while (__VicoContinue) {
        if (VL_UNLIKELY(((0x64U < __VicoIterCount)))) {
#ifdef VL_DEBUG
            Vtop___024root___dump_triggers__ico(vlSelf);
#endif
            VL_FATAL_MT("/home/BigPond63/protocol-emulator-asic/src/spi/spi_controller.sv", 4, "", "Input combinational region did not converge.");
        }
        __VicoIterCount = ((IData)(1U) + __VicoIterCount);
        __VicoContinue = 0U;
        if (Vtop___024root___eval_phase__ico(vlSelf)) {
            __VicoContinue = 1U;
        }
        vlSelfRef.__VicoFirstIteration = 0U;
    }
    __VnbaIterCount = 0U;
    __VnbaContinue = 1U;
    while (__VnbaContinue) {
        if (VL_UNLIKELY(((0x64U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vtop___024root___dump_triggers__nba(vlSelf);
#endif
            VL_FATAL_MT("/home/BigPond63/protocol-emulator-asic/src/spi/spi_controller.sv", 4, "", "NBA region did not converge.");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        __VnbaContinue = 0U;
        vlSelfRef.__VactIterCount = 0U;
        vlSelfRef.__VactContinue = 1U;
        while (vlSelfRef.__VactContinue) {
            if (VL_UNLIKELY(((0x64U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                Vtop___024root___dump_triggers__act(vlSelf);
#endif
                VL_FATAL_MT("/home/BigPond63/protocol-emulator-asic/src/spi/spi_controller.sv", 4, "", "Active region did not converge.");
            }
            vlSelfRef.__VactIterCount = ((IData)(1U) 
                                         + vlSelfRef.__VactIterCount);
            vlSelfRef.__VactContinue = 0U;
            if (Vtop___024root___eval_phase__act(vlSelf)) {
                vlSelfRef.__VactContinue = 1U;
            }
        }
        if (Vtop___024root___eval_phase__nba(vlSelf)) {
            __VnbaContinue = 1U;
        }
    }
}

#ifdef VL_DEBUG
void Vtop___024root___eval_debug_assertions(Vtop___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vtop___024root___eval_debug_assertions\n"); );
    Vtop__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY(((vlSelfRef.clk & 0xfeU)))) {
        Verilated::overWidthError("clk");}
    if (VL_UNLIKELY(((vlSelfRef.rst & 0xfeU)))) {
        Verilated::overWidthError("rst");}
    if (VL_UNLIKELY(((vlSelfRef.start & 0xfeU)))) {
        Verilated::overWidthError("start");}
    if (VL_UNLIKELY(((vlSelfRef.cipo & 0xfeU)))) {
        Verilated::overWidthError("cipo");}
}
#endif  // VL_DEBUG
