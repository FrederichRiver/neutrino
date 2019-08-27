#!/usr/bin/env python
# -*- coding: utf-8 -*-


class traderBase(object):
    def __init__(self, name, currency, start_date='1999-12-19'):
        self.name = name
        self.quantity = 0
        self.currency = currency
        self.freq = 3

    def _buy(self, quantity, price):
        """TODO: Docstring for _buy.

        :quantity: TODO
        :price: TODO
        :returns: TODO

        """
        if price:
            if (self.currency - quantity*price) >= 0:
                self.currency = self.currency - quantity*price
                self.quantity = self.quantity + quantity
                return 1
            else:
                return 0
        else:
            return 0

    def _sell(self, quantity, price):
        """TODO: Docstring for _sell.

        :quantity: TODO
        :price: TODO
        :returns: TODO

        """
        if self.quantity >= quantity:
            self.currency = self.currency + quantity*price
            self.quantity = self.quantity - quantity
            return 1
        else:
            return 0

    def _bankrupt(self):
        pass

    def __repr__(self):
        return f"{self.name} starts his interest with {self.currency}."


class assetBase(object):

    """Docstring for asset. """

    def __init__(self):
        """TODO: to be defined. """
        pass


class taxBase(object):

    """Docstring for taxBase. """

    def __init__(self):
        """TODO: to be defined. """
        pass


class bidBase(object):

    """Docstring for bidBase. """

    def __init__(self):
        """TODO: to be defined. """
        pass


if __name__ == "__main__":
    NewTrader = traderBase('John',10000)
    print(NewTrader)
