import model
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt

BATCH_SIZE = 128
net = model.SIMP_LSTM(6, 1024, 1, 4, BATCH_SIZE, 21).cuda()
opt = torch.optim.Adam(net.parameters(), lr=0.01)
LOSS = nn.MSELoss()
dataset = model.FUL_DAY_DATA("stock_data/SH600008.json", 21)
print(len(dataset))
dataloader = DataLoader(
    dataset=dataset, batch_size=BATCH_SIZE, shuffle=True, drop_last=True
)
for epcc in range(1000000000):
    for i, (x, y) in enumerate(dataloader):
        for epc in range(1000000000):
            opt.zero_grad()
            z = net(x.to("cuda"))
            # print(x, y, z, sep="\n")
            # print(x.size(), y.size(), z.size())
            loss = LOSS(z[:, -21:, :], y[:, -21:, 0:1].to("cuda"))
            loss.backward()
            if loss < 1e-5:
                break
            opt.step()
            print(epc, loss)
            plt.plot(x[0, -21:, 0], "r.-")
            plt.plot(y[0, -21:, 0], "b*-")
            plt.plot(z[0, -21:, 0].cpu().detach().numpy(), "g*-")
            # plt.show()
            plt.savefig(f"fig/fig{-1}")
            plt.clf()
            if epc % 1000 == 0:
                for j, (x0, y0) in enumerate(dataloader):
                    pass
                z0 = net(x0.to("cuda"))
                plt.plot(x0[0, :, 0], "r.-")
                plt.plot(y0[0, :, 0], "b*-")
                plt.plot(z0[0, :, 0].cpu().detach().numpy(), "g*-")
                # plt.show()
                plt.savefig(f"fig/fig{-3}")
                plt.clf()
                torch.save(
                    {
                        "epoch": epc,
                        "model_state_dict": net.state_dict(),
                        "optimizer_state_dict": opt.state_dict(),
                        "loss": loss,
                    },
                    f"cnnCheckPoint-1",
                )
# for i, (x, y) in enumerate(dataloader):
#     pass
# z = net(x.to("cuda"))
# loss = LOSS(z, y.to("cuda"))
# loss.backward()
# plt.plot(x[0, :, 0], "r.-")
# plt.plot(y[0, :, 0], "b*-")
# plt.plot(z[0, :, 0].cpu().detach().numpy(), "g*-")
# plt.savefig(f"fig/fig{-2}")
# plt.clf()
# print(
#     epc,
#     loss * 100,
#     torch.max(torch.abs(y[:, -1, 0] - z.cpu())),
#     torch.max(torch.abs(z.cpu())),
#     sep="\t",
# )
# plt.plot(x[0, :, 0], "r.-")
# plt.plot(y[0, -1, 0], "b*-")
# plt.plot(z[0].cpu().detach().numpy(), "g*-")
# # plt.plot(y[0, :], "b.-")
# plt.savefig(f"fig/fig{-1}")
# plt.clf()
# torch.save(
#     {
#         "epoch": epc,
#         "model_state_dict": net.state_dict(),
#         "optimizer_state_dict": opt.state_dict(),
#         "loss": loss,
#     },
#     f"cnnCheckPoint_test3",
# )
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
