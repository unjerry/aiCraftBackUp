import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import json
import math
import torch.nn.functional as F


class DAY_DATA(Dataset):
    def __init__(self, filename) -> None:
        super().__init__()
        share_data = {}
        self.filename = filename
        with open(filename, "rb") as ipf:
            share_data = json.load(ipf)
        print(share_data)
        share_data_2_6 = [it[2:6] for it in share_data["item"]]
        # print(share_data_2_6)
        self.share_data_tensor = torch.tensor(share_data_2_6)

    def __getitem__(self, index):
        s = 10
        return (
            self.share_data_tensor[index : index + s, :],
            self.share_data_tensor[index + 1 : index + 1 + s, :],
        )

    def __len__(self):
        return self.share_data_tensor.shape[0] - 10


class DIF_DAY_DATA(Dataset):
    def __init__(self, filename, s=10) -> None:
        super().__init__()
        share_data = {}
        self.s = s
        self.filename = filename
        with open(filename, "rb") as ipf:
            share_data = json.load(ipf)
        # print(share_data)
        share_data_7 = [it[7:8] for it in share_data["item"]]
        # print(share_data_7)
        self.share_data_tensor = torch.tensor(share_data_7)

    def __getitem__(self, index):
        return (
            torch.log(
                self.share_data_tensor[index + 1 : index + self.s + 1, :] / 100 + 1
            ),
            torch.log(
                self.share_data_tensor[index + 1 + 1 : index + 1 + self.s + 1, :] / 100
                + 1
            ),
        )

    def __len__(self):
        return self.share_data_tensor.shape[0] - self.s - 1


class FUL_DAY_DATA_IMAGE(Dataset):
    def __init__(self, filename, s=10) -> None:
        super().__init__()
        share_data = {}
        self.s = s
        self.filename = filename
        with open(filename, "rb") as ipf:
            share_data = json.load(ipf)
        # print(share_data)
        share_data = [math.log(it[5] / 100 + 1) for it in share_data["item"]]
        share_data_2_6 = [it[8:9] for it in share_data["item"]]
        share_data_7 = []
        share_data_7_1 = []
        for i in range(1, len(share_data)):
            zero = torch.zeros(21)
            # print(zero.size())
            if share_data[i] < -0.11 or share_data[i] > 0.1:
                print(share_data[i])
            zero[math.floor((share_data[i] - (-0.11)) / 0.01)] = 1.0
            share_data_7.append(zero)
            share_data_7_1.append(math.floor((share_data[i] - (-0.11)) / 0.01))
        self.share_data_tensor = torch.stack(share_data_7)
        self.share_data_tensor_1 = torch.tensor(share_data_7_1)
        # print(self.share_data_tensor.size())

    def __getitem__(self, index):
        return (
            self.share_data_tensor[None, index + 1 : index + self.s + 1, :],
            self.share_data_tensor_1[index + 1 + self.s],
        )

    def __len__(self):
        return self.share_data_tensor.shape[0] - self.s - 1


class DIF_DAY_DATA_IMAGE_TEST(Dataset):
    def __init__(self, filename, s=10) -> None:
        super().__init__()
        share_data = {}
        self.s = s
        self.filename = filename
        with open(filename, "rb") as ipf:
            share_data = json.load(ipf)
        # print(share_data)
        share_data = [math.log(it[7] / 100 + 1) for it in share_data["item"]]
        share_data_7 = []
        share_data_7_1 = []
        for i in range(1, len(share_data)):
            zero = torch.zeros(21)
            # print(zero.size())
            if share_data[i] < -0.11 or share_data[i] > 0.1:
                print(share_data[i])
            zero[math.floor((share_data[i] - (-0.11)) / 0.01)] = 1.0
            share_data_7.append(zero)
            share_data_7_1.append(math.floor((share_data[i] - (-0.11)) / 0.01))
        self.share_data_tensor = torch.stack(share_data_7)
        self.share_data_tensor_1 = torch.tensor(share_data_7_1)
        # print(self.share_data_tensor.size())

    def __getitem__(self, index):
        return (
            self.share_data_tensor[
                None, index + self.test + 1 : index + self.test + self.s + 1, :
            ],
            self.share_data_tensor_1[index + self.test + 1 + self.s],
        )

    def __len__(self):
        self.test = math.ceil((self.share_data_tensor.shape[0] - self.s - 1) * 0.8)
        self.len = math.floor((self.share_data_tensor.shape[0] - self.s - 1) * 0.2)
        return self.len


