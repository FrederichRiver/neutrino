import torch
from torch import nn, Tensor
from torch import optim
from torch.autograd import Variable
import torch.utils.data as Data
from torch.utils.data import TensorDataset

x_train = Tensor(['SH600001', 'SH601313', 'SH600005','SH601818', '600001.SH', '601818.SH'])
y_train = Tensor(['SH600001', 'SH601313', 'SH600005','SH601818', 'SH600001', 'SH601818'])

x_test = ['SH601926', '600235.SH']

code_set = TensorDataset(x_train, y_train)
train_loader = DataLoader(dataset=code_set,
        batch_size=1,
        shuffle=True)
print(train_loader)

class altair(nn.Moudule):
    def __init__(self):
        """TODO: Docstring for __init__.
        :returns: TODO

        """
        super(altair, self).__init__()
        self.layer1 = nn.Linear(10,10)
        self.layer2 = nn.Linear(10,10)

        w1 = torch.zeros(1, 10)
        h1 = torch.zeros(1, 10)
        w2 = torch.zeros(1, 10)
        h2 = torch.zeros(1, 10)
        nn.init.xavier_uniform_(w1, 1)
        nn.init.xavier_uniform_(h1, 1)
        nn.init.xavier_uniform_(w2, 1)
        nn.init.xavier_uniform_(h2, 1)
        
    def forward(self):
        _out, _ =self.layer1(x, self.w1, self.h1)
        _out2, _ =self.layer2(_out, self.w2, self.h2)
        return _out2

def training(model, t):
    loss_funtion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    EPOCH = 20
