import torch
from utils import BSpline


class KANTest1(torch.nn.Module):
    def __init__(self) -> None:
        super(KANTest1, self).__init__()
        self.F = BSpline(dx=torch.tensor(1))
        self.R = BSpline(dx=torch.tensor(1))

    def forward(self, x):
        return self.R(self.F(x))


if __name__ == "__main__":
    F = KANTest1()
    import matplotlib.pyplot as plt

    def f(x):
        return torch.sin(torch.pi * x) / x

    X = torch.randn(500)
    X=(X*4).sort().values
    print(X)
    Y = F(X)
    T = F.F(X)
    R = F.R(X)
    Tp = torch.sin(torch.pi * X)
    Rp = torch.exp(X)
    Yp = f(X)
    print(X, Y)
    plt.plot(X.detach().numpy(), Y.detach().numpy())
    plt.plot(X.detach().numpy(), T.detach().numpy())
    plt.plot(X.detach().numpy(), R.detach().numpy())
    plt.plot(X.detach().numpy(), Yp.detach().numpy())
    plt.plot(X.detach().numpy(), Tp.detach().numpy())
    # plt.plot(X.detach().numpy(), Rp.detach().numpy())
    plt.show()

    opt = torch.optim.Adam(F.parameters())
    for i in F.parameters():
        print(i)
    L = torch.nn.MSELoss()
    for i in range(3000):
        opt.zero_grad()
        Y = F(X)
        l: torch.tensor = L(Y, Yp)
        print(l)
        l.backward(retain_graph=True)
        opt.step()
    Y = F(X)
    T = F.F(X)
    R = F.R(X)
    Tp = torch.sin(torch.pi * X)
    Rp = torch.exp(X)
    Yp = f(X)
    print(X, Y)
    plt.plot(X.detach().numpy(), Y.detach().numpy())
    plt.plot(X.detach().numpy(), T.detach().numpy())
    plt.plot(X.detach().numpy(), R.detach().numpy())
    plt.plot(X.detach().numpy(), Yp.detach().numpy())
    plt.plot(X.detach().numpy(), Tp.detach().numpy())
    # plt.plot(X.detach().numpy(), Rp.detach().numpy())
    plt.show()
    for i in F.parameters():
        print(i)
