from model import ANN
import torch.optim as optim
import torch.nn as nn
import torch

BATCH_SIZE = 64
EPOCH = 26
PATH = f"./module/netAndOptimAtEpoch{EPOCH}"

EPOCH_NUM = 100
model = ANN(784, 10, 16, 2).to("cuda")
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

checkpoint = torch.load(PATH)
model.load_state_dict(checkpoint["model_state_dict"])
optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
epoch = checkpoint["epoch"]
loss = checkpoint["loss"]
model.train()


from torchvision import datasets
from torchvision.transforms import ToTensor

training_data = datasets.FashionMNIST(
    root="data", train=True, download=True, transform=ToTensor()
)
test_data = datasets.FashionMNIST(
    root="data", train=False, download=True, transform=ToTensor()
)
from torch.utils.data import DataLoader

train_dataloader = DataLoader(training_data, batch_size=BATCH_SIZE, shuffle=True)
test_dataloader = DataLoader(test_data, batch_size=BATCH_SIZE, shuffle=True)


for epoch in range(epoch + 1, epoch + 1 + EPOCH_NUM):
    cnt = 0
    for trainFeatures, trainLabels in train_dataloader:
        cnt += 1
        runningLoss = torch.tensor(0.0, requires_grad=True).to("cuda")
        X = trainFeatures.to("cuda")
        Y = trainLabels.to("cuda")
        optimizer.zero_grad()
        LEN=len(trainFeatures)
        for i in range(LEN):
            # print(X.dtype, Y.shape)

            output = model(X[i].view(-1))
            # print(output.view(1, -1), Y)
            loss = criterion(output.view(1, -1), Y[i].view(-1)) / LEN
            loss.backward()
            runningLoss += loss

            # print(X.device, criterion(Y, trainLabels[i].to("cuda")), sep="|-|")
        optimizer.step()
        print(f"[{epoch + 1}, {cnt}] loss: {runningLoss:.3f}")
        del runningLoss
    torch.save(
        {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "loss": loss,
        },
        f"./module/netAndOptimAtEpoch{epoch}",
    )
