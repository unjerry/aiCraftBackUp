import pyglet
import numpy as np
from MonoBookingManifest import *
import pyglet.resource
import sys, os

print(sys.path, os.path.dirname(__file__))

margin = 10

if getattr(sys, "frozen", False):
    absPath = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    absPath = os.path.dirname(os.path.abspath(__file__))
print(absPath)
fileList = os.listdir(absPath)
print(fileList)
# ruleFilePath = os.path.join(absPath,fileList)
# class UniLedger:
#     pass


class Transaction:
    def __init__(self, amount, date, accountname, expl="Default") -> None:
        self.amount: int = amount
        self.explanation: str = expl
        self.date: str = date
        self.accountname: str = accountname

    def __str__(self) -> str:
        return f"<amount={self.amount},date={self.date},accountname={self.accountname},exp={self.explanation}>"


class UniLedger:
    def __init__(self, filename: str) -> None:
        self.file: str = filename
        self.data: dict[int, Transaction] | dict = self.load()

    def save(self) -> None:
        np.save(self.file, self.data)

    def load(self) -> dict[int, Transaction] | dict:
        try:
            dt = np.load(self.file, allow_pickle=True).item()
            dt["self.currentId"]
        except:
            dt = {}
            dt["self.currentId"] = 0
        return dt

    def add(self, trans: Transaction) -> None:
        self.data[self.data["self.currentId"]] = trans
        self.data["self.currentId"] += 1
        self.save()

    def export_list(self) -> None:
        for k, v in self.data.items():
            print(k, v)


class Account:
    def __init__(self, filename: str, accountname: str, uni: UniLedger) -> None:
        self.filename: str = filename
        self.accountname: str = accountname
        self.uni: UniLedger = uni
        self.transactionIdList: list[Transaction] | list = self.load()
        print(self.transactionIdList)

    def save(self) -> None:
        print(self.transactionIdList)
        np.save("./Accounts/"+self.filename, self.transactionIdList)

    def load(self) -> list[Transaction] | list:
        print(self.accountname, self.filename)
        try:
            print("dt")
            dt = np.load("./Accounts/"+self.filename, allow_pickle=True).tolist()
            print(dt)
            # dt["self.currentId"]
        except:
            print("lksdjf")
            dt = []
            # dt["self.currentId"] = 0
        return dt


class AccountTrueWindow(pyglet.window.Window):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name: str = name
        self.account: Account = Account(name + ".npy", name, UniData)
        self.switch_to()
        self.batch: pyglet.graphics.Batch = pyglet.graphics.Batch()
        self.bias = 0
        self.lableList: list[pyglet.text.Label] = self.generateList()

        @self.event
        def on_draw():
            self.clear()
            self.lableList = self.generateList()
            self.render()

        @self.event
        def on_mouse_scroll(x, y, scroll_x, scroll_y):
            print("self Mouse scrolled", x, y, scroll_x, scroll_y)
            self.bias -= scroll_y

    def render(self) -> None:
        self.batch.draw()

    def generateList(self) -> list[pyglet.text.Label]:
        return [
            pyglet.text.Label(
                f"{self.account.accountname}",
                font_name="Times New Roman",
                font_size=20,
                x=0,
                y=(len(self.account.transactionIdList) + self.bias) * 20,
                color=(255, 255, 0, 255),
                anchor_x="left",
                anchor_y="bottom",
                batch=self.batch,
            )
        ] + [
            pyglet.text.Label(
                (
                    self.account.uni.data[self.account.transactionIdList[i]].date
                    + f":ammount-explain:{self.account.uni.data[self.account.transactionIdList[i]].explanation}:"
                    + (
                        ""
                        if self.account.uni.data[
                            self.account.transactionIdList[i]
                        ].amount
                        > 0
                        else "\t\t"
                    )
                    + f"{self.account.uni.data[self.account.transactionIdList[i]].amount}"
                ),
                font_name="Times New Roman",
                font_size=20,
                x=0,
                y=(len(self.account.transactionIdList) - 1 - i + self.bias) * 20,
                color=(255, 255, 0, 255),
                anchor_x="left",
                anchor_y="bottom",
                batch=self.batch,
            )
            for i in range(len(self.account.transactionIdList))
        ]


