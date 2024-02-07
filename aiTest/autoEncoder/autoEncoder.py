import torch.nn as nn
from collections import OrderedDict
import torch
import torch.optim as optim


class autoDecoder(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.encoder = nn.Sequential(
            OrderedDict(
                [
                    ("Linear1", nn.Linear(28 * 28, 128)),
                    ("active1", nn.ReLU()),
                    ("Linear2", nn.Linear(128, 64)),
                    ("active2", nn.ReLU()),
                    ("Linear3", nn.Linear(64, 36)),
                    ("active3", nn.ReLU()),
                    ("Linear4", nn.Linear(36, 18)),
                    ("active4", nn.ReLU()),
                    ("Linear5", nn.Linear(18, 9)),
                ]
            )
        )
        self.decoder = nn.Sequential(
            OrderedDict(
                [
                    ("Linear1", nn.Linear(9, 18)),
                    ("active1", nn.ReLU()),
                    ("Linear2", nn.Linear(18, 36)),
                    ("active2", nn.ReLU()),
                    ("Linear3", nn.Linear(36, 64)),
                    ("active3", nn.ReLU()),
                    ("Linear4", nn.Linear(64, 128)),
                    ("active4", nn.ReLU()),
                    ("Linear5", nn.Linear(128, 28 * 28)),
                    ("active5", nn.Sigmoid()),
                ]
            )
        )

    def forward(self, input):
        code = self.encoder(torch.flatten(input, 1))
        output = self.decoder(code)
        return output, code


from torchvision import datasets
from torchvision.transforms import ToTensor

training_data = datasets.MNIST(
    root="data", train=True, download=True, transform=ToTensor()
)
test_data = datasets.MNIST(
    root="data", train=False, download=True, transform=ToTensor()
)


from torch.utils.data import DataLoader

train_dataloader = DataLoader(training_data, batch_size=64, shuffle=True)
test_dataloader = DataLoader(test_data, batch_size=64, shuffle=True)


IS_CREATE = 0
CHECKPOINT_PATH = "./data"
if IS_CREATE:
    net = autoDecoder()
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


IS_TRAIN = 0
EPOCH_NUM = 50
if IS_TRAIN:
    model = autoDecoder().to("cuda")
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
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
        for i, (trainFeatures, trainLabels) in enumerate(train_dataloader, 0):
            X = trainFeatures.to("cuda")
            # print(X.shape)

            optimizer.zero_grad()
            output, code = model(X)
            # print(output.shape)
            loss = criterion(output.view(-1), X.view(-1))
            loss.backward()
            optimizer.step()

            runningLoss += loss.item()

            # print(X.device, criterion(Y, trainLabels[i].to("cuda")), sep="|-|")
            if i % 200 == 199:  # print every 2000 mini-batches
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


model = autoDecoder().to("cuda")
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
with open(CHECKPOINT_PATH + "epoch.log", "r") as file:
    startEpoch = int(file.read())
    print(startEpoch)

checkpoint = torch.load(CHECKPOINT_PATH + f"cnnCheckPoint{startEpoch}")
model.load_state_dict(checkpoint["model_state_dict"])
optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
epoch = checkpoint["epoch"]
loss = checkpoint["loss"]
model.eval()


import matplotlib.pyplot as plt

# Display image and label.
train_features, train_labels = next(iter(train_dataloader))
print(f"Feature batch shape: {train_features.size()}")
print(f"Labels batch shape: {train_labels.size()}")
img = train_features[0]
label = train_labels[0]
output, code = model(img.view(1, -1).to("cuda"))
print(code)
plt.imshow(img.view(28, 28).cpu().detach().numpy(), cmap="gray")
plt.show()
plt.imshow(output.view(28, 28).cpu().detach().numpy(), cmap="gray")
plt.show()
print(f"Label: {label}")

labe = {
    0: "#1f77b4",
    1: "#ff7f0e",
    2: "#2ca02c",
    3: "#d62728",
    4: "#9467bd",
    5: "#8c564b",
    6: "#e377c2",
    7: "#7f7f7f",
    8: "#bcbd22",
    9: "#17becf",
}

for i in range(1000):
    img, label = test_data[i]
    output, code = model(img.view(1, -1).to("cuda"))
    act = torch.exp(output)
    lst = act.view(-1).tolist()
    # print(code.shape)
    plt.scatter(code[0][8].item(), code[0][7].item(), c=labe[label])

plt.show()
