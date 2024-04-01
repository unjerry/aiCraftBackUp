import os
import pandas as pd
from torch.utils.data import Dataset
import torch


class learsSquareData(Dataset):
    def __init__(self, fileName) -> None:
        super().__init__()
        self.dt = pd.read_csv(fileName).values
        self.X = self.dt[:, 0]
        self.Y = self.dt[:, 1]
        print(self.X)
        print(self.Y)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, index):
        return torch.tensor(self.X[index], device="cuda", dtype=torch.float32).view(-1), torch.tensor(self.Y[index], device="cuda", dtype=torch.float32).view(-1)
