DATA_ROOT = "./data"
from torchvision import datasets
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt

print("start loading data")
training_data = datasets.FashionMNIST(
    root=DATA_ROOT, train=True, download=True, transform=ToTensor()
)
test_data = datasets.FashionMNIST(
    root=DATA_ROOT, train=False, download=True, transform=ToTensor()
)
print("training_data_len:", len(training_data))
for i, (img, label) in enumerate(training_data):
    print(img.size(), img.squeeze().size())
    plt.title(f"{label}")
    plt.imshow(img.squeeze(), cmap="gray")
    plt.show()
    break
