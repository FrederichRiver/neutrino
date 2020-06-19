#!/usr/bin/python3
from abc import ABCMeta, abstractmethod
# Event (market, signal, order, fill)
# Event Queue
# portfolio
# DataHandler(abstract base class)产生market event
# Strategy
class Strategy(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def interface(self):
        raise NotImplementedError
# ExecutionHandler
# Back test
class MarketEventBase(object):
    pass

class SingalBase(object):
    def __init__(self):