class AccountWindow:
    def __init__(
        self,
        account: Account,
        batch: pyglet.graphics.Batch,
        window: pyglet.window.Window,
    ):
        self.account: Account = account
        self.batch: pyglet.graphics.Batch = batch
        self.window: pyglet.window.Window = window
        self.window.switch_to()
        self.bias = 0
        self.lableList: list[pyglet.text.Label] = self.generateList()

    def render(self) -> None:
        self.batch.draw()

    def generateList(self) -> list[pyglet.text.Label]:
        return [
            pyglet.text.Label(
                f"{self.account.accountname}",
                font_name="Times New Roman",
                font_size=20,
                x=0,
                y=(len(self.account.transactionIdList) + self.bias) * 20,
                color=(255, 255, 0, 255),
                anchor_x="left",
                anchor_y="bottom",
                batch=self.batch,
            )
        ] + [
            pyglet.text.Label(
                (
                    self.account.uni.data[self.account.transactionIdList[i]].date
                    + ":ammount:"
                    + (
                        ""
                        if self.account.uni.data[
                            self.account.transactionIdList[i]
                        ].amount
                        > 0
                        else "\t\t"
                    )
                    + f"{self.account.uni.data[self.account.transactionIdList[i]].amount}"
                ),
                font_name="Times New Roman",
                font_size=20,
                x=0,
                y=(len(self.account.transactionIdList) - 1 - i + self.bias) * 20,
                color=(255, 255, 0, 255),
                anchor_x="left",
                anchor_y="bottom",
                batch=self.batch,
            )
            for i in range(len(self.account.transactionIdList))
        ]


UniData = UniLedger(UniLedgeName)
# UniData.add(103, "2024-05-25")
UniData.export_list()

window = pyglet.window.Window(resizable=True, width=400)
# Twindow = pyglet.window.Window(resizable=True, width=600)
window.switch_to()
batch = pyglet.graphics.Batch()
pyglet.resource.path = [f"{absPath}", ".", f"{os.path.dirname(__file__)}", *sys.path]
pyglet.resource.reindex()
print(pyglet.resource.path)
# pyglet.resource.add_path("./artAssets")
ball_image = pyglet.image.load("./artAssets/but.png")
print(type(ball_image))
# ball = pyglet.sprite.Sprite(ball_image, x=50, y=50, batch=batch)

pressed_img = pyglet.resource.image("artAssets/greenPress.png")
depressed_img = pyglet.resource.image("artAssets/greenRelease.png")
print(type(pressed_img))
pressed_img.height = 40
pressed_img.width = 40
depressed_img.height = 40
depressed_img.width = 40
# print(pressed_img.height)
pushbutton = pyglet.gui.PushButton(
    x=100 + margin,
    y=0 + margin,
    pressed=pressed_img,
    depressed=depressed_img,
    batch=batch,
)
# datepushbutton = pyglet.gui.PushButton(
#     x=350, y=20, pressed=pressed_img, depressed=depressed_img, batch=batch
# )

UniAccountNameDict: dict[str, Account] = {}


def my_on_press_handler():
    print(txen.value, type(txen.value))
    try:
        amt = int(txen.value)
        dat = datetxen.value
    except:
        print("null value")
        return
    # sdf=Transaction(amt)
    try:
        print("dat", dat, UniAccountNameDict[dat].accountname)
        UniAccountNameDict[dat].transactionIdList.append(UniData.data["self.currentId"])
        UniAccountNameDict[dat].save()
        UniData.add(Transaction(amt, "20240525", dat))
        print("Button Pressed!")
    except:
        print("null account")
        return
    txen.value = "amount"
    # datetxen.value = "CashAccount"
    UniData.export_list()


def my_on_release_handler():
    pass
    # print("Button Released...")


pushbutton.set_handler("on_press", my_on_press_handler)
pushbutton.set_handler("on_release", my_on_release_handler)
window.push_handlers(pushbutton)

# sliddd=pyglet.gui.Slider(100,100,pressed_img,depressed_img,100,batch=batch)
# window.push_handlers(sliddd)
# window.push_handlers(datepushbutton)


def commmm(strr: str):
    print("commmmmm:" + strr)


def datecommmm(strr: str):
    print("datecomm:" + strr)


txen = pyglet.gui.TextEntry("amount", 0 + margin, 0 + margin, 100, batch=batch)
datetxen = pyglet.gui.TextEntry(
    "CertainAccount", 0 + margin, 20 + margin, 100, batch=batch
)
txen.set_handler("on_commit", commmm)
datetxen.set_handler("on_commit", datecommmm)
window.push_handlers(txen)
window.push_handlers(datetxen)


@window.event
def on_draw():
    window.clear()
    batch.draw()


# Twindow.switch_to()
# tbatch = pyglet.graphics.Batch()
# acc = Account("CashAccount.npy", "CashAccount", UniData)
# UniAccountNameDict[acc.accountname] = acc
# accwin = AccountWindow(acc, tbatch, Twindow)


# @Twindow.event
# def on_draw():
#     Twindow.clear()
#     accwin.lableList = accwin.generateList()
#     accwin.render()


# @Twindow.event
# def on_mouse_scroll(x, y, scroll_x, scroll_y):
#     print("Mouse scrolled", x, y, scroll_x, scroll_y)
#     accwin.bias -= scroll_y


tmpwin = AccountTrueWindow("NewAccount", resizable=True, width=600)
UniAccountNameDict[tmpwin.account.accountname] = tmpwin.account
print(UniAccountNameDict)
caswin = AccountTrueWindow("CashAccount", resizable=True, width=600)
UniAccountNameDict[caswin.account.accountname] = caswin.account
print(UniAccountNameDict)


pyglet.app.run()
