# https://machinelearningmastery.com/a-gentle-introduction-to-positional-encoding-in-transformer-models-part-1/
# https://www.youtube.com/watch?v=PXOzkkB5eH0&t=118s
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import json
import math


class TRANS(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.L = nn.Linear(4, 128, bias=False)
        self.UL = nn.Linear(128, 4, bias=False)
        self.W_Q = nn.Linear(128, 64, bias=False)
        self.W_K = nn.Linear(128, 64, bias=False)
        self.W_V_down = nn.Linear(128, 64, bias=False)
        self.W_V_up = nn.Linear(64, 128, bias=False)

        self.W_Q2 = nn.Linear(128, 64, bias=False)
        self.W_K2 = nn.Linear(128, 64, bias=False)
        self.W_V_down2 = nn.Linear(128, 64, bias=False)
        self.W_V_up2 = nn.Linear(64, 128, bias=False)

        # self.W_Q3 = nn.Linear(128, 64, bias=False)
        # self.W_K3 = nn.Linear(128, 64, bias=False)
        # self.W_V_down3 = nn.Linear(128, 64, bias=False)
        # self.W_V_up3 = nn.Linear(64, 128, bias=False)


        self.soft_max = nn.Softmax(1)
        self.soft_max2 = nn.Softmax(1)

        self.quesin = nn.Parameter(torch.randn([10, 128, 64], requires_grad=True))
        self.quesout = nn.Parameter(torch.randn([10, 64, 128], requires_grad=True))
        self.quesin2 = nn.Parameter(torch.randn([10, 128, 64], requires_grad=True))
        self.quesout2 = nn.Parameter(torch.randn([10, 64, 128], requires_grad=True))
        # self.quesin3 = nn.Parameter(torch.randn([10, 128, 64], requires_grad=True))
        # self.quesout3 = nn.Parameter(torch.randn([10, 64, 128], requires_grad=True))
        self.mask = torch.zeros([10, 10])
        self.position = torch.zeros([10, 128])
        for i, row in enumerate(self.mask):
            # print(i, row)
            for k in range(i):
                self.mask[i][k] += float("-inf")
        # print(self.mask)
        # print(self.position.shape[0])
        # print(self.position.shape[1])
        for i in range(self.position.shape[0]):
            for j in range(self.position.shape[1] // 2):
                self.position[i][2 * j] += math.sin(i / (1000 ** (2 * j / 128)))
                self.position[i][2 * j + 1] += math.cos(i / (1000 ** (2 * j / 128)))
        # print(self.position)

    def forward(self, x):
        x = self.L(x)
        x += self.position
        Q = self.W_Q(x)
        K = self.W_K(x)
        V = self.W_V_up(self.W_V_down(x))
        C = torch.einsum("nik,njk->nji", Q, K)
        # print(C.shape)
        # print(self.mask.shape)
        for i in range(C.shape[0]):
            # print(C[i])
            C[i] += self.mask
            # print(C[i])
        # print(C)
        C = self.soft_max(C)
        DE = torch.einsum("nij,nik->nkj", V, C)

        E2 = x + DE/math.sqrt(10)

        x = torch.einsum("mnj,nji,nik->mnk", E2, self.quesin, self.quesout)

        Q2 = self.W_Q2(x)
        K2 = self.W_K2(x)
        V2 = self.W_V_up2(self.W_V_down2(x))
        C2 = torch.einsum("nik,njk->nji", Q2, K2)
        # print(C.shape)
        # print(self.mask.shape)
        for i in range(C2.shape[0]):
            # print(C[i])
            C2[i] += self.mask
            # print(C[i])
        # C2=C2/torch.max(C2)
        # print(C2)
        C2 = self.soft_max2(C2)
        # print(C2)
        DE2 = torch.einsum("nij,nik->nkj", V2, C2)

        E22 = x + DE2/math.sqrt(10)

        x = torch.einsum("mnj,nji,nik->mnk", E22, self.quesin2, self.quesout2)

        x = self.UL(x)
        return x



class DAY_DATA(Dataset):
    def __init__(self) -> None:
        super().__init__()
        share_data = {}
        with open("stock_data/SH600007.json", "rb") as ipf:
            share_data = json.load(ipf)
        # print(share_data)
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


def print_tensor(filename, tensor):
    with open(filename, "w") as file:
        torch.set_printoptions(precision=2, linewidth=1000)
        file.write(f"{tensor}")


model = TRANS()
model = torch.load("trans2")
dataset = DAY_DATA()
# print(dataset[len(dataset) - 1])
dataloader = DataLoader(dataset=dataset, batch_size=4, shuffle=True)

num_epochs = 1
tot_sample = len(dataset)
n_iter = math.ceil(tot_sample / 4)

print(tot_sample, n_iter)

with open("paralis", "w") as file:
    for it in model.parameters():
        torch.set_printoptions(precision=2, linewidth=1000)
        file.write(f"{it}\n")
opt = torch.optim.Adam(model.parameters())
mse = torch.nn.MSELoss()

for ep in range(num_epochs):
    for i, (x, y) in enumerate(dataloader):
        # opt.zero_grad()
        z = model(x)
        loss = mse(y, z)
        # loss.backward()
        # opt.step()
        if (i + 1) % 5 == 0:
            print(f"loss-{loss}-epoch {ep+1}/{num_epochs}, step{i+1}/{n_iter}, inputs{x.shape}")
            print_tensor(
                f"view_data/epoch--{num_epochs}-step-{i+1}-{n_iter}-inputs-{x.shape}-x",
                x,
            )
            print_tensor(
                f"view_data/epoch--{num_epochs}-step-{i+1}-{n_iter}-inputs-{x.shape}-y",
                y,
            )
            print_tensor(
                f"view_data/epoch--{num_epochs}-step-{i+1}-{n_iter}-inputs-{x.shape}-z",
                z,
            )
    # torch.save(model, "trans2")