class DIF_DAY_DATA_IMAGE_TRAIN(Dataset):
    def __init__(self, filename, s=10) -> None:
        super().__init__()
        share_data = {}
        self.s = s
        self.filename = filename
        with open(filename, "rb") as ipf:
            share_data = json.load(ipf)
        # print(share_data)
        share_data = [math.log(it[7] / 100 + 1) for it in share_data["item"]]
        share_data_7 = []
        share_data_7_1 = []
        for i in range(1, len(share_data)):
            zero = torch.zeros(21)
            # print(zero.size())
            if share_data[i] < -0.11 or share_data[i] > 0.1:
                print(share_data[i])
            zero[math.floor((share_data[i] - (-0.11)) / 0.01)] = 1.0
            share_data_7.append(zero)
            share_data_7_1.append(math.floor((share_data[i] - (-0.11)) / 0.01))
        self.share_data_tensor = torch.stack(share_data_7)
        self.share_data_tensor_1 = torch.tensor(share_data_7_1)
        # print(self.share_data_tensor.size())

    def __getitem__(self, index):
        return (
            self.share_data_tensor[None, index + 1 : index + self.s + 1, :],
            self.share_data_tensor_1[index + 1 + self.s],
        )

    def __len__(self):
        self.len = math.floor((self.share_data_tensor.shape[0] - self.s - 1) * 0.8)
        return self.len


class FUL_DAY_DATA(Dataset):
    def __init__(self, filename, s=10) -> None:
        super().__init__()
        share_data = {}
        self.s = s
        self.filename = filename
        with open(filename, "rb") as ipf:
            share_data = json.load(ipf)
        # print(share_data)
        share_data_7 = [it[7:8] for it in share_data["item"]]
        share_data_2_6 = [it[2:6] for it in share_data["item"]]
        share_data_8 = [it[8:9] for it in share_data["item"]]
        # print(share_data_7)
        self.share_data_tensor = torch.tensor(share_data_7)
        self.share_data_tensor_26 = torch.tensor(share_data_2_6)
        self.share_data_tensor_8 = torch.tensor(share_data_8)

    def __getitem__(self, index):
        return (
            torch.concatenate(
                (
                    torch.log(
                        self.share_data_tensor[index + 1 : index + self.s + 1, :] / 100
                        + 1
                    ),
                    self.share_data_tensor_26[index + 1 : index + self.s + 1, :],
                    self.share_data_tensor_8[index + 1 : index + self.s + 1, :],
                ),
                dim=1,
            ),
            torch.concatenate(
                (
                    torch.log(
                        self.share_data_tensor[
                            index + 1 + 1 : index + 1 + self.s + 1, :
                        ]
                        / 100
                        + 1
                    ),
                    self.share_data_tensor_26[index + 1 : index + self.s + 1, :],
                    self.share_data_tensor_8[index + 1 : index + self.s + 1, :],
                ),
                dim=1,
            ),
        )

    def __len__(self):
        return self.share_data_tensor.shape[0] - self.s - 1


