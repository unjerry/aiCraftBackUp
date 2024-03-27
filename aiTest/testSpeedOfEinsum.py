import torch


A_cpu = torch.randn([int(1e4), int(1e4)])
B_cpu = torch.randn([int(1e4), int(1e4)])
A_gpu = torch.randn([int(1e4), int(1e4)], device="cuda")
B_gpu = torch.randn([int(1e4), int(1e4)], device="cuda")


import time

print("cpu multi:")
startTime = time.time()
C_cpu = torch.einsum("ij,ik->jk", A_cpu, B_cpu)
endTime = time.time()
print(startTime - endTime)

print("gpu multi:")
startTime = time.time()
C_gpu = torch.einsum("ij,ik->jk", A_gpu, B_gpu)
endTime = time.time()
print(startTime - endTime)


print("cpu multi:")
startTime = time.time()
C_cpu = torch.einsum("ij,ik->jk", A_cpu, B_cpu)
endTime = time.time()
print(startTime - endTime)

print("gpu multi:")
startTime = time.time()
C_gpu = torch.einsum("ij,ik->jk", A_gpu, B_gpu)
endTime = time.time()
print(startTime - endTime)


print("A_cpu", A_cpu.device)
print("B_cpu", B_cpu.device)
print("A_gpu", A_gpu.device)
print("B_gpu", B_gpu.device)
