import torch
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt
from model import ANN
import torch.optim as optim
import torch.nn as nn

EPOCH_NUM = 2
net = ANN(784, 10, 16, 2).to("cuda")
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr=0.001)


training_data = datasets.FashionMNIST(
    root="data", train=True, download=True, transform=ToTensor()
)

test_data = datasets.FashionMNIST(
    root="data", train=False, download=True, transform=ToTensor()
)

# labels_map = {
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
# figure = plt.figure(figsize=(8, 8))
# cols, rows = 3, 3
# for i in range(1, cols * rows + 1):
#     sample_idx = torch.randint(len(training_data), size=(1,)).item()
#     img, label = training_data[sample_idx]
#     figure.add_subplot(rows, cols, i)
#     plt.title(labels_map[label])
#     plt.axis("off")
#     plt.imshow(img.squeeze(), cmap="gray")
# plt.show()

# print(training_data[sample_idx][0].shape, training_data[sample_idx][1])

from torch.utils.data import DataLoader

train_dataloader = DataLoader(training_data, batch_size=64, shuffle=True)
test_dataloader = DataLoader(test_data, batch_size=64, shuffle=True)

# Display image and label.
# train_features, train_labels = next(iter(train_dataloader))
# print(f"Feature batch shape: {train_features.size()}")
# print(f"Labels batch shape: {train_labels.size()}")
# img = train_features[0].squeeze()
# label = train_labels[0]
# plt.imshow(img, cmap="gray")
# plt.show()
# print(f"Label: {label}")

# print(net.modules)
# print("Model's state_dict:")
# for param_tensor in net.state_dict():
#     print(param_tensor, "\t", net.state_dict()[param_tensor].size())


for epoch in range(EPOCH_NUM):
    runningLoss = 0.0
    cnt = 0
    for trainFeatures, trainLabels in train_dataloader:
        cnt += 1
        runningLoss = 0.0
        for i in range(len(trainFeatures)):
            X = trainFeatures[i].view(-1).to("cuda")
            Y = trainLabels[i].view(-1).to("cuda")

            # print(X.dtype, Y.shape)

            optimizer.zero_grad()
            output = net(X)
            # print(output.view(1, -1), Y)
            loss = criterion(output.view(1, -1), Y)
            loss.backward()
            optimizer.step()

            runningLoss += loss.item()

            # print(X.device, criterion(Y, trainLabels[i].to("cuda")), sep="|-|")
        print(f"[{epoch + 1}, {cnt}] loss: {runningLoss / 64:.3f}")
    torch.save(
        {
            "epoch": epoch,
            "model_state_dict": net.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "loss": loss,
        },
        f"./module/netAndOptimAtEpoch{epoch}",
    )
