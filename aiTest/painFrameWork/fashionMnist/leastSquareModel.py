import torch
import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, stride=1, padding="same")
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, 3, stride=1, padding="same")
        self.fc2 = nn.Linear(64 * 7 * 7, 128)
        self.fc3 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1)  # flatten all dimensions except batch
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class Pain(nn.Module):
    def __init__(self):
        super().__init__()
        self.dream1 = nn.Linear(11, 64, bias=True)
        self.dream2 = nn.Linear(64, 64, bias=True)
        self.dream3 = nn.Linear(64, 1, bias=True)
        self.act = nn.Softmax(dim=1)

    def forward(self, x):
        loss = self.dream1(x)
        loss = self.act(loss)
        loss = self.dream2(loss)
        loss = self.act(loss)
        loss = self.dream3(loss)
        return loss
