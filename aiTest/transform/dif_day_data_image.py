import model
from torch.utils.data import DataLoader
import torch
import matplotlib.pyplot as plt

dataset = model.DIF_DAY_DATA_IMAGE("stock_data/SH600008.json", 21)
print(len(dataset))
dataloader = DataLoader(dataset=dataset, batch_size=1, shuffle=True)
for i, (x, y) in enumerate(dataloader):
    torch.set_printoptions(precision=2, linewidth=1000)
    print(i, x.size(), y.size())
    print(x, y, sep="\n")
    plt.imshow(x[0], cmap="viridis")  # cmap参数指定颜色映射
    plt.colorbar()  # 显示颜色条
    plt.show()
    break
