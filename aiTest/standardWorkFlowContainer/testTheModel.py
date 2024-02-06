import torch
import sys
import importlib
from parameter import CHECKPOINT_PATH, TEST_DATA_LOADER
from parameter import CHECKPOINT_PATH
from parameter import IMG_TEST_PATH
import torch.optim as optim
import torch.nn as nn
import torch

print("start loading data")
sys.path.append(f"{CHECKPOINT_PATH}")
test_data = importlib.import_module(TEST_DATA_LOADER).test_data
print("data load finish")

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
model.eval()


totKind = torch.zeros(10)
correctKind = torch.zeros(10)


correct = 0
for i in range(len(test_data)):
    img, label = test_data[i]
    output = model(img.view(1, 1, 28, 28).to("cuda"))
    act = torch.exp(output)
    lst = act.view(-1).tolist()
    # print(output, act)
    # print(label, lst.index(max(lst)))
    totKind[label] += 1
    if label == lst.index(max(lst)):
        correct += 1
        correctKind[label] += 1
for i in range(10):
    print(f"label:{i}\t|rate:{correctKind[i]/totKind[i]:.2f}")
print("correctRateIs:", correct / len(test_data), sep="")
