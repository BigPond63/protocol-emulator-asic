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
    vlSelfRef.uart_tx__DOT__clk = vlSelfRef.clk;
    vlSelfRef.uart_tx__DOT__rst = vlSelfRef.rst;
    vlSelfRef.uart_tx__DOT__start = vlSelfRef.start;
    vlSelfRef.uart_tx__DOT__data = vlSelfRef.data;
    vlSelfRef.tx = vlSelfRef.uart_tx__DOT__tx;
    vlSelfRef.busy = vlSelfRef.uart_tx__DOT__busy;
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
    CData/*3:0*/ __Vdly__uart_tx__DOT__state;
    __Vdly__uart_tx__DOT__state = 0;
    CData/*1:0*/ __Vdly__uart_tx__DOT__baud_counter;
    __Vdly__uart_tx__DOT__baud_counter = 0;
    CData/*2:0*/ __Vdly__uart_tx__DOT__bit_index;
    __Vdly__uart_tx__DOT__bit_index = 0;
    CData/*7:0*/ __Vdly__uart_tx__DOT__shift_reg;
    __Vdly__uart_tx__DOT__shift_reg = 0;
    // Body
    __Vdly__uart_tx__DOT__state = vlSelfRef.uart_tx__DOT__state;
    __Vdly__uart_tx__DOT__baud_counter = vlSelfRef.uart_tx__DOT__baud_counter;
    __Vdly__uart_tx__DOT__bit_index = vlSelfRef.uart_tx__DOT__bit_index;
    __Vdly__uart_tx__DOT__shift_reg = vlSelfRef.uart_tx__DOT__shift_reg;
    if (vlSelfRef.rst) {
        __Vdly__uart_tx__DOT__state = 1U;
        vlSelfRef.uart_tx__DOT__tx = 1U;
        vlSelfRef.uart_tx__DOT__busy = 0U;
        __Vdly__uart_tx__DOT__baud_counter = 0U;
        __Vdly__uart_tx__DOT__bit_index = 0U;
    } else if ((8U & (IData)(vlSelfRef.uart_tx__DOT__state))) {
        if ((4U & (IData)(vlSelfRef.uart_tx__DOT__state))) {
            __Vdly__uart_tx__DOT__state = 1U;
        } else if ((2U & (IData)(vlSelfRef.uart_tx__DOT__state))) {
            __Vdly__uart_tx__DOT__state = 1U;
        } else if ((1U & (IData)(vlSelfRef.uart_tx__DOT__state))) {
            __Vdly__uart_tx__DOT__state = 1U;
        } else if ((3U == (IData)(vlSelfRef.uart_tx__DOT__baud_counter))) {
            __Vdly__uart_tx__DOT__state = 1U;
            vlSelfRef.uart_tx__DOT__busy = 0U;
        } else {
            __Vdly__uart_tx__DOT__baud_counter = (3U 
                                                  & ((IData)(1U) 
                                                     + (IData)(vlSelfRef.uart_tx__DOT__baud_counter)));
        }
    } else if ((4U & (IData)(vlSelfRef.uart_tx__DOT__state))) {
        if ((2U & (IData)(vlSelfRef.uart_tx__DOT__state))) {
            __Vdly__uart_tx__DOT__state = 1U;
        } else if ((1U & (IData)(vlSelfRef.uart_tx__DOT__state))) {
            __Vdly__uart_tx__DOT__state = 1U;
        } else if ((3U == (IData)(vlSelfRef.uart_tx__DOT__baud_counter))) {
            vlSelfRef.uart_tx__DOT__tx = (1U & (IData)(vlSelfRef.uart_tx__DOT__shift_reg));
            __Vdly__uart_tx__DOT__shift_reg = (0x7fU 
                                               & ((IData)(vlSelfRef.uart_tx__DOT__shift_reg) 
                                                  >> 1U));
            __Vdly__uart_tx__DOT__bit_index = (7U & 
                                               ((IData)(1U) 
                                                + (IData)(vlSelfRef.uart_tx__DOT__bit_index)));
            __Vdly__uart_tx__DOT__baud_counter = 0U;
            if ((7U == (IData)(vlSelfRef.uart_tx__DOT__bit_index))) {
                __Vdly__uart_tx__DOT__state = 8U;
                __Vdly__uart_tx__DOT__baud_counter = 0U;
                vlSelfRef.uart_tx__DOT__tx = 1U;
            }
        } else {
            __Vdly__uart_tx__DOT__baud_counter = (3U 
                                                  & ((IData)(1U) 
                                                     + (IData)(vlSelfRef.uart_tx__DOT__baud_counter)));
        }
    } else if ((2U & (IData)(vlSelfRef.uart_tx__DOT__state))) {
        if ((1U & (IData)(vlSelfRef.uart_tx__DOT__state))) {
            __Vdly__uart_tx__DOT__state = 1U;
        } else {
            vlSelfRef.uart_tx__DOT__tx = 0U;
            if ((3U == (IData)(vlSelfRef.uart_tx__DOT__baud_counter))) {
                __Vdly__uart_tx__DOT__baud_counter = 0U;
                vlSelfRef.uart_tx__DOT__tx = (1U & (IData)(vlSelfRef.uart_tx__DOT__shift_reg));
                __Vdly__uart_tx__DOT__state = 4U;
                __Vdly__uart_tx__DOT__shift_reg = (0x7fU 
                                                   & ((IData)(vlSelfRef.uart_tx__DOT__shift_reg) 
                                                      >> 1U));
            } else {
                __Vdly__uart_tx__DOT__baud_counter 
                    = (3U & ((IData)(1U) + (IData)(vlSelfRef.uart_tx__DOT__baud_counter)));
            }
        }
    } else if ((1U & (IData)(vlSelfRef.uart_tx__DOT__state))) {
        if (vlSelfRef.start) {
            __Vdly__uart_tx__DOT__shift_reg = vlSelfRef.data;
            vlSelfRef.uart_tx__DOT__busy = 1U;
            __Vdly__uart_tx__DOT__baud_counter = 0U;
            __Vdly__uart_tx__DOT__bit_index = 0U;
            __Vdly__uart_tx__DOT__state = 2U;
            vlSelfRef.uart_tx__DOT__tx = 0U;
        } else {
            vlSelfRef.uart_tx__DOT__tx = 1U;
        }
    } else {
        __Vdly__uart_tx__DOT__state = 1U;
    }
    vlSelfRef.uart_tx__DOT__state = __Vdly__uart_tx__DOT__state;
    vlSelfRef.uart_tx__DOT__baud_counter = __Vdly__uart_tx__DOT__baud_counter;
    vlSelfRef.uart_tx__DOT__bit_index = __Vdly__uart_tx__DOT__bit_index;
    vlSelfRef.uart_tx__DOT__shift_reg = __Vdly__uart_tx__DOT__shift_reg;
    vlSelfRef.tx = vlSelfRef.uart_tx__DOT__tx;
    vlSelfRef.busy = vlSelfRef.uart_tx__DOT__busy;
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
            VL_FATAL_MT("/home/BigPond63/protocol-emulator-asic/src/uart/uart.v", 1, "", "Input combinational region did not converge.");
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
            VL_FATAL_MT("/home/BigPond63/protocol-emulator-asic/src/uart/uart.v", 1, "", "NBA region did not converge.");
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
                VL_FATAL_MT("/home/BigPond63/protocol-emulator-asic/src/uart/uart.v", 1, "", "Active region did not converge.");
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
}
#endif  // VL_DEBUG
