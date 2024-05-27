import pyglet
import numpy as np
from MonoBookingManifest import *
import pyglet.resource
import sys, os
import json
import datetime

with open("MonoBookingdoubleCounting.json", "r") as file:
    manifestJsonDict: dict = json.load(file)

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
        np.save("./Accounts/" + self.filename, self.transactionIdList)

    def load(self) -> list[Transaction] | list:
        print(self.accountname, self.filename)
        try:
            print("dt")
            dt = np.load("./Accounts/" + self.filename, allow_pickle=True).tolist()
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
        self.set_caption(name)

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
                    + f":explain:{self.account.uni.data[self.account.transactionIdList[i]].explanation}:"
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


class Profile:
    def __init__(self) -> None:
        self.netIcome = 100


class ProfileWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cashFlow = pyglet.gui.TextEntry(
            "cashFLow", 0 + margin, 0 + margin, 100, batch=batch
        )


class CharaLabel:
    def __init__(
        self, window: pyglet.window.Window, batch: pyglet.graphics.Batch
    ) -> None:
        self.currentDisplay: int = 0
        self.window: pyglet.window.Window = window
        self.batch: pyglet.graphics.Batch = batch
        self.nameList: list[str] = [
            "artAssets/Chara_PAYDAY.png",
            "artAssets/Chara_DEAL.png",
        ]
        self.ExplanList: list[str] = [
            "artAssets/PAYDAY_EXPLAIN.png",
            "artAssets/DEAL_EXPLAIN.png",
        ]
        self.CharaList: list[pyglet.sprite.Sprite] = self.generate()
        self.ExpanList: list[pyglet.sprite.Sprite] = self.genExp()

    def genExp(self) -> list[pyglet.sprite.Sprite]:
        lis = [
            pyglet.sprite.Sprite(
                pyglet.resource.image(it),
                x=0 + margin,
                y=window.height - margin - 64,
                batch=batch,
            )
            for it in self.ExplanList
        ]
        for spr in lis:
            spr.y -= spr.height
            spr.visible = False
        lis[self.currentDisplay].visible = True
        return lis

    def generate(self) -> list[pyglet.sprite.Sprite]:
        lis = [
            pyglet.sprite.Sprite(
                pyglet.resource.image(it),
                x=0 + margin,
                y=window.height - margin,
                batch=batch,
            )
            for it in self.nameList
        ]
        for spr in lis:
            spr.y -= spr.height
            spr.visible = False
        lis[self.currentDisplay].visible = True
        return lis

    def changeChara(self):
        rand = np.random.uniform()
        print(rand, type(rand))
        self.CharaList[self.currentDisplay].visible = False
        self.ExpanList[self.currentDisplay].visible = False
        if rand < 0.1:
            self.currentDisplay = 0
        else:
            self.currentDisplay = 1
        self.ExpanList[self.currentDisplay].visible = True
        self.CharaList[self.currentDisplay].visible = True


UniData = UniLedger(UniLedgeName)
# UniData.add(103, "2024-05-25")
UniData.export_list()
UniAccountNameDict: dict[str, Account] = {}

window = pyglet.window.Window(width=400)
accountwindows: list[AccountTrueWindow] = []
for accountName in manifestJsonDict["Accounts"]:
    tmp = AccountTrueWindow(accountName, resizable=True, width=600)
    accountwindows.append(tmp)
    UniAccountNameDict[tmp.account.accountname] = tmp.account
    print(UniAccountNameDict)
    tmp.close()
window.set_caption("worldLine MonoBookingdoubleCounting")
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

backgroung_image: pyglet.image.ImageData = pyglet.image.load("artAssets/Designer3.png")

# image = pyglet.resource.image("artAssets/Chara_PAYDAY.png")
# sprite = pyglet.sprite.Sprite(
#     image, x=0 + margin, y=window.height - margin, batch=batch
# )
# sprite.y -= sprite.height
charaLabel = CharaLabel(window, batch)
playerTest = Profile()

pressed_img = pyglet.resource.image("artAssets/greenPress.png")
depressed_img = pyglet.resource.image("artAssets/greenRelease.png")
check_pressed_img = pyglet.resource.image("artAssets/checksPressed.png")
check_depressed_img = pyglet.resource.image("artAssets/checks.png")
batsu_pressed_img = pyglet.resource.image("artAssets/batsuPressed.png")
batsu_depressed_img = pyglet.resource.image("artAssets/batsu.png")
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
check_pushbutton = pyglet.gui.PushButton(
    x=128 + margin,
    y=window.height - margin,
    pressed=check_pressed_img,
    depressed=check_depressed_img,
    batch=batch,
)
check_pushbutton.y -= check_pushbutton.height
batsu_pushbutton = pyglet.gui.PushButton(
    x=128 + margin + 64,
    y=window.height - margin,
    pressed=batsu_pressed_img,
    depressed=batsu_depressed_img,
    batch=batch,
)
batsu_pushbutton.y -= batsu_pushbutton.height
# datepushbutton = pyglet.gui.PushButton(
#     x=350, y=20, pressed=pressed_img, depressed=depressed_img, batch=batch
# )


