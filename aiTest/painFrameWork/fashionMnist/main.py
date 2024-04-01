from leastSquareData import learsSquareData
from torch.utils.data import DataLoader
import torch
import torch.optim as optim
from leastSquareModel import Net, Pain
from torchvision import datasets
import torch.nn as nn
from torchvision.transforms import ToTensor


def testTheModel():
    model = Net().to("cuda")
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    with open(CHECKPOINT_PATH + "epoch.log", "r") as file:
        startEpoch = int(file.read())
        print(startEpoch)

    checkpoint = torch.load(CHECKPOINT_PATH + f"cnnCheckPoint{startEpoch}")

    model.load_state_dict(checkpoint["model_state_dict"])
    epoch = checkpoint["epoch"]
    loss = checkpoint["loss"]
    model.eval()

    from torchvision import datasets
    from torchvision.transforms import ToTensor

    test_data = datasets.FashionMNIST(
        root="data", train=False, download=True, transform=ToTensor()
    )

    import matplotlib.pyplot as plt

    labels_map = {
        0: "T-Shirt",
        1: "Trouser",
        2: "Pullover",
        3: "Dress",
        4: "Coat",
        5: "Sandal",
        6: "Shirt",
        7: "Sneaker",
        8: "Bag",
        9: "Ankle Boot",
    }

    totKind = torch.zeros(10)
    correctKind = torch.zeros(10)

    figure = plt.figure(figsize=(16, 4))
    for i in range(1, 1 + 4):
        img, label = test_data[torch.randint(len(test_data), size=(1,)).item()]
        output = model(img.view(1, 1, 28, 28).to("cuda"))
        figure.add_subplot(1, 4, i)
        act = torch.exp(output)
        lst = act.view(-1).tolist()
        print(lst)
        plt.title(f"{labels_map[label]}\n{labels_map[lst.index(max(lst))]}")
        plt.axis("off")
        plt.imshow(img.squeeze(), cmap="gray")
    plt.savefig(IMG_TEST_PATH)

    correct = 0
    for i in range(len(test_data)):
        img, label = test_data[i]
        output = model(img.view(1, 1, 28, 28).to("cuda"))
        act = torch.exp(output)
        lst = act.view(-1).tolist()
        # print(output, act)
        # print(label, lst.index(max(lst)))
        totKind[label] += 1
        if label == lst.index(max(lst)):
            correct += 1
            correctKind[label] += 1
    for i in range(10):
        print(f"name:{labels_map[i]}\t|rate:{correctKind[i]/totKind[i]:.2f}")
    print("correctRateIs:", correct / len(test_data), sep="")


def startTrain(dataLoader, epoch, CHECKPOINT_PATH):
    with open(CHECKPOINT_PATH + "epoch.log", "r") as file:
        startEpoch = int(file.read())
        print(startEpoch)
    model = Net().to("cuda")
    pian = Pain().to("cuda")
    model_optimizer = optim.Adam(model.parameters(), lr=0.001)
    pian_optimizer = optim.Adam(pian.parameters(), lr=0.001)
    checkpoint = torch.load(CHECKPOINT_PATH + f"cnnCheckPoint{startEpoch}")
    model.load_state_dict(checkpoint["model_state_dict"])
    pian.load_state_dict(checkpoint["pian_state_dict"])
    pian_optimizer.load_state_dict(checkpoint["pian_optimizer_state_dict"])
    model_optimizer.load_state_dict(checkpoint["model_optimizer_state_dict"])
    st = checkpoint["epoch"]
    loss = checkpoint["loss"]
    model.train()
    criterion = nn.CrossEntropyLoss()
    painc = nn.MSELoss()
    # for it in model.parameters():
    #     print(it)
    # for it in pian.parameters():
    #     print(it)
    # dataLoader = dataLoader.to("cuda")
    for j in range(st + 1, st + 1 + epoch):
        for i, item in enumerate(dataLoader):
            pian_optimizer.zero_grad()
            model_optimizer.zero_grad()
            X, Y = item
            X = X.to("cuda")
            Y = Y.to("cuda")
            ## print(i, X, Y)
            y = model(X)
            # print(y.shape,Y.shape)
            pain = pian(torch.concatenate((y, Y.view(-1, 1)), dim=1))
            tpain = torch.vmap(criterion)(y, Y.view(-1))
            loss = painc(tpain.view(-1), pain.view(-1)) + torch.sum(pain)
            loss.backward()
            pian_optimizer.step()
            model_optimizer.step()

            ## print(X,model(X),Y)
            # print(i, loss.tolist(), torch.sum(pain).tolist())
        print(j, loss.tolist(), torch.sum(pain).tolist())
        torch.save(
            {
                "epoch": j,
                "model_state_dict": model.state_dict(),
                "pian_state_dict": pian.state_dict(),
                "pian_optimizer_state_dict": pian_optimizer.state_dict(),
                "model_optimizer_state_dict": model_optimizer.state_dict(),
                "loss": loss,
            },
            CHECKPOINT_PATH + f"cnnCheckPoint{j}",
        )
        with open(CHECKPOINT_PATH + "epoch.log", "w") as file:
            file.write(f"{j}")


def setUpModel():
    pian = Pain().to("cuda")
    model = Net().to("cuda")
    # print(pian.parameters(), model.parameters())
    pian_optimizer = optim.Adam(pian.parameters(), lr=0.001)
    model_optimizer = optim.Adam(model.parameters(), lr=0.001)
    torch.save(
        {
            "epoch": 0,
            "model_state_dict": model.state_dict(),
            "pian_state_dict": pian.state_dict(),
            "pian_optimizer_state_dict": pian_optimizer.state_dict(),
            "model_optimizer_state_dict": model_optimizer.state_dict(),
            "loss": None,
        },
        CHECKPOINT_PATH + f"cnnCheckPoint{0}",
    )
    with open(CHECKPOINT_PATH + "epoch.log", "w") as file:
        file.write(f"{0}")


if __name__ == "__main__":
    print("hello, world!")
    with open("commandHelpFile", "r") as file:
        chf = file.read()
    data = datasets.FashionMNIST(
        root="data", train=True, download=True, transform=ToTensor()
    )
    dataLoader = DataLoader(dataset=data, batch_size=1024, shuffle=True)
    CHECKPOINT_PATH = "./checkPoint/"
    IMG_TEST_PATH = "pic/pic.png"
    MODEL_PATH = ""
    while True:
        cmd = input(chf)
        if cmd == "q":
            break
        if cmd == "start":
            ep = int(input("EPOCHNUM:"))
            startTrain(
                dataLoader=dataLoader,
                epoch=ep,
                CHECKPOINT_PATH=CHECKPOINT_PATH,
            )
        if cmd == "setup":
            setUpModel()
        if cmd == "test":
            testTheModel()
