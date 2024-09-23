print("project autoCluster")
import torch

print(torch.__version__)
print(torch.cuda.is_available())

import matplotlib.pyplot as plt


def normDist(x, p):
    return torch.norm((x - p), dim=-1)


# autoCluster model setup
import torch
import torch.nn as nn
import torch.nn.functional as F


class autoCluster(nn.Module):
    def __init__(self, x: torch.Tensor, k=2):
        super().__init__()
        self.k = k
        self.pointWeight = nn.Parameter(torch.randn([x.shape[0], k]))
        self.FUN = nn.Softmax(dim=-1)
        self.pointPose = nn.Parameter(
            torch.stack([torch.mean(x, dim=0) for _ in range(k)])
        )
        # print(self.pointPose, self.pointWeight)

    def forward(self, x):
        D = torch.stack(
            [normDist(x, self.pointPose[i, :]) for i in range(self.k)],
            dim=1,
        )
        W = self.FUN(self.pointWeight)
        Wei = torch.sum(self.FUN(self.pointWeight), dim=0)
        imd = torch.einsum("ij,ij->ij", D, W)
        sum = torch.max(imd, dim=0).values
        # print(sum)
        return sum


P = torch.tensor(
    [
        [-0.5, -0.5],
        [0.5, 0.5],
    ],
)
dPList = [
    torch.randn([10, 2]) * 0.1 + P[0, :],
    torch.randn([100, 2]) * 0.1 + P[1, :],
]
dP = torch.concatenate(dPList)

# print(normDist(dP, P[0, :]))
# print(len(P.shape))

# start Train
import torch.optim as optim


K = 2
dP = dP.to("cuda")
KMEAN = autoCluster(dP, K)
KMEAN.to("cuda")
print(dP)
for _ in KMEAN.parameters():
    print(_)
# print(KMEAN(dP))
optimizer = optim.Adam(KMEAN.parameters(), lr=0.001)
for _ in range(2000):
    optimizer.zero_grad()
    ans = torch.max(KMEAN(dP))
    print(ans)
    ans.backward()
    optimizer.step()
    print(ans)

for _ in KMEAN.parameters():
    print(_)

P = KMEAN.pointPose.to("cpu").detach().numpy()
L = KMEAN(dP).to("cpu").detach().numpy()
Wei = torch.sum(KMEAN.FUN(KMEAN.pointWeight), dim=0).to("cpu").detach().numpy()
dP = dP.to("cpu")
fig, ax = plt.subplots(dpi=300)
ax.set_aspect(1.0)
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.scatter(P[:, 1], P[:, 0])
ax.scatter(dP[:, 1], dP[:, 0])
print(L, Wei)
for _ in range(K):
    ax.add_artist(plt.Circle(P[_, :], L[_], fill=False))
ax.scatter(P[:, 1], P[:, 0])
fig.savefig("fig/test200.png")
