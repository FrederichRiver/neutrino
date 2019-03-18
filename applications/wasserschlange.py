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
from torch.utils.data import Dataset, DataLoader
input_size = 15
hidden_size = 15

class LSTM101(nn.Module):
    def __init__(self, *args, **kwargs):
        super(LSTM101, self).__init__()
        self.lstm = nn.LSTM(input_size,4*hidden_size,batch_first=True)
        self.lstm2 = nn.LSTM(4*hidden_size,2*hidden_size,batch_first=True)
        self.predict = nn.Linear(2*hidden_size,1)
        self.hidden = None
        self.hidden2 = None
    def init_hidden():
        pass

    def forward(self, x):
        _out, self.hidden = self.lstm(x, self.hidden)
        _out2, self.hidden2 = self.lstm2(_out, self.hidden2)
        _out3 = self.predict(_out2)
        return _out3
class trainSet(Dataset):
    def __init__(self, x):
        self.data, self.label = x[:,:-1], x[:,-1] 
    def __getitem__(self,i):
        return self.data[i], self.label[i]
    def __len__(self):
        return len(self.data)


def training(first = True):
    n = input_size
    sp = EventStockPrice()
    prices = sp.run()
    t = torch.tensor(prices[0][:-500])
    x = t.resize_(int(t.size(0)/(n+1)),n+1)
    print('x:',x.size())
    dt,label = x[:,:-1],x[:,-1]
    print('dt:',dt.size())
    print('label:',label.size())
    if first:
        model = LSTM101()
    else:
        model = torch.load('lstm.pkl')
    loss_function = nn.MSELoss()
    valuate_price = model(torch.unsqueeze(dt,dim=0))
    EPOCH = 500
    train_set = trainSet(x)
    train_data= DataLoader(train_set, batch_size = 10,shuffle=True)
    optimizer = torch.optim.Adam(model.parameters(),lr=0.0001)
    for step in range(EPOCH):
        for x,y in train_data:
            output = model(torch.unsqueeze(x,dim = 0))
            loss= loss_function(torch.squeeze(output),y)
            optimizer.zero_grad
            loss.backward(retain_graph=True)
            optimizer.step()
        print(step,loss)
        if step % 10: 
            torch.save(model,'lstm.pkl')
    torch.save(model, 'lstm.pkl')

def test():
    n = input_size
    sp = EventStockPrice()
    prices = sp.run()
    t = torch.tensor(prices[0])
    t = t[-500:]
    x = t.resize_(int(t.size(0)/(n+1)),n+1)
    dt,label = x[:,:-1],x[:,-1]
    lstm = torch.load('lstm.pkl')
    train_set = trainSet(x)
    train_data= DataLoader(train_set, batch_size = len(train_set),shuffle=True)
    for x,y in train_data:
        out= lstm(torch.unsqueeze(x,dim=0))
        print(x,out,y)

if __name__ == '__main__':
    test()
    #training(first=False)   
