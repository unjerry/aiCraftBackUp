import torch
import sys
import importlib
from parameter import EPOCH_NUM, CHECKPOINT_PATH, TRAIN_DATA_LOADER, TEST_DATA_LOADER

print("start loading data")
sys.path.append(f"{CHECKPOINT_PATH}")
train_dataloader = importlib.import_module(TRAIN_DATA_LOADER).train_dataloader
test_dataloader = importlib.import_module(TEST_DATA_LOADER).test_dataloader
print("data load finish")


import torch.nn as nn
import torch.optim as optim

sys.path.append(f"{CHECKPOINT_PATH}")
Net = importlib.import_module(f"model").Net

model = Net().to("cuda")
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
with open(CHECKPOINT_PATH + "epoch.log", "r") as file:
    startEpoch = int(file.read())
    print(startEpoch)
checkpoint = torch.load(CHECKPOINT_PATH + f"cnnCheckPoint{startEpoch}.ckpt")
model.load_state_dict(checkpoint["model_state_dict"])
optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
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
        output = model(X)
        # print(output.shape)
        loss = criterion(output, Y)
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
        CHECKPOINT_PATH + f"cnnCheckPoint{epoch}.ckpt",
    )
    with open(CHECKPOINT_PATH + "epoch.log", "w") as file:
        file.write(f"{epoch}")
