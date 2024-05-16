import model
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt

BATCH_SIZE = 32
net = model.SEQUENCE_CNN().cuda()
opt = torch.optim.Adam(net.parameters(), lr=0.1)
LOSS = nn.MSELoss()
dataset = model.FUL_DAY_DATA("stock_data/SH600008.json", 21)
print(len(dataset))
dataloader = DataLoader(dataset=dataset, batch_size=BATCH_SIZE, shuffle=True)
for epc in range(10000):
    for i, (x, y) in enumerate(dataloader):
        opt.zero_grad()
        z = net(x.view(-1, 6 * 21).to("cuda"))
        # print(z)
        loss = LOSS(z[:, 0], y[:, -1, 0].to("cuda"))
        loss.backward()
        opt.step()
    # # print(y[:, -1], z, sep="\n")
    print(
        epc,
        loss * 100,
        torch.max(torch.abs(y[:, -1, 0] - z.cpu())),
        torch.max(torch.abs(z.cpu())),
        sep="\t",
    )
    plt.plot(x[0, :, 0], "r.-")
    plt.plot(y[0, -1, 0], "b*-")
    plt.plot(z[0].cpu().detach().numpy(), "g*-")
    # plt.plot(y[0, :], "b.-")
    plt.savefig(f"fig/fig{-1}")
    plt.clf()
    torch.save(
        {
            "epoch": epc,
            "model_state_dict": net.state_dict(),
            "optimizer_state_dict": opt.state_dict(),
            "loss": loss,
        },
        f"cnnCheckPoint_test3",
    )
# for i, (x, y) in enumerate(dataloader):
#     break
# for i in range(100000):
#     # print(x, y, sep="\n")
#     # print(y[:, -1, 0], sep="\n")
#     # print(x.size(), x, sep="\n")
#     opt.zero_grad()
#     z = net(x.view(-1, 6 * 21).to("cuda"))
#     # print(z)
#     loss = LOSS(z, y[:, -1, 0].to("cuda"))
#     loss.backward()
#     opt.step()
#     # # print(y[:, -1], z, sep="\n")
#     print(
#         i,
#         loss * 100,
#         torch.max(torch.abs(y[:, -1, 0] - z.cpu())),
#         torch.max(torch.abs(z.cpu())),
#         sep="\t",
#     )
#     plt.plot(x[0, :, 0], "r.-")
#     plt.plot(y[0, -1, 0], "b*-")
#     plt.plot(z[0].cpu().detach().numpy(), "g*-")
#     # plt.plot(y[0, :], "b.-")
#     plt.savefig(f"fig/fig{-1}")
#     plt.clf()
