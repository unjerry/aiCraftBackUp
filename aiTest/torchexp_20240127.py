import torch
import torch.nn as nn
import torch.nn.functional as F

print(torch.cuda.is_available(), torch.__version__, sep="\n")


class ANN(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(OrderedDict())

    def forward(self, x):
        x = F.relu(self.conv1(x))
        return F.relu(self.conv2(x))
