import torch.optim as optim
import torch


stx = [0, 2, 1]
sty = [1, 2, 7]


import matplotlib.pyplot as plt

cl0 = 0.1 * torch.randn((20, 2))
for i in range(20):
    cl0[i][0] += stx[0]
    cl0[i][1] += sty[0]
print(cl0)
cl1 = 0.1 * torch.randn((100, 2))
for i in range(100):
    cl1[i][0] += stx[1]
    cl1[i][1] += sty[1]
print(cl1)
cl2 = 0.1 * torch.randn((5, 2))
for i in range(5):
    cl2[i][0] += stx[2]
    cl2[i][1] += sty[2]
print(cl2)


plt.scatter(stx, sty)
plt.scatter(cl0[:, 0].detach().numpy(), cl0[:, 1].detach().numpy(), c="red")
plt.scatter(cl1[:, 0].detach().numpy(), cl1[:, 1].detach().numpy(), c="green")
plt.scatter(cl2[:, 0].detach().numpy(), cl2[:, 1].detach().numpy(), c="blue")
plt.show()


dt = torch.concatenate([cl0, cl1, cl2], dim=0)

plt.scatter(dt[:, 0].detach().numpy(), dt[:, 1].detach().numpy(), c="red")
plt.show()

import torch.nn as nn


class losL(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.weight = nn.parameter.Parameter(torch.randn((125, 3), requires_grad=True))
        self.active = nn.Softmax(dim=1)

    def forward(self, x):
        self.weight = self.active(self.weight)
        mean = torch.einsum("ij,ik->ijk", self.weight, x)
        sum = torch.einsum("ij->j", self.weight)
        tmea = torch.einsum("ijk,j->ijk", mean, 1 / sum)
        orig = torch.einsum("ik,j->ijk", x, torch.ones(3).to("cuda"))
        deva = torch.einsum("ijk,ij,j->", (tmea - orig) ** 2, self.weight, 1 / sum)
        return deva


IS_CREATE = 1
CHECKPOINT_PATH = "./data/"

if IS_CREATE:
    net = losL()
    optimizer = optim.Adam(net.parameters(), lr=0.001)
    torch.save(
        {
            "epoch": 0,
            "model_state_dict": net.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "loss": None,
        },
        CHECKPOINT_PATH + f"cnnCheckPoint{0}",
    )
    with open(CHECKPOINT_PATH + "epoch.log", "w") as file:
        file.write(f"{0}")


IS_TRAIN = 1
EPOCH_NUM = 10000
if IS_TRAIN:
    model = losL().to("cuda")
    criterion = nn.MSELoss()
    optimizer = optim.Adam(net.parameters(), lr=0.001)
    with open(CHECKPOINT_PATH + "epoch.log", "r") as file:
        startEpoch = int(file.read())
        print(startEpoch)
    checkpoint = torch.load(CHECKPOINT_PATH + f"cnnCheckPoint{startEpoch}")
    model.load_state_dict(checkpoint["model_state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
    epoch = checkpoint["epoch"]
    loss = checkpoint["loss"]
    model.train()
    for epoch in range(startEpoch + 1, startEpoch + 1 + EPOCH_NUM):
        runningLoss = 0.0

        optimizer.zero_grad()
        output = model(dt.to("cuda"))
        # print(output.shape)
        loss = criterion(output, torch.tensor(0.0).to("cuda"))
        loss.backward()
        optimizer.step()

        runningLoss += loss.item()
        if epoch % 200 == 199:  # print every 2000 mini-batches
            print(f"[{epoch}, {i + 1:5d}] loss: {runningLoss / 200:.3f}")
            runningLoss = 0.0

            torch.save(
                {
                    "epoch": epoch,
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "loss": loss,
                },
                CHECKPOINT_PATH + f"cnnCheckPoint{epoch}",
            )
            with open(CHECKPOINT_PATH + "epoch.log", "w") as file:
                file.write(f"{epoch}")


model = losL().to("cuda")
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr=0.001)
with open(CHECKPOINT_PATH + "epoch.log", "r") as file:
    startEpoch = int(file.read())
    print(startEpoch)

checkpoint = torch.load(CHECKPOINT_PATH + f"cnnCheckPoint{startEpoch}")
model.load_state_dict(checkpoint["model_state_dict"])
optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
epoch = checkpoint["epoch"]
loss = checkpoint["loss"]
model.eval()
