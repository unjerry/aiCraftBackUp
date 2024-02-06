import torch
import torch.optim as optim
import sys
import importlib
from parameter import CHECKPOINT_PATH

sys.path.append(f"{CHECKPOINT_PATH}")
Net = importlib.import_module(f"model").Net

net = Net()
optimizer = optim.Adam(net.parameters(), lr=0.001)
torch.save(
    {
        "epoch": 0,
        "model_state_dict": net.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "loss": None,
    },
    CHECKPOINT_PATH + f"cnnCheckPoint{0}.ckpt",
)
with open(CHECKPOINT_PATH + "epoch.log", "w") as file:
    file.write(f"{0}")
