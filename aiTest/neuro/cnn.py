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
        self.conv1 = nn.Conv2d(1, 32, 3, stride=1, padding="same")
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, 3, stride=1, padding="same")
        self.fc2 = nn.Linear(64 * 7 * 7 + 10, 128)
        self.fc3 = nn.Linear(128, 1)

    def forward(self, x):
        t, r = x
        t = self.pool(F.relu(self.conv1(t)))
        t = self.pool(F.relu(self.conv2(t)))
        t = torch.flatten(t, 1)  # flatten all dimensions etcept batch
        # print(t.shape, r.shape)
        t = F.relu(self.fc2(torch.concatenate((t, r), dim=1)))
        t = self.fc3(t)
        return t
