import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import OrderedDict

print(torch.cuda.is_available(), torch.__version__, sep="\n")


class ANN(nn.Module):
    def __init__(self, inputDim, outputDim, hiddenDim, hiddenNum) -> None:
        super().__init__()
        self.ipl = nn.Sequential(
            OrderedDict(
                [
                    ("inputLinear", nn.Linear(inputDim, hiddenDim)),
                    ("inputActivation", nn.LogSoftmax()),
                ]
            )
        )
        self.hpl = nn.Sequential(
            OrderedDict(
                [
                    (
                        f"hidden{i}",
                        nn.Sequential(
                            OrderedDict(
                                [
                                    ("Linear", nn.Linear(hiddenDim, hiddenDim)),
                                    ("Activation", nn.LogSoftmax()),
                                ]
                            )
                        ),
                    )
                    for i in range(hiddenNum)
                ]
            )
        )
        self.opl = nn.Sequential(
            OrderedDict(
                [
                    ("outputLinear", nn.Linear(hiddenDim, outputDim)),
                    ("outputActivation", nn.LogSoftmax()),
                ]
            )
        )

    def forward(self, x):
        x = self.ipl(x)
        x = self.hpl(x)
        x = self.opl(x)
        return x
