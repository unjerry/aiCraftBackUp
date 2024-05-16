import numpy as np

dict1 = []

dict1.append({"+/-": 1234, "=": 1234})

np.save("testDict.npy", dict1)

print(dict1)
