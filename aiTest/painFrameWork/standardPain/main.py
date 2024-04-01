from leastSquareData import learsSquareData
from torch.utils.data import DataLoader
import torch
import torch.optim as optim
from leastSquareModel import Net, Pain
import torch.nn as nn


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
    criterion = nn.MSELoss()
    for it in model.parameters():
        print(it)
    # for it in pian.parameters():
    #     print(it)
    # dataLoader = dataLoader.to("cuda")
    for j in range(st + 1, st + 1 + epoch):
        for i, item in enumerate(dataLoader):
            pian_optimizer.zero_grad()
            model_optimizer.zero_grad()
            X, Y = item
            ## print(i, X, Y)
            y = model(X)
            # print(y.shape,Y.shape)
            pain = pian(torch.concatenate((y, Y), dim=1))
            tpain = torch.vmap(criterion)(y, Y)
            loss = criterion(tpain, pain) + torch.sum(pain)
            loss.backward()
            pian_optimizer.step()
            model_optimizer.step()

            ## print(X,model(X),Y)
            print(i, loss.tolist(), torch.sum(pain).tolist())
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
    data = learsSquareData("dataFile.in")
    dataLoader = DataLoader(dataset=data, batch_size=9, shuffle=True)
    CHECKPOINT_PATH = "./checkPoint/"
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
