import torch.optim as optim
import torch


stx = [0, 2, 1]
sty = [1, 2, 7]


import matplotlib.pyplot as plt

cl0 = 0.1 * torch.randn((20, 2))
for i in range(20):
    cl0[i][0] += stx[0]
    cl0[i][1] += sty[0]
print(cl0)
cl1 = 0.1 * torch.randn((100, 2))
for i in range(100):
    cl1[i][0] += stx[1]
    cl1[i][1] += sty[1]
print(cl1)
cl2 = 0.1 * torch.randn((50, 2))
for i in range(50):
    cl2[i][0] += stx[2]
    cl2[i][1] += sty[2]
print(cl2)


plt.scatter(stx, sty)
plt.scatter(cl0[:, 0].detach().numpy(), cl0[:, 1].detach().numpy(), c="red")
plt.scatter(cl1[:, 0].detach().numpy(), cl1[:, 1].detach().numpy(), c="green")
plt.scatter(cl2[:, 0].detach().numpy(), cl2[:, 1].detach().numpy(), c="blue")
plt.show()


dt = torch.concatenate([cl0, cl1, cl2], dim=0)

plt.scatter(dt[:, 0].detach().numpy(), dt[:, 1].detach().numpy(), c="red")
plt.show()


W = torch.randn((170, 3), requires_grad=True)
opt = torch.optim.Adam([W], lr=0.001)
for i in range(100000):

    opt.zero_grad

    stdW = torch.nn.Softmax(dim=1)(W)
    # print(W[:5, :])
    # print(stdW[:5, :])
    mean = torch.einsum("ij,ik->jk", stdW, dt)
    # print(dt)
    # print(mean[:, :])
    sum = torch.einsum("ij->j", stdW)
    # print(sum)
    tmea = torch.einsum("jk,j->jk", mean, 1 / sum)
    totm = torch.einsum("jk,i->ijk", tmea, torch.ones(len(dt)))
    # print(tmea)
    # print(totm[:7,:,:])
    orig = torch.einsum("ik,j->ijk", dt, torch.ones(3))
    # print(orig[:7,:,:])
    deva = torch.einsum("ijk,ij,j->", (tmea - orig) ** 2, stdW, 1 / sum)
    print(i, deva)
    deva.backward()
    opt.step()

    if i % 5000 == 0:
        with open("fi", "w") as file:
            file.write(f"{torch.concatenate([stdW,dt],dim=1)}{i//5000}")
