import model
from torch.utils.data import DataLoader
import torch
import matplotlib.pyplot as plt

net = model.CNN()
opt = torch.optim.Adam(net.parameters(), lr=0.0005)
LOSS = torch.nn.CrossEntropyLoss()

checkpoint = torch.load("cnnCheckPointCNN")
net.load_state_dict(checkpoint["model_state_dict"])
opt.load_state_dict(checkpoint["optimizer_state_dict"])
epoch = checkpoint["epoch"]
loss = checkpoint["loss"]
net.train()

dataset = model.DIF_DAY_DATA_IMAGE_TRAIN("stock_data/SH600008.json", 21)
print(len(dataset))
dataloader = DataLoader(dataset=dataset, batch_size=128, shuffle=True)
for epc in range(101):
    for i, (x, y) in enumerate(dataloader):
        # print(x.size(), y.size())
        # break
        # for i in range(100000000000000000):
        torch.set_printoptions(precision=5, linewidth=1000)
        opt.zero_grad()
        # print(x.size())
        z = net(x)
        loss = LOSS(z, y)
        loss.backward()
        opt.step()
    print(epc, loss, sep="\t")
    if (epc) % 100 == 0:
        z = torch.nn.functional.softmax(z, dim=1)
        print(
            epc,
            x.size(),
            y.size(),
            z.size(),
            y[0],
            # torch.concatenate([x[0], z[0:].cpu().detach()]).size(),
        )
        # print(x, y, z,torch.concatenate([x[0], z.cpu().detach()]), sep="\n")
        plt.imshow(
            torch.concatenate([x[0, 0], z[0][None, :].cpu().detach()]), cmap="viridis"
        )  # cmap参数指定颜色映射
        plt.colorbar()  # 显示颜色条
        plt.savefig(f"fig_seq")
        plt.clf()
        # plt.show()
        plt.imshow(z.cpu().detach().numpy(), cmap="viridis")  # cmap参数指定颜色映射
        plt.colorbar()  # 显示颜色条
        plt.savefig(f"fig_prid")
        plt.clf()
        torch.save(
            {
                "epoch": epc,
                "model_state_dict": net.state_dict(),
                "optimizer_state_dict": opt.state_dict(),
                "loss": loss,
            },
            f"cnnCheckPointCNN",
        )
        # break
