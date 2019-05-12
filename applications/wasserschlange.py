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
import pywt
input_size = 4
hidden_size = 4*input_size
seq_len = 10
batch_size = 1


def wavelet_nr(df):
    """TODO: Docstring for wavelet_nr.

    :df: TODO
    :returns: TODO

    """
    db4 = pywt.wavelet('db4')
    if type(df) is not types.NoneType:
        coeffs = pywt.wavedec(df, db4)
        coeffs[-1] = 0
        coeefs[-2] = 0
        meta = pywt.waverec(coeffs, db4)
        return meta


class LSTM101(nn.Module):
    def __init__(self, *args, **kwargs):
        super(LSTM101, self).__init__()
        self.lstm = nn.LSTM(input_size,
                            hidden_size,
                            batch_first=True)
        self.lstm2 = nn.LSTM(hidden_size,
                             hidden_size,
                             batch_first=True)
        self.lstm3 = nn.LSTM(hidden_size,
                             hidden_size,
                             batch_first=True)

        w1 = torch.zeros(1, batch_size, hidden_size)
        h1 = torch.zeros(1, batch_size, hidden_size)
        w2 = torch.zeros(1, batch_size, hidden_size)
        h2 = torch.zeros(1, batch_size, hidden_size)
        w3 = torch.zeros(1, batch_size, hidden_size)
        h3 = torch.zeros(1, batch_size, hidden_size)
        c1 = torch.zeros(1, batch_size, hidden_size)
        c2 = torch.zeros(1, batch_size, hidden_size)
        c3 = torch.zeros(1, batch_size, hidden_size)

        nn.init.xavier_uniform_(w1, 1)
        nn.init.xavier_uniform_(h1, 1)
        nn.init.xavier_uniform_(w2, 1)
        nn.init.xavier_uniform_(h2, 1)
        nn.init.xavier_uniform_(w3, 1)
        nn.init.xavier_uniform_(h3, 1)
        self.predict = nn.Linear(hidden_size, 1)
        self.hidden = (h1, c1)
        self.hidden2 = (h2, c2)
        self.hidden3 = (h3, c3)

    def forward(self, x):
        _out, _ = self.lstm(x, self.hidden)
        #_out2, _ = self.lstm2(_out, self.hidden2)
        #_out3, _ = self.lstm3(_out2, self.hidden3)
        _out4 = self.predict(_out)
        return _out4


class trainSet2(Dataset):
    def __init__(self, x):
        self.data = []
        self.label = []
        self.seq_len = seq_len
        self._run(x)

    def __getitem__(self, i):
        return self.data[i], self.label[i]

    def __len__(self):
        return len(self.data)

    def _run(self, x):
        n = int(len(x)/(self.seq_len+1))
        for i in range(n):
            t = i * self.seq_len
            self.data.append(x[t:t+self.seq_len-1, :4])
            self.label.append(x[t+1:t+self.seq_len, -1])
        # print(self.data[0],self.label[0])
        return self.data, self.label


def get_stock_data(stock_code):
    """TODO: Docstring for get_stock_data.
    :returns: TODO

    """
    n = input_size
    fd = financeData()
    prices = fd._get_stock_data(stock_code,
                                'close_price, open_price, high_price, low_price')
    prices = ma(prices, 7)
    prices = ma26(prices)
    prices = MACD(prices)
    prices['result'] = prices['close_price'].shift(-1)
    # print(prices.head)
    return prices


def model_create(first=True):
    if first:
        model = LSTM101(input_size, hidden_size, batch_first=True)
    else:
        model = torch.load('lstm.pkl')
    return model


def data_get():
    """TODO: Docstring for data_get.
    :returns: TODO

    """
    prices = get_stock_data('SH600001')
    prices = prices.as_matrix()
    t = torch.from_numpy(prices).float()
    return t


def training(model, t):
    import time
    for param in model.parameters():
        param.requires_grad = True
    model.train(mode=True)
    loss_function = nn.MSELoss()
    train_set = trainSet2(t)
    train_data = DataLoader(train_set,
                            batch_size=batch_size,
                            shuffle=True,
                            drop_last=True)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    EPOCH = 20
    for epoch in range(EPOCH):
        for step, (x, y) in enumerate(train_data):
            result = model(x)
            optimizer.zero_grad
            loss = loss_function(torch.squeeze(result), torch.squeeze(y))
            loss.backward()
            optimizer.step()
        print("EPOCH:{0}".format(epoch), loss,
              time.strftime('%H:%M:%S', time.localtime()))
        torch.save(model, 'lstm.pkl')
    torch.save(model, 'lstm.pkl')
    return model


def testing(model, t):
    """TODO: Docstring for testing.
    :returns: TODO

    """
    model.eval
    test_set = trainSet2(t)
    test_data = DataLoader(test_set, batch_size)
    for x, y in test_data:
        result = model(x)
        print(result)
        print(y)
        break


if __name__ == '__main__':
    model = model_create(first=True)
    t = data_get()
    training(model, t)
    testing(model, t)
