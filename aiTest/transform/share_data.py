import torch
import json
import torch.nn as nn
import math

share_data = {}
with open("stock_data/SH600008.json", "rb") as ipf:
    share_data = json.load(ipf)

print(share_data)
print(share_data.keys())
print(len(share_data["item"]))
print(share_data["symbol"])
print(share_data["column"])
# print(share_data["item"][:3][:2])
share_data_2_6 = [it[2:6] for it in share_data["item"]]
# print(share_data_2_6)
share_data_tensor = torch.tensor(share_data_2_6)
print(share_data_tensor.shape)


s = 10
share_data_tensor_0_s = share_data_tensor[:s, :]
share_data_tensor_s = share_data_tensor[s, :]
print(share_data_tensor_0_s)
print(share_data_tensor_0_s.shape)
print(share_data_tensor_s)
print(share_data_tensor_s.shape)


class TRANS(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.W_E = nn.Linear(4, 32, bias=False)

    def forward(self, x):
        return self.W_E(x)


soft_max = nn.Softmax(0)
mselos = nn.MSELoss()
print(soft_max(torch.tensor([1.0, 2.0])))
L = nn.Linear(4, 32, bias=False)
UL = nn.Linear(32, 4, bias=False)
W_Q = nn.Linear(32, 16, bias=False)
W_K = nn.Linear(32, 16, bias=False)
W_V_down = nn.Linear(32, 16, bias=False)
W_V_up = nn.Linear(16, 32, bias=False)

embedding = L(share_data_tensor_0_s)
quesin = torch.randn([10, 32, 64], requires_grad=True)
quesout = torch.randn([10, 64, 32], requires_grad=True)
Q = W_Q(embedding)
K = W_K(embedding)
V = W_V_up(W_V_down(embedding))
C = torch.einsum("ik,jk->ji", Q, K)
print("E", embedding.shape)
print("Q", Q.shape)
print("K", K.shape)
print("V", V.shape)
print("C", C.shape)

for i, row in enumerate(C):
    # print(i, row)
    for k in range(i):
        C[i][k] += float("-inf")
soft_C = soft_max(C)

DE = torch.einsum("ij,ik->kj", V, soft_C)
print("DE", DE.shape)

E2 = embedding + DE

E2p = torch.einsum("nj,nji,nik->nk", E2, quesin, quesout)

print("E2p", E2p.shape)


loss = mselos(UL(E2p[9]), share_data_tensor_s)
print(loss)
loss.backward()
print(L.gradient())


def print_tensor(filename, tensor):
    with open(filename, "w") as file:
        torch.set_printoptions(precision=2, linewidth=1000)
        file.write(f"{tensor}")


print_tensor("E", embedding)
print_tensor("Q", Q)
print_tensor("K", K)
print_tensor("C", C)
print_tensor("V", V)
print_tensor("soft_C", soft_C)
print_tensor("DE", DE)
print_tensor("E2", E2)
print_tensor("E2p", E2p)