class SIMP_RNN(nn.Module):
    def __init__(self, INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE, NUM_LAYER, N, L) -> None:
        super().__init__()
        self.INPUT_SIZE = INPUT_SIZE
        self.HIDDEN_SIZE = HIDDEN_SIZE
        self.OUTPUT_SIZE = OUTPUT_SIZE
        self.NUM_LAYER = NUM_LAYER
        self.N = N
        self.L = L
        self.RNN = nn.RNN(
            INPUT_SIZE,
            HIDDEN_SIZE,
            NUM_LAYER,
            dropout=0.5,
            device="cpu",
            batch_first=True,
        )
        self.HIDLIN = nn.Linear(self.L, HIDDEN_SIZE)
        self.LIN = nn.Linear(HIDDEN_SIZE, HIDDEN_SIZE)
        self.LIN2 = nn.Linear(HIDDEN_SIZE, OUTPUT_SIZE)
        self.TAN = nn.Tanh()

    def forward(self, x):
        # print(x.shape)
        preh = self.HIDLIN(x.view(-1, self.L))
        # print(preh.size())
        h = preh.repeat(self.NUM_LAYER, 1, 1)
        # print(h.size())
        z, h = self.RNN(x, h)
        ans = 2 * self.TAN(self.LIN2(self.LIN(z)))
        return ans


class SIMP_LSTM(nn.Module):
    def __init__(self, INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE, NUM_LAYER, N, L) -> None:
        super().__init__()
        self.INPUT_SIZE = INPUT_SIZE
        self.HIDDEN_SIZE = HIDDEN_SIZE
        self.OUTPUT_SIZE = OUTPUT_SIZE
        self.NUM_LAYER = NUM_LAYER
        self.N = N
        self.L = L
        self.h0 = torch.nn.Parameter(
            torch.randn(self.NUM_LAYER, self.N, self.OUTPUT_SIZE)
        )
        self.c0 = torch.nn.Parameter(
            torch.randn(self.NUM_LAYER, self.N, self.HIDDEN_SIZE)
        )
        # self.h0 = torch.zeros(self.NUM_LAYER, self.N, self.OUTPUT_SIZE)
        # self.c0 = torch.zeros(self.NUM_LAYER, self.N, self.HIDDEN_SIZE)

        self.lstm = torch.nn.LSTM(
            self.INPUT_SIZE,
            self.HIDDEN_SIZE,
            self.NUM_LAYER,
            batch_first=True,
            proj_size=self.OUTPUT_SIZE,
        )

    def forward(self, x):
        x, (h, c) = self.lstm(x, (self.h0, self.c0))
        return x


class SEQUENCE_CNN(nn.Module):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # self.cov1 = nn.Conv1d(1, 64, 3, stride=1, padding="same")
        # self.cov2 = nn.Conv1d(64, 128, 3, stride=1, padding="same")
        # self.pool = nn.MaxPool1d(3)
        self.lin1 = nn.Linear(6 * 21, 128)
        self.lin2 = nn.Linear(128, 256)
        self.lin3 = nn.Linear(256, 256)
        self.lin4 = nn.Linear(256, 64)
        self.lin5 = nn.Linear(64, 1)
        # self.lin4 = nn.Linear(256, 1)

    def forward(self, x):
        # print(x.size())
        # x = self.cov1(x)
        # print(x.size())
        # x = self.cov2(x)
        # print(x.size())
        # x = torch.flatten(x, 1)
        # print(x.size())
        x = torch.nn.Softplus()(self.lin1(x))
        # print(x.size())
        x = torch.nn.Softplus()(self.lin2(x))
        x = torch.nn.Softplus()(self.lin3(x))
        x = torch.nn.Softplus()(self.lin4(x))
        x = self.lin5(x)
        # print(x.size())
        # x = torch.nn.functional.relu(self.lin3(x))
        # x = torch.nn.functional.relu(self.lin4(x))
        return x


class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, stride=1, padding="same")
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, 3, stride=1, padding="same")
        self.fc2 = nn.Linear(64 * 5 * 5, 128)
        self.fc3 = nn.Linear(128, 21)

    def forward(self, x):
        # print(x.size())
        x = self.pool(F.relu(self.conv1(x)))
        # print(x.size())
        x = self.pool(F.relu(self.conv2(x)))
        # print(x.size())
        x = torch.flatten(x, 1)  # flatten all dimensions except batch
        # print(x.size())
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
