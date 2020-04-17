#!/usr/bin/python3
# from strategy_base import strategyBase
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

input_size = 4
hidden_size = 4 * input_size
num_layers = 1
seq_len = 10
batch_size = 20


class strategyBase(object):
    def __init__(self):
        pass

    def _get_data(self):
        pass

    def _settle(self):
        pass


class Phoenix(nn.Module):
    """
    input (batch, seq_len, feature_size)
    output (batch, 1)
    """
    def __init__(self, *args, **kwargs):
        super(Phoenix, self).__init__()
        self.lstm = nn.LSTM(input_size,
                            hidden_size,
                            num_layers)
        # nn.init.xavier_uniform_(self.lstm.weight)
        self.linear = nn.Linear(hidden_size, 1)

    def forward(self, x):
        x, _ = self.lstm(x)
        print(x.size())
        b, s, h = x.shape
        x = x.reshape(batch_size * seq_len, hidden_size)
        x = self.linear(x)
        print(x.size())
        return x

    def train(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=0.001)
        loss_func = nn.CrossEntropyLoss()
        for epoch in range(10):
            pass


class stockData(torch.utils.data.Dataset):
    def __init__(self):
        from polaris.mysql8 import mysqlBase, mysqlHeader
        from dev_global.env import GLOBAL_HEADER
        import torch.tensor
        import pandas
        import numpy as np
        stock_code = 'SH600000'
        self.mysql = mysqlBase(GLOBAL_HEADER)
        result = self.mysql.select_values(stock_code, 'open_price,close_price,highest_price,lowest_price')
        predict = pandas.DataFrame()
        predict['predict'] = result[1].shift(-1)
        # print(result.head(10))
        self.input = []
        self.label = []
        # print(result.shape[0])
        block = 10
        for i in range(int(result.shape[0]/block)):
            x = result[i*block: (i+1)*block]
            y = predict['predict'][(i+1)*block-1]
            self.input.append(torch.tensor(np.array(x), dtype=torch.float32))
            self.label.append(torch.tensor(np.array(y), dtype=torch.float32))
        # print(result.head(15))
        # print(self.input[0])
        # print(self.label[0])

    def __len__(self):
        return len(self.input)

    def __getitem__(self, index):
        return self.input[index], self.label[index]


h = torch.randn(num_layers, batch_size, hidden_size)
c = torch.randn(num_layers, batch_size, hidden_size)
input = torch.randn(seq_len, batch_size, input_size)
# print(input)
net = Phoenix()
# output, _ = net.lstm(input, (h, c))
# out2 = net.forward(input)

dt = stockData()
inp = DataLoader(dt, batch_size=batch_size, drop_last=True)

for step, (x, y) in enumerate(inp):
    # print(step)
    # print(x.size())
    # print(x)
    # print(input.size())
    # print(input)
    print(y)
    print(net.forward(x))
    pass