def checks_on_press():
    # charaLabel.CharaList[0].visible = False
    charaLabel.changeChara()
    if charaLabel.currentDisplay == 0:
        dat = "CashAccount"
        UniAccountNameDict[dat].transactionIdList.append(UniData.data["self.currentId"])
        UniAccountNameDict[dat].save()
        UniData.add(
            Transaction(
                playerTest.netIcome,
                datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
                dat,
                "PAYDAY_INCOME",
            )
        )
    # print("checksPressed")


def checks_on_unpress():
    pass
    # print("checksReleased")


def batsu_on_press():
    charaLabel.CharaList[charaLabel.currentDisplay].visible = False
    # print("batsuPressed")


def batsu_on_unpress():
    charaLabel.CharaList[charaLabel.currentDisplay].visible = True
    # for ite in accountwindows:
    #     ite.set_visible(True)
    #     print(ite.account)
    # print(accountwindows)
    # print("batsuReleased")


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
        UniData.add(
            Transaction(
                amt, datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"), dat
            )
        )
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
check_pushbutton.set_handler("on_press", checks_on_press)
check_pushbutton.set_handler("on_release", checks_on_unpress)
batsu_pushbutton.set_handler("on_press", batsu_on_press)
batsu_pushbutton.set_handler("on_release", batsu_on_unpress)
window.push_handlers(pushbutton)
window.push_handlers(check_pushbutton)
window.push_handlers(batsu_pushbutton)

# sliddd=pyglet.gui.Slider(100,100,pressed_img,depressed_img,100,batch=batch)
# window.push_handlers(sliddd)
# window.push_handlers(datepushbutton)


def commmm(strr: str):
    print("commmmmm:" + strr)


def datecommmm(strr: str):
    print("datecomm:" + strr)


def accopen(strr: str):
    if strr in manifestJsonDict["Accounts"]:
        tmp = AccountTrueWindow(strr, resizable=True, width=600)
        # accountwindows.append(tmp)
        UniAccountNameDict[tmp.account.accountname] = tmp.account
        print(UniAccountNameDict)
    print(" accopen:" + strr)


def craccopen(strr: str):
    if strr in manifestJsonDict["Accounts"]:
        print("already exits just open")
    else:
        tmp = AccountTrueWindow(strr, resizable=True, width=600)
        accountwindows.append(tmp)
        UniAccountNameDict[tmp.account.accountname] = tmp.account
        print(UniAccountNameDict)
    print("craccopen:" + strr)


txen = pyglet.gui.TextEntry("amount", 0 + margin, 0 + margin, 100, batch=batch)
datetxen = pyglet.gui.TextEntry(
    "CertainAccount", 0 + margin, 20 + margin, 100, batch=batch
)
txen.set_handler("on_commit", commmm)
datetxen.set_handler("on_commit", datecommmm)
window.push_handlers(txen)
window.push_handlers(datetxen)
accountOpen = pyglet.gui.TextEntry(
    "openAccount", 0 + margin, 0 + margin + 50, 100, batch=batch
)
createAccountOpen = pyglet.gui.TextEntry(
    "CertainAccount", 0 + margin, 20 + margin + 50, 100, batch=batch
)
accountOpen.set_handler("on_commit", accopen)
createAccountOpen.set_handler("on_commit", craccopen)
window.push_handlers(accountOpen)
window.push_handlers(createAccountOpen)


fps_display = pyglet.window.FPSDisplay(window=window)

ddvx = 0
ddvy = 0
ddx = -50
ddy = -50


def bronian():
    global ddvx, ddvy, ddx, ddy
    ddvx += (np.random.uniform(0, 1) - 0.5) * 0.1
    ddvy += (np.random.uniform(0, 1) - 0.5) * 0.1
    ddx += ddvx
    ddy += ddvy
    if ddx > 0:
        # ddx = 1
        ddvx = -ddvx
    if ddy > 0:
        # ddy = 1
        ddvy = -ddvy
    if ddy < 0 - (backgroung_image.height - window.height):
        # ddy = 1
        ddvy = -ddvy
    if ddx < 0 - (backgroung_image.width - window.width):
        # ddx = 1
        ddvx = -ddvx


@window.event
def on_draw():
    window.clear()
    bronian()
    backgroung_image.blit(ddx, ddy)
    batch.draw()
    fps_display.draw()


@window.event
def on_close():
    pyglet.app.exit()


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


# tmpwin = AccountTrueWindow("NewAccount", resizable=True, width=600)
# UniAccountNameDict[tmpwin.account.accountname] = tmpwin.account
# print(UniAccountNameDict)
# caswin = AccountTrueWindow("CashAccount", resizable=True, width=600)
# UniAccountNameDict[caswin.account.accountname] = caswin.account
# print(UniAccountNameDict)
# pyglet.app.run()
# for accountName in manifestJsonDict["Accounts"]:
#     tmp = AccountTrueWindow(accountName, resizable=True, width=600)
#     UniAccountNameDict[tmp.account.accountname] = tmp.account
#     print(UniAccountNameDict)


# import time

# time.sleep(1)

# del accountwindows
pyglet.app.run(1 / 30.0)
