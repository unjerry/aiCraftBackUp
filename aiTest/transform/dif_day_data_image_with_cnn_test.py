import model
from torch.utils.data import DataLoader
import torch
import matplotlib.pyplot as plt
import math

net = model.CNN()
LOSS = torch.nn.CrossEntropyLoss()
opt = torch.optim.Adam(net.parameters(), lr=0.001)

checkpoint = torch.load("cnnCheckPointCNN")
net.load_state_dict(checkpoint["model_state_dict"])
opt.load_state_dict(checkpoint["optimizer_state_dict"])
epoch = checkpoint["epoch"]
loss = checkpoint["loss"]
net.eval()

dataset = model.DIF_DAY_DATA_IMAGE_TEST("stock_data/SH600008.json", 21)
print(len(dataset))
dataloader = DataLoader(dataset=dataset, batch_size=1, shuffle=True)
cnt = 0
for epc in range(1):
    for i, (x, y) in enumerate(dataloader):
        # print(x.size(), y.size())
        # break
        # for i in range(100000000000000000):
        torch.set_printoptions(precision=5, linewidth=1000)
        z = net(x)
        loss = LOSS(z, y)
        ans = 0
        z = torch.nn.functional.softmax(z, dim=1)
        for it in range(len(z[0])):
            # print(z.size())
            ans += it * z[0][it]
        print(i, loss, y, ans, sep="\t")
        if math.fabs(y - ans) < 1.0:
            cnt += 1
        # print(
        #     # epc,
        #     # x.size(),
        #     # y.size(),
        #     # z.size(),
        #     y,
        #     # torch.concatenate([x[0], z[0:].cpu().detach()]).size(),
        # )
        # print(x, y, z,torch.concatenate([x[0], z.cpu().detach()]), sep="\n")
        # plt.imshow(
        #     torch.concatenate([x[0, 0], z[0][None, :].cpu().detach()]), cmap="viridis"
        # )  # cmap参数指定颜色映射
        # plt.colorbar()  # 显示颜色条
        # plt.show()
    # plt.imshow(z.cpu().detach().numpy(), cmap="viridis")  # cmap参数指定颜色映射
    # plt.colorbar()  # 显示颜色条
    # plt.show()
    # torch.save(
    #     {
    #         "epoch": epc,
    #         "model_state_dict": net.state_dict(),
    #         "optimizer_state_dict": opt.state_dict(),
    #         "loss": loss,
    #     },
    #     f"cnnCheckPointCNN",
    # )
    # break
print(cnt / len(dataset))
