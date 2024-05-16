import model
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt

INPUT_SIZE = 1
HIDDEN_SIZE = 16
OUTPUT_SIZE = 1
NUM_LAYER = 1024
BATCH_SIZE = 512
L = 60
net = model.SIMP_RNN(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE, NUM_LAYER, BATCH_SIZE, L)
opt = torch.optim.Adam(net.parameters(), lr=0.1)
LOSS = nn.MSELoss()
dataset = model.DIF_DAY_DATA("stock_data/SH600008.json", L)
print(len(dataset))
dataloader = DataLoader(dataset=dataset, batch_size=BATCH_SIZE, shuffle=True)
for epc in range(10000000):
    for i, (x, y) in enumerate(dataloader):
        opt.zero_grad()
        net.N = x.shape[0]
        ans = net(x)
        loss = LOSS((ans) * 50, (y) * 50)
        loss.backward()
        opt.step()
        print(i, loss, x.shape, len(dataset) // BATCH_SIZE, sep="\t")
        # # plt.gca().set_aspect(1.0)
    # plt.plot(x[0])
    plt.plot(y[0])
    plt.plot(ans[0].detach().numpy(), "r.-")
    plt.savefig(f"fig/fig{epc}")
    plt.clf()
# break
