from parameter import CHECKPOINT_PATH
import torch
import torch.optim as optim
from cnn import Net

net = Net().to("cuda")
optimizer = optim.Adam(net.parameters(), lr=0.001)
torch.save(
    {
        "epoch": 0,
        "model_state_dict": net.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "loss": None,
    },
    CHECKPOINT_PATH + f"cnnCheckPoint{0}",
)
with open(CHECKPOINT_PATH + "epoch.log", "w") as file:
    file.write(f"{0}")
