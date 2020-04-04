#!/usr/bin/python3
# from strategy_base import strategyBase
import torch
import torch.nn as nn

input_size = 4
hidden_size = 4 * input_size
num_layers = 2
seq_len = 10
batch_size = 1


class strategyBase(object):
    def __init__(self):
        pass

    def _get_data(self):
        pass

    def _settle(self):
        pass


class Phoenix(nn.Module):
    def __init__(self, *args, **kwargs):
        super(Phoenix, self).__init__()
        self.lstm = nn.LSTM(input_size,
                            hidden_size,
                            num_layers,
                            batch_first=True)
        # nn.init.xavier_uniform_(self.lstm.weight)
        self.linear = nn.Linear(hidden_size, 1)
        nn.init.xavier_uniform_(self.linear.weight)
        nn.init.xavier_uniform(self.lstm.all_weights)

    def forward(self, x):
        x, _ = self.lstm(x)
        x = self.linear(x)
        return x


h = torch.randn(num_layers, batch_size, hidden_size)
c = torch.randn(num_layers, batch_size, hidden_size)
input = torch.randn(batch_size, seq_len, input_size)
# print(input)
net = Phoenix()
output, _ = net.lstm(input, (h, c))
print(output)
