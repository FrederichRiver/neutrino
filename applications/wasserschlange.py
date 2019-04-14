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
from data_feature import financeData, ma, ma26, MACD
input_size = 9
hidden_size = 20
seq_len = 15
batch_size = 1 

class LSTM101(nn.Module):
    def __init__(self, *args, **kwargs):
        super(LSTM101, self).__init__()
        self.lstm = nn.LSTM(input_size,
                hidden_size,
                batch_first=True)
        self.lstm2 = nn.LSTM(hidden_size,
                hidden_size,
                batch_first=True)

        self.predict = nn.Linear(hidden_size,1)
        self.hidden = (torch.autograd.Variable(torch.zeros(1,batch_size,hidden_size)),
                torch.autograd.Variable(torch.zeros(1,batch_size,hidden_size)))
        self.hidden2 = (torch.autograd.Variable(torch.zeros(1,batch_size,hidden_size)),
                torch.autograd.Variable(torch.zeros(1,batch_size,hidden_size)))


    def init_hidden():
        pass

    def forward(self, x):
        _out, self.hidden = self.lstm(x, self.hidden)
        _out2, self.hidden2 =self.lstm2(_out, self.hidden2)
        _out3 = self.predict(_out2)
        return _out3

class trainSet2(Dataset):
    def __init__(self, x):
        self.data = []
        self.label =[]
        self.seq_len = seq_len
        self._run(x)
    def __getitem__(self,i):
        return self.data[i], self.label[i]
    def __len__(self):
        return len(self.data)
    def _run(self,x):
        n = int(len(x)/(self.seq_len+1))
        for i in range(n):
            t = i* self.seq_len
            #print(t)
            self.data.append(x[i:i+self.seq_len-1,:-1])
            self.label.append(x[i+1:i+self.seq_len,-1])
        #print(self.data)
        return self.data,self.label
def get_stock_data(stock_code):
    """TODO: Docstring for get_stock_data.
    :returns: TODO

    """
    n = input_size
    fd = financeData()
    EPOCH = 100
    prices = fd._get_stock_data(stock_code,
            'close_price, open_price, high_price, low_price')
    prices = ma(prices, 7)
    prices = ma26(prices)
    prices = MACD(prices)
    prices['result'] = prices['close_price'].shift(-1)
    return prices

def training(first = True):
    prices = get_stock_data('SH600001')
    prices = prices.as_matrix()
    t = torch.autograd.Variable(torch.from_numpy(prices).float(),requires_grad=True)
    if first:
        model = LSTM101(input_size, hidden_size, batch_first=True)
    else:
        model = torch.load('lstm.pkl')
    loss_function = nn.MSELoss()
    train_set = trainSet2(t)
    train_data= DataLoader(train_set,
            batch_size = batch_size,
            shuffle=True,
            drop_last=True)
    optimizer = torch.optim.Adam(model.parameters(),lr=0.0001)
    import time
    basetime = time.time()
    
    for step in range(EPOCH):
        for x,y in train_data:
            result = model(x)
            #print(result.shape,y.shape)
            #print(torch.squeeze(result).shape,torch.squeeze(y).shape)
            loss = loss_function(torch.squeeze(result),torch.squeeze(y))
            optimizer.zero_grad
            loss.backward(retain_graph=True)
            optimizer.step()
        print(step,loss,time.strftime('%H:%M:%S',time.localtime()))
        
        #if step % 10: 
        torch.save(model,'lstm.pkl')
    torch.save(model, 'lstm.pkl')

if __name__ == '__main__':
    training(first=False)
    
