#!/usr/bin/python3
import torch
import torch.nn as nn
import torch.optim as optim
from mysql.libmysql8_dev import MySQLBase
"""
1.create network
2.create training set
3.training
4.test
5.running
"""
from events import EventStockPrice

class LSTM101(nn.Module):
    def __init__(self, *args, **kwargs):
        super(LSTM101, self).__init__()
        self.lstm = nn.LSTM(1, 15)
        self.hidden = None
    def forward(self, input_serial):
        print('running')
        _out, self.hidden = self.lstm(input_serial,self.hidden)
        return _out



if __name__ == '__main__':
    sp = EventStockPrice()
    prices = sp.run()
    t = torch.Tensor(prices[0])
    x = t.resize_(16,int(t.size(0)/16),1)
    y = torch.split(x, 15,0)
    print(y[0].size())
    print(y[1].size())
    model = LSTM101()
    loss_function = nn.NLLLoss()
    valuate_price = model(y[0])
    print(valuate_price.size())
    """
    loss = loss_function(valuate_price, y[1])
    loss.backward()
    optimizer = optim.SGD(model.parameter(), lr= 0.01)
    optimizer.step()
    """
