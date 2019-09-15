#!/usr/bin/env python
# -*- coding: utf-8 -*-


class traderBase(object):
    def __init__(self, name, currency, start_date='1999-12-19'):
        self.name = name
        self.quantity = 0
        self.currency = currency
        self.assetgroup = assetGroup()

    def buy(self, asset):
        if asset.unit_cost:
            if (self.currency - asset.quantity*asset.unit_cost) >= 0:
                self.currency = self.currency - asset.settle()
                print(f"{self.name} "
                      f"buys {asset.quantity} assets "
                      f"in price {asset.unit_cost}\n")
                self.assetgroup.append(asset)
                self.settle()
                return 1
            else:
                print("Trading failed. Currency is not enough.\n")
                return 0
        else:
            print("Trading failed.")
            return 0

    def settle(self):
        print(f"Currency: {self.currency}")

    def sell(self, sell_asset, quantity, price):
        """TODO: Docstring for _sell.

        :quantity: TODO
        :price: TODO
        :returns: TODO

        """
        for asset in self.assetgroup.pool:
            if asset.name == sell_asset.name:
                if asset.quantity >= quantity:
                    self.currency += quantity*price
                    asset.quantity -= quantity
                    print(f"{asset.name}: {asset.quantity}\n"
                            f"Currency: {self.currency}")
                    return 1
                else:
                    print("selling failed.")
                    return 0
            else:
                return 0

    def _bankrupt(self):
        pass

    def __repr__(self):
        return f"{self.name} starts his interest with {self.currency}."


class assetGroup(object):
    def __init__(self):
        self.pool = []

    def append(self, new_asset):
        if self.pool:
            for asset in self.pool:
                if new_asset.name == asset.name:
                    quantity = asset.quantity + new_asset.quantity
                    asset.unit_cost = (
                        asset.settle()+new_asset.settle())/quantity
                    asset.quantity += new_asset.quantity
                    new_asset.reset()
            if new_asset.unit_cost != 0:
                self.pool.append(new_asset)
        else:
            self.pool.append(new_asset)
        print(self)

    def merge(self):
        pass

    def __str__(self):
        content = ""
        for asset in self.pool:
            content += f"{asset.name}: cost: {asset.unit_cost}, sum: {asset.quantity}\n"
        return content


class assetBase(object):

    """Docstring for asset. """

    def __init__(self, name, cost, quantity):
        """TODO: to be defined. """
        self.name = name
        self.unit_cost = cost
        self.quantity = quantity
        self.cost = 0.0
        self.value = 0.0

    def settle(self):
        self.cost = self.quantity * self.unit_cost
        return self.cost

    def reset(self):
        self.unit_cost = 0.0
        self.quantity = 0.0
        self.cost = 0.0
        self.value = 0.0


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
    NewTrader = traderBase('John', 10000)
    print(NewTrader)
    asset1 = assetBase('SZ002230', 3.20, 100)
    NewTrader.buy(asset1)
    asset2 = assetBase('SZ002230', 5.71, 100)
    asset3 = assetBase('SH601818', 6.43, 100)
    NewTrader.buy(asset2)
    NewTrader.buy(asset3)
    asset4 = assetBase('SZ002230', 6.82, 100)
    NewTrader.sell(asset4, 100, 6.82)
