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
import torch.nn.functional as F

input_size = 15
hidden_size = 15

class LSTM101(nn.Module):
    def __init__(self, *args, **kwargs):
        super(LSTM101, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size,batch_first=True)
        self.predict = nn.Linear(hidden_size,1)
        self.hidden = None
    def init_hidden():
        pass

    def forward(self, x):
        print('running')
        _out, self.hidden = self.lstm(x, self.hidden)
        _out3 = self.predict(_out)
        return _out3



if __name__ == '__main__':
    n = input_size
    sp = EventStockPrice()
    prices = sp.run()
    t = torch.Tensor(prices[0])
    x = t.resize_(int(t.size(0)/(n+1)),n+1)
    print('x:',x.size())
    dt,label = x[:,:-1],x[:,-1]
    print('dt:',dt.size())
    print('label:',label.size())
    model = LSTM101()
    #loss_function = nn.NLLLoss()
    valuate_price = model(torch.unsqueeze(dt,dim=0))
    #print(model)
    print(valuate_price.size())
    print(valuate_price)
    #loss = loss_function(valuate_price, y[1])
    #loss.backward()
    """
    optimizer = optim.SGD(model.parameter(), lr= 0.01)
    optimizer.step()
    """
