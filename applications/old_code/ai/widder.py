#!/usr/bin/python3
"""
Widder
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        # 1 input image channel, 6 output channels, 5x5 square convolution
        # kernel
        self.conv1 = nn.Conv1d(in_channels=4, out_channels=4, kernel_size=5)
        self.conv2 = nn.Conv1d(in_channels=4, out_channels=1 ,kernel_size=5)

        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(128 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 20)

    def forward(self, x):
        t = torch.randn(4,4,32)
        #maxpool1 = nn.MaxPool1d(3, stride=3)
        t1 = self.conv1(x)
        F.relu(t1)
        y = 1 
        # Max pooling over a (2, 2) window
        return y 

    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features

net = Net()
i = torch.randn(4,4,32)
print('i',i)
t0 = net.conv1(i)
print('t0',t0)
mp1 = nn.MaxPool1d(3, stride=3)
z = mp1(t0)
print('pooling',z)
t1 = F.relu(z)
print('t1',t1)
