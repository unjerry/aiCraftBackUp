import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.a = nn.Linear(1, 1, bias=True)

    def forward(self, x):
        return self.a(x)


class Pain(nn.Module):
    def __init__(self):
        super().__init__()
        self.dream1 = nn.Linear(2, 16, bias=True)
        self.dream2 = nn.Linear(16, 16, bias=True)
        self.dream3 = nn.Linear(16, 1, bias=True)
        self.act = nn.Tanh()

    def forward(self, x):
        loss = self.dream1(x)
        loss = self.act(loss)
        loss = self.dream2(loss)
        loss = self.act(loss)
        loss = self.dream3(loss)
        return loss
