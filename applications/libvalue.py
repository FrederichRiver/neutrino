#!/usr/bin/env python
# -*- coding: utf-8 -*-


# FCF value methord
# WACC methord
# CF methord
# increasing rate

# NOPLAT
# WACC
def expect_return_of_equity():
    return 0.0


def expect_return_of_liability():
    return 0.0


def wacc(equity, liability):
    equity_return = expect_return_of_equity()
    liability_return = expect_return_of_liability()
    wacc = equity_return * equity + liability_return * liability
    wacc = wacc/(equity + liability)
    return wacc
# RONIC
# g
# Continue Value
def continue_value(noplat, ronic, wacc, a):
    cv = noplat*(1-g/ronic)/(wacc-g)
    return cv
