import pyglet
import numpy as np


class Transaction:
    def __init__(self, amount, date) -> None:
        self.amount = amount
        self.date = date

    def __str__(self) -> str:
        return f"<amount={self.amount},date={self.date}>"


class UniLedger:
    def __init__(self, filename: str) -> None:
        self.file = filename
        self.data = self.load()

    def save(self) -> None:
        np.save(self.file, self.data)

    def load(self) -> dict:
        try:
            dt = np.load(self.file, allow_pickle=True).item()
            dt["self.currentId"]
        except:
            dt = {}
            dt["self.currentId"] = 0
        return dt

    def add(self, amount: int, date: str) -> None:
        self.data[self.data["self.currentId"]] = Transaction(amount, date)
        self.data["self.currentId"] += 1
        self.save()

    def export_list(self):
        for k, v in self.data.items():
            print(k, v)


UniData = UniLedger("newUniLedger.npy")
# UniData.add(103, "2024-05-25")
UniData.export_list()

window = pyglet.window.Window(resizable=True)
batch = pyglet.graphics.Batch()
ball_image = pyglet.image.load("artAssets/but.png")
# ball = pyglet.sprite.Sprite(ball_image, x=50, y=50, batch=batch)

pressed_img = pyglet.resource.image("artAssets/greenPress.png")
depressed_img = pyglet.resource.image("artAssets/greenRelease.png")
pressed_img.height = 20
pressed_img.width = 20
depressed_img.height = 20
depressed_img.width = 20
print(pressed_img.height)
pushbutton = pyglet.gui.PushButton(
    x=350, y=0, pressed=pressed_img, depressed=depressed_img, batch=batch
)
# datepushbutton = pyglet.gui.PushButton(
#     x=350, y=20, pressed=pressed_img, depressed=depressed_img, batch=batch
# )


def my_on_press_handler():
    print(txen.value, type(txen.value))
    try:
        amt = int(txen.value)
        dat = datetxen.value
    except:
        print("null value")
        return
    # sdf=Transaction(amt)
    UniData.add(amt, dat)
    print("Button Pressed!")
    txen.value = "amount"
    datetxen.value = "date"
    UniData.export_list()


def my_on_release_handler():
    pass
    # print("Button Released...")


pushbutton.set_handler("on_press", my_on_press_handler)
pushbutton.set_handler("on_release", my_on_release_handler)
window.push_handlers(pushbutton)
# window.push_handlers(datepushbutton)


# label = pyglet.text.Label(
#     "Hello, world",
#     font_name="Times New Roman",
#     font_size=20,
#     x=0,
#     y=0,
#     color=(255, 255, 0, 255),
#     anchor_x="left",
#     anchor_y="bottom",
#     batch=batch,
# )


def commmm(strr: str):
    print("commmmmm:" + strr)


def datecommmm(strr: str):
    print("datecomm:" + strr)


txen = pyglet.gui.TextEntry("amount", 200, 0, 100, batch=batch)
datetxen = pyglet.gui.TextEntry("date", 200, 20, 100, batch=batch)
txen.set_handler("on_commit", commmm)
datetxen.set_handler("on_commit", datecommmm)
window.push_handlers(txen)
window.push_handlers(datetxen)


@window.event
def on_draw():
    window.clear()
    batch.draw()


pyglet.app.run()
