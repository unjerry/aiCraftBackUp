from parameter import BATCH_SIZE
from parameter import DATA_ROOT
from parameter import EPOCH_NUM
from parameter import CHECKPOINT_PATH

import torch
from torchvision import datasets
from torchvision.transforms import ToTensor

print("start loading data")
training_data = datasets.FashionMNIST(
    root=DATA_ROOT, train=True, download=True, transform=ToTensor()
)
test_data = datasets.FashionMNIST(
    root=DATA_ROOT, train=False, download=True, transform=ToTensor()
)


from torch.utils.data import DataLoader

train_dataloader = DataLoader(training_data, batch_size=BATCH_SIZE, shuffle=True)
test_dataloader = DataLoader(test_data, batch_size=BATCH_SIZE, shuffle=True)
# classes = {
#     0: "T-Shirt",
#     1: "Trouser",
#     2: "Pullover",
#     3: "Dress",
#     4: "Coat",
#     5: "Sandal",
#     6: "Shirt",
#     7: "Sneaker",
#     8: "Bag",
#     9: "Ankle Boot",
# }
classes = (
    "T-Shirt",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle Boot",
)
print("data load finish")


import torch.nn as nn
import torch.optim as optim
from cnn import Net, Pain


model = Net().to("cuda")
criterion = Pain().to("cuda")
truePain = nn.MSELoss()
trueCriterion = nn.CrossEntropyLoss()
criterion_optimizer = optim.Adam(criterion.parameters(), lr=0.001)
optimizer = optim.Adam(model.parameters(), lr=0.001)
with open(CHECKPOINT_PATH + "epoch.log", "r") as file:
    startEpoch = int(file.read())
    print(startEpoch)

checkpoint = torch.load(CHECKPOINT_PATH + f"cnnCheckPoint{startEpoch}")
model.load_state_dict(checkpoint["model_state_dict"])
criterion.load_state_dict(checkpoint["criterion_state_dict"])
optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
criterion_optimizer.load_state_dict(checkpoint["criterion_optimizer_state_dict"])
epoch = checkpoint["epoch"]
loss = checkpoint["loss"]
model.train()

for epoch in range(startEpoch + 1, startEpoch + 1 + EPOCH_NUM):
    runningLoss = 0.0
    for i, (trainFeatures, trainLabels) in enumerate(train_dataloader, 0):
        X = trainFeatures.to("cuda")
        Y = trainLabels.to("cuda")
        # print(X.shape, Y.shape)
        # print(X.dtype, Y.shape)

        optimizer.zero_grad()
        criterion_optimizer.zero_grad()
        output = model(X)
        # print(output.shape)
        with torch.no_grad():
            op = output
        pain = criterion((X, output))
        # trpain = torch.func.vmap(trueCriterion)(op, Y).view(-1, 1)
        sumpain = torch.sum(pain)
        # loss = truePain(pain, trpain)
        ## print(pain.shape, trpain.shape)
        ## print(output[0].shape, Y[0].shape)
        # loss.backward(retain_graph=True)

        sumpain.backward(retain_graph=True)
        optimizer.step()
        # criterion_optimizer.step()

        # runningLoss += loss.item()
        runningLoss += sumpain.item()

        # print(X.device, criterion(Y, trainLabels[i].to("cuda")), sep="|-|")
        if i % 200 == 199:  # print every 2000 mini-batches
            print(f"[{epoch}, {i + 1:5d}] loss: {runningLoss / 200:.7f}")
            runningLoss = 0.0
    torch.save(
        {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "criterion_state_dict": criterion.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "criterion_optimizer_state_dict": criterion_optimizer.state_dict(),
            "loss": loss,
        },
        CHECKPOINT_PATH + f"cnnCheckPoint{epoch}",
    )
    with open(CHECKPOINT_PATH + "epoch.log", "w") as file:
        file.write(f"{epoch}")
