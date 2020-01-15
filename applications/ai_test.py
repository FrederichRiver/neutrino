import torch
import torch.nn


class Net1(nn.Module):
    def __init__(self):
        super(Net1, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv1d(
                in_channels=1,
                out_channels=8,
                kernel_size=3
            ),
            nn.MaxPool1d(kernel_size=2)
        )
        self.conv2 = nn.Sequential(
            nn.Conv1d(
                in_channels=8,
                out_channels=16,
                kernel_size=3
            ),
            nn.MaxPool1d(kernel_size=2)
        )
        # self.fc = nn.Linear(384, 1)

    def forward(self, input):
        x = self.conv1(input)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)
        out = x
        return out

