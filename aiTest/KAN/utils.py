import torch


class BSpline(torch.nn.Module):
    def __init__(
        self,
        dx: torch.tensor = torch.tensor(1.0),
        weights: int = 100,
    ) -> None:
        super(BSpline, self).__init__()
        self.dx: torch.tensor = dx
        self.weights: torch.tensor = torch.nn.Parameter(torch.ones(weights))
        self.mat: torch.tensor = (
            torch.tensor([[1.0, 4, 1, 0], [-3, 0, 3, 0], [3, -6, 3, 0], [-1, 3, -3, 1]])
            / 6
        )

    def b(self, x):
        return x / (1 + torch.exp(-x))

    def __call__(self, x: torch.tensor) -> torch.tensor:
        n: torch.tensor = torch.floor(x / self.dx).clone().int()
        t: torch.tensor = (x / self.dx - n).clone()
        T: torch.tensor = torch.stack([t**0, t**1, t**2, t**3], dim=1)
        P: torch.tensor = torch.stack(
            [
                self.weights[n - 1],
                self.weights[n - 0],
                self.weights[n + 1],
                self.weights[n + 2],
            ]
        )
        # print(T.shape, self.mat.shape, P.shape)
        return torch.einsum("bi,ij,jb->b", T, self.mat, P)


if __name__ == "__main__":
    F = BSpline(dx=torch.tensor(1))
    # F.init_range(-5, 7)
    # F.weights[0] += 5
    # print(F(torch.tensor(1.0)))
    import matplotlib.pyplot as plt

    def f(x):
        return torch.exp(torch.sin(torch.pi * x))

    X = torch.linspace(-4, 3, 500)
    Y = F(X)
    Yp = f(X)
    # print(X, Y)
    # plt.plot(X.detach().numpy(), Y.detach().numpy())
    # plt.plot(
    #     X.detach().numpy(),
    #     F.weights[torch.floor(X / F.dx).clone().int()].detach().numpy(),
    # )
    # plt.plot(X.detach().numpy(), Yp.detach().numpy())
    # plt.show()

    opt = torch.optim.Adam(F.parameters())
    L = torch.nn.MSELoss()
    for i in range(20000):
        opt.zero_grad()
        Y = F(X)
        l: torch.tensor = L(Y, Yp)
        print(l)
        l.backward(retain_graph=True)
        opt.step()
    plt.plot(X.detach().numpy(), Y.detach().numpy())
    print(
        torch.arange(-4, 3, 1).detach().numpy(),
        torch.concatenate([F.weights[0:3], F.weights[-4:]]).detach().numpy(),
    )
    plt.plot(
        torch.arange(-4, 3, 1).detach().numpy(),
        torch.concatenate([F.weights[-4:], F.weights[0:3]]).detach().numpy(),
    )
    plt.plot(X.detach().numpy(), Yp.detach().numpy())
    plt.show()
