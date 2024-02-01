from FCN import FCN
import torch
from torch.autograd.functional import jacobian
from torch.autograd.functional import jvp

F = FCN(4, 6, 1, 0)

print(F.state_dict())

x = torch.rand(4)
print(x)
print(jacobian(F, x))
jacMat=jacobian(F, x)


