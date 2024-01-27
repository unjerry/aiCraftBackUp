from model import ANN
import torch.optim as optim
import torch.nn as nn
import torch

EPOCH = 36
PATH = f"./module/netAndOptimAtEpoch{EPOCH}"


model = ANN(784, 10, 16, 2).to("cuda")
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

checkpoint = torch.load(PATH)
model.load_state_dict(checkpoint["model_state_dict"])
optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
epoch = checkpoint["epoch"]
loss = checkpoint["loss"]
model.eval()

from torchvision import datasets
from torchvision.transforms import ToTensor

test_data = datasets.FashionMNIST(
    root="data", train=False, download=True, transform=ToTensor()
)

import matplotlib.pyplot as plt

labels_map = {
    0: "T-Shirt",
    1: "Trouser",
    2: "Pullover",
    3: "Dress",
    4: "Coat",
    5: "Sandal",
    6: "Shirt",
    7: "Sneaker",
    8: "Bag",
    9: "Ankle Boot",
}

totKind = torch.zeros(10)
correctKind = torch.zeros(10)

figure = plt.figure(figsize=(16, 4))
for i in range(1, 1 + 4):
    img, label = test_data[torch.randint(len(test_data), size=(1,)).item()]
    output = model(img.view(-1).to("cuda"))
    figure.add_subplot(1, 4, i)
    act = torch.exp(output)
    lst = act.tolist()
    # print(output, act)
    plt.title(f"{labels_map[label]}\n{labels_map[lst.index(max(lst))]}")
    plt.axis("off")
    plt.imshow(img.squeeze(), cmap="gray")
plt.show()

correct = 0
for i in range(len(test_data)):
    img, label = test_data[i]
    output = model(img.view(-1).to("cuda"))
    act = torch.exp(output)
    lst = act.tolist()
    # print(output, act)
    # print(label, lst.index(max(lst)))
    totKind[label] += 1
    if label == lst.index(max(lst)):
        correct += 1
        correctKind[label] += 1
for i in range(10):
    print(f"name:{labels_map[i]}\t|rate:{correctKind[i]/totKind[i]:.2f}")
print("correctRateIs:", correct / len(test_data), sep="")
