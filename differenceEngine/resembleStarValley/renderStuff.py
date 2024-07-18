import pyglet
from pyglet.gl import GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA
import pyglet.graphics
import entiti
import sys
import os
import math

# set the pixel style art
pyglet.image.Texture.default_mag_filter = pyglet.image.Texture.default_min_filter = (
    pyglet.gl.GL_NEAREST
)
# use the transparent shader
pyglet.sprite.fragment_source = """#version 150 core
in vec4 vertex_colors;
in vec3 texture_coords;
out vec4 final_colors;

uniform sampler2D loc_texture;

void main()
{
    final_colors = texture(loc_texture, texture_coords.xy) * vertex_colors;
    if (final_colors.a < 0.01) discard;
} """
# the pyinstaller freeze the relative path
if getattr(sys, "frozen", False):
    absPath = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    absPath = os.path.dirname(os.path.abspath(__file__))
print("PRINT_absPath", absPath)
fileList = os.listdir(absPath)
print("PRINT_fileList", fileList)
pyglet.resource.path = [f"{absPath}", ".", f"{os.path.dirname(__file__)}", *sys.path]
pyglet.resource.reindex()
print("PRINT_pyglet.resource.path", pyglet.resource.path)


# the unified assets
class assetsManager(entiti.entiti):
    def __init__(self, **karg) -> None:
        super().__init__(**karg)
        filenames: list[str] = os.listdir(self.folder)
        for itm in filenames:
            setattr(
                self,
                itm.split(".")[0],
                pyglet.resource.image(self.folder + itm),
            )
            if getattr(self, itm.split(".")[0]).width == 3 * 16:
                img = getattr(self, itm.split(".")[0])
                img.anchor_x = 16
        print("Assets load finished")


mainAssets = assetsManager(folder="artAssets/mainAssets/")


class ytemListBatch(pyglet.graphics.Batch):
    def __init__(self, drone: entiti.dron, scale: float):
        super().__init__()
        self.drone: entiti.dron = drone
        self.spriteDict: dict[str, pyglet.sprite.Sprite] = {}
        self.labelDict: dict[str, pyglet.sprite.Sprite] = {}
        self.scaleF: float = scale
        print("PRINT_ytembatch", drone.data["itemDict"])
        self.selector: pyglet.sprite.Sprite = pyglet.sprite.Sprite(
            mainAssets.tile011,
            210 + self.drone.data["itemSelected"] * 16 * self.scaleF,
            0,
            11,
            batch=self,
        )
        self.selector.scale *= self.scaleF
        for k, item in drone.data["itemDict"].items():
            k: int
            item: entiti.ytem
            # print("PRINT_item", item)
            self.spriteDict[k] = pyglet.sprite.Sprite(
                getattr(mainAssets, item.ident),
                210 + k * self.scaleF * 16,
                0,
                11,
                batch=self,
            )
            self.spriteDict[k].scale *= self.scaleF
            self.labelDict[k] = pyglet.text.Label(
                f"{item.num}",
                font_name="courier new",
                font_size=13,
                x=240 + k * self.scaleF * 16,
                y=10,
                z=12,
                anchor_x="center",
                anchor_y="center",
                batch=self,
            )

    def update(self):
        self.selector.x = 210 + self.drone.data["itemSelected"] * 16 * self.scaleF
        if self.drone.itemChanged:
            for k, item in self.drone.data["itemDict"].items():
                k: int
                item: entiti.ytem
                # print("PRINT_item", item)
                if item.num == 0:
                    self.spriteDict.pop(k)
                    self.labelDict.pop(k)
                    self.drone.data["itemDict"].pop(k)
                    break
                self.spriteDict[k] = pyglet.sprite.Sprite(
                    getattr(mainAssets, item.ident),
                    210 + k * self.scaleF * 16,
                    0,
                    11,
                    batch=self,
                )
                self.spriteDict[k].scale *= self.scaleF
                self.labelDict[k] = pyglet.text.Label(
                    f"{item.num}",
                    font_name="courier new",
                    font_size=13,
                    x=240 + k * self.scaleF * 16,
                    y=10,
                    z=12,
                    anchor_x="center",
                    anchor_y="center",
                    batch=self,
                )
            self.drone.itemChanged = False


# the main window object
class blobWindow(pyglet.window.Window):
    def __init__(
        self,
        tileSize: int,
        name: str,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.pldrone: PlayerDroneRender
        self.selectDrone: droneRender
        self.drone: droneRender
        self.YtemBatch: ytemListBatch
        # the scaling factor default is 3.0 [HYPERPARAMETER]
        self.scaleFactor: float = 3
        self.tileSize: int = tileSize  # the sprite real pixel size
        self.name: str = name  # the blobs name
        self.blob: entiti.blob = entiti.blob(self.name)
        self.anchor: pyglet.math.Vec3 = pyglet.math.Vec3(0, 0, 0)
        # self.tileMapSize: pyglet.math.Vec3 = pyglet.math.Vec3(
        #     self.blob.size[0] * self.tileSize, self.blob.size[1] * self.tileSize, 0
        # )
        self.anchorVelocity: pyglet.math.Vec3 = pyglet.math.Vec3(0, 0, 0)
        self.set_icon(mainAssets.tile034)  # set the icon
        self.set_vsync(False)  # close verticle sync
        # set the update function to be called 60 times/second
        pyglet.clock.schedule_interval(self.update, 1 / 60)
        # set the gameTimeUpdate function to be called 1 times/second
        pyglet.clock.schedule_interval(self.gameTimeUpdate, 1)
        pyglet.gl.glClearColor(0.35, 0.4, 0.65, 0.5)  # set window clear color
        # set the fpsDisplay at leftbottom corner
        self.fpsDisplay: pyglet.window.FPSDisplay = pyglet.window.FPSDisplay(
            window=self,
            color=(0, 0, 0, 128),
        )
        # the main Dict for the tile sprite in this blob
        self.spriteDict: dict[str, pyglet.sprite.Sprite] = {}
        # bath rendering
        self.tilemapBatch: pyglet.graphics.Batch = pyglet.graphics.Batch()
        self.weidgeBatch: pyglet.graphics.Batch = pyglet.graphics.Batch()
        self.treeBatch: pyglet.graphics.Batch = pyglet.graphics.Batch()
        # the command bar at the left bottom corner
        self.commandBar: pyglet.gui.TextEntry = pyglet.gui.TextEntry(
            "", 0 + 5, 0 + 5, 200, batch=self.weidgeBatch
        )
        self.commandBar.set_handler("on_commit", self.commandBarOnCommit)
        self.push_handlers(self.commandBar)
        # set the right top corner a clock display
        self.timeDisplay: pyglet.gui.TextEntry = pyglet.gui.TextEntry(
            f"tick:{self.blob.data['blobTime']}",
            self.width - 30 - 200,
            self.height - 50,
            200,
            batch=self.weidgeBatch,
        )
        # definate the tile size by the scaleing factor
        self.tileSize *= self.scaleFactor
        # generate the actual sprite are rendering
        # the sprite pixel size shoud be same as the original tileSize
        for k, v in self.blob.data["tileMap"].items():
            v: entiti.tyle
            k: str
            pos: str = k.split("_")[-1]
            # print("PRINT_pos_init", pos)
            if v.ident == "tree":
                self.add_sprite(v, pos, self.treeBatch)
                continue
            self.add_sprite(v, pos, self.tilemapBatch)

    # the command Bar
    def commandBarOnCommit(self, cmd: str):
        print("The coammand you enter is:", cmd)
        if cmd == "quit":
            self.dispatch_event("on_close")
        if cmd.startswith("goto_tyle"):  # for example goto_tyle_(2,3)
            lis = cmd.split("_")
            print(lis, lis[-1], [int(it) for it in lis[-1][1:-1].split(",")])
        if cmd.startswith("create_blob"):  # for example create_blob_newBlob
            name = cmd.split("_")[-1]
            newBlob = entiti.blob(name=name, size=(10, 20))
            print("PRINT_create_newBlob", name, newBlob)
        if cmd.startswith("goto_window"):  # for example goto_window_newBlob
            lis = cmd.split("_")
            print("PRINT_goto_window", lis, lis[-1])
            self.save()
            pyglet.clock.unschedule(self.update)
            pyglet.clock.unschedule(self.gameTimeUpdate)
            self.pldrone.movoto(lis[-1])
            self.close()
        if cmd.startswith("set_scale"):  # for example set_scale_4
            lis = cmd.split("_")
            print("PRINT_set_scale", lis, lis[-1])
            self.tileSize /= self.scaleFactor
            self.tileSize *= float(lis[-1])
            self.selectDrone.scale /= self.scaleFactor
            self.selectDrone.scale *= float(lis[-1])
            self.drone.scale /= self.scaleFactor
            self.drone.scale *= float(lis[-1])
            for k, v in self.blob.data["tileMap"].items():
                k: str
                v: entiti.tyle
                pos: str = k.split("_")[-1]
                # print("PRINT_pos_command", pos)
                self.spriteDict["loc_" + pos].scale /= self.scaleFactor
                self.spriteDict["loc_" + pos].scale *= float(lis[-1])
                self.spriteDict["loc_" + pos].initposition = tuple(
                    pyglet.math.Vec3(
                        v.position[0] * self.tileSize,
                        v.position[1] * self.tileSize,
                        v.position[2],
                    )
                )
            self.scaleFactor = float(lis[-1])
        if cmd.startswith("give_ytem"):  # give_ytem_seed_5
            if len(cmd.split("_")[-2]) == 4:
                name = cmd.split("_")[-2]
                num = int(cmd.split("_")[-1])
                self.pldrone.drone.giveYtem(name, num)
        self.commandBar.value = ""  # clear the bar after enter

    def add_sprite(self, v: entiti.tyle, pos: str, bat: pyglet.graphics.Batch):
        self.spriteDict["loc_" + pos] = pyglet.sprite.Sprite(
            img=getattr(mainAssets, v.tiletype),
            batch=bat,
            group=pyglet.graphics.Group(-v.position[1]),
        )
        self.spriteDict["loc_" + pos].scale *= self.scaleFactor
        self.spriteDict["loc_" + pos].initposition = tuple(
            pyglet.math.Vec3(
                v.position[0] * self.tileSize,
                v.position[1] * self.tileSize,
                v.position[2],
            )
        )
        if v.ident == "tree":
            self.spriteDict["loc_" + pos].initposition = tuple(
                pyglet.math.Vec3(
                    (v.position[0]) * self.tileSize,
                    (v.position[1]) * self.tileSize,
                    v.position[2],
                )
            )

    # main update loop
    def update(self, dt: float) -> None:
        self.YtemBatch.update()
        self.timeDisplay.x = self.width - 30 - 200
        self.timeDisplay.y = self.height - 50
        self.anchor += self.anchorVelocity * dt
        # render sprite at the right position
        for sprite in self.spriteDict.values():
            position: pyglet.math.Vec3 = pyglet.math.Vec3(*sprite.initposition)
            sprite.position = tuple(position + (self.anchor))
        for k, v in self.spriteDict.items():
            k: str
            v: pyglet.sprite.Sprite
            if k not in self.blob.data["tileMap"]:
                self.spriteDict.pop(k)
                break
        for k, v in self.blob.data["tileMap"].items():
            v: entiti.tyle
            pos: str = k.split("_")[-1]
            if ("loc_" + pos) not in self.spriteDict:
                print("PRINT_notINdict")
                self.add_sprite(v, pos, self.tilemapBatch)
            if v.changed:
                self.spriteDict["loc_" + pos].image = getattr(
                    mainAssets,
                    v.tiletype,
                )
                self.spriteDict["loc_" + pos].position = tuple(
                    pyglet.math.Vec3(
                        v.position[0] * self.tileSize,
                        v.position[1] * self.tileSize,
                        v.position[2],
                    )
                    + self.anchor
                )
                v.changed = False

    def gameTimeUpdate(self, dt: float) -> None:
        self.pldrone.drone.data["perspectiveCumulateTime"] += 1
        self.blob.sync(self.pldrone.drone.data["perspectiveCumulateTime"])
        self.timeDisplay.value = f"tick:{self.blob.data['blobTime']}"
        print(
            "PRINT_sampling",
            self.blob.data["blobTime"],
            self.blob.data["tileMap"][f"loc_({0},{0},{0})"].ident,
            (f"loc_({0},{0},{1})" in self.blob.data["tileMap"]),
            self.blob.data["tileMap"][f"loc_({0},{0},{0})"].tiletype,
            self.blob.data["tileMap"][f"loc_({0},{0},{0})"].age,
            self.pldrone.drone.data["perspectiveCumulateTime"],
        )
        if f"loc_({0},{0},{1})" in self.blob.data["tileMap"]:
            print(self.blob.data["tileMap"][f"loc_({0},{0},{1})"].tiletype)
            print(self.blob.data["tileMap"][f"loc_({0},{0},{1})"].age)
            print(self.blob.data["tileMap"][f"loc_({0},{0},{1})"].ident)

    def on_draw(self) -> None:
        self.clear()
        pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)
        self.tilemapBatch.draw()
        pyglet.gl.glDisable(pyglet.gl.GL_DEPTH_TEST)
        self.treeBatch.draw()
        self.YtemBatch.draw()
        self.weidgeBatch.draw()
        self.fpsDisplay.draw()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # print("PRINT_onMouse_scroll", x, y, scroll_x, scroll_y)
        self.pldrone.drone.data["itemSelected"] -= int(scroll_y)
        if self.pldrone.drone.data["itemSelected"] < 0:
            self.pldrone.drone.data["itemSelected"] = 0

    def on_key_press(self, symbol, modifiers):
        # print(symbol, modifiers, pyglet.window.key.A)
        if symbol == pyglet.window.key.A:
            self.anchorVelocity.x += 4 * self.tileSize
        if symbol == pyglet.window.key.D:
            self.anchorVelocity.x += -4 * self.tileSize
        if symbol == pyglet.window.key.S:
            self.anchorVelocity.y += 4 * self.tileSize
        if symbol == pyglet.window.key.W:
            self.anchorVelocity.y += -4 * self.tileSize
        if (
            symbol == pyglet.window.key.LSHIFT
            or symbol == pyglet.window.key.RSHIFT
            or symbol == pyglet.window.key.SPACE
        ):
            self.anchorVelocity.y /= 2
            self.anchorVelocity.x /= 2
        return super().on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        # print(symbol, modifiers, pyglet.window.key.A)
        if symbol == pyglet.window.key.A:
            self.anchorVelocity.x = 0
        if symbol == pyglet.window.key.D:
            self.anchorVelocity.x = 0
        if symbol == pyglet.window.key.S:
            self.anchorVelocity.y = 0
        if symbol == pyglet.window.key.W:
            self.anchorVelocity.y = 0
        if (
            symbol == pyglet.window.key.LSHIFT
            or symbol == pyglet.window.key.RSHIFT
            or symbol == pyglet.window.key.SPACE
        ):
            self.anchorVelocity.y *= 2
            self.anchorVelocity.x *= 2
        # print(self.anchorVelocity)

    def on_mouse_press(self, x, y, button, modifiers):
        # print(x, y, button, modifiers)
        selector: pyglet.sprite.Sprite = self.selectDrone
        if selector.visible:
            tup: tuple[int, int] = (
                math.floor((x - self.anchor.x) / self.tileSize),
                math.floor((y - self.anchor.y) / self.tileSize),
            )
            if f"loc_({tup[0]},{tup[1]},{0})" in self.blob.data["tileMap"]:
                # print(self.blob.data["tileMap"][f"loc_({tup[0]},{tup[1]},{0})"])
                if button == 4:  # right clic
                    print("PRINT_onMOUSEpressRIGHTclick")
                    self.pldrone.drone.onRightClick(
                        self.blob.data["tileMap"][f"loc_({tup[0]},{tup[1]},{0})"]
                    )
                    self.blob.data["tileMap"][
                        f"loc_({tup[0]},{tup[1]},{0})"
                    ].onRightClick(self.pldrone.drone)
                    # self.blob.data["tileMap"][
                    #     f"loc_({tup[0]},{tup[1]},{0})"
                    # ].tiletype = "tile012"
                    # self.blob.data["tileMap"][
                    #     f"loc_({tup[0]},{tup[1]},{0})"
                    # ].ident = "dirt"
                    # self.blob.data["tileMap"][f"loc_({tup[0]},{tup[1]},{0})"].age = 0
                if button == 1:
                    pass
                    # self.blob.data["tileMap"][
                    #     f"loc_({tup[0]},{tup[1]},{0})"
                    # ].tiletype = "RSV_GRASS_GREEN_PIX"
                    # self.blob.data["tileMap"][
                    #     f"loc_({tup[0]},{tup[1]},{0})"
                    # ].ident = "salty"
                    # self.blob.data["tileMap"][f"loc_({tup[0]},{tup[1]},{0})"].age = 0
                self.spriteDict[f"loc_({tup[0]},{tup[1]},{0})"].image = getattr(
                    mainAssets,
                    self.blob.data["tileMap"][f"loc_({tup[0]},{tup[1]},{0})"].tiletype,
                )
            else:
                print("out of this blobs boundary")
        return

    def on_mouse_motion(self, x, y, dx, dy):
        # print(
        #     x - self.anchor.x,
        #     y - self.anchor.y,
        #     dx,
        #     dy,
        #     math.floor((x - self.anchor.x) / self.tileSize),
        #     math.floor((y - self.anchor.y) / self.tileSize),
        #     math.floor((self.drone.x - self.anchor.x) / self.tileSize),
        #     math.floor((self.drone.y - self.anchor.y) / self.tileSize),
        # )
        drone: pyglet.sprite.Sprite = self.selectDrone
        self.selectDrone.x = (
            math.floor((x - self.anchor.x) / self.tileSize) * self.tileSize
        ) + self.anchor.x
        self.selectDrone.y = (
            math.floor((y - self.anchor.y) / self.tileSize) * self.tileSize
        ) + self.anchor.y
        if (
            abs(
                math.floor((x - self.anchor.x) / self.tileSize)
                - (math.floor((self.drone.x - self.anchor.x) / self.tileSize) + 0.5)
            )
            > 1.5
        ) or (
            abs(
                math.floor((y - self.anchor.y) / self.tileSize)
                - (math.floor((self.drone.y - self.anchor.y) / self.tileSize) + 0.5)
            )
            > 1.5
        ):
            drone.visible = False
        else:
            drone.visible = True
        return

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # print(x, y, dx, dy, buttons, modifiers)
        drone: pyglet.sprite.Sprite = self.selectDrone
        self.selectDrone.x = (
            math.floor((x - self.anchor.x) / self.tileSize) * self.tileSize
        ) + self.anchor.x
        self.selectDrone.y = (
            math.floor((y - self.anchor.y) / self.tileSize) * self.tileSize
        ) + self.anchor.y
        if (
            abs(
                math.floor((x - self.anchor.x) / self.tileSize)
                - (math.floor((self.drone.x - self.anchor.x) / self.tileSize) + 0.5)
            )
            > 1.5
        ) or (
            abs(
                math.floor((y - self.anchor.y) / self.tileSize)
                - (math.floor((self.drone.y - self.anchor.y) / self.tileSize) + 0.5)
            )
            > 1.5
        ):
            drone.visible = False
        else:
            drone.visible = True
        selector: pyglet.sprite.Sprite = self.selectDrone
        if selector.visible:
            tup: tuple[int, int] = (
                math.floor((x - self.anchor.x) / self.tileSize),
                math.floor((y - self.anchor.y) / self.tileSize),
            )
            if f"loc_({tup[0]},{tup[1]},{0})" in self.blob.data["tileMap"]:
                # print(self.blob.data["tileMap"][f"loc_({tup[0]},{tup[1]},{0})"])
                if buttons == 4:
                    print("PRINT_onMOUSEpressRIGHTclick")
                    self.pldrone.drone.onRightDrag(
                        self.blob.data["tileMap"][f"loc_({tup[0]},{tup[1]},{0})"]
                    )
                    self.blob.data["tileMap"][
                        f"loc_({tup[0]},{tup[1]},{0})"
                    ].onRightDrag(self.pldrone.drone)
                if buttons == 1:
                    pass
                    # self.blob.data["tileMap"][
                    #     f"loc_({tup[0]},{tup[1]},{0})"
                    # ].tiletype = "RSV_GRASS_GREEN_PIX"
                    # self.blob.data["tileMap"][
                    #     f"loc_({tup[0]},{tup[1]},{0})"
                    # ].ident = "salty"
                    # self.blob.data["tileMap"][f"loc_({tup[0]},{tup[1]},{0})"].age = 0
                self.spriteDict[f"loc_({tup[0]},{tup[1]},{0})"].image = getattr(
                    mainAssets,
                    self.blob.data["tileMap"][f"loc_({tup[0]},{tup[1]},{0})"].tiletype,
                )
            else:
                print("out of this blobs boundary")
        return

    def save(self) -> None:
        self.blob.save()
        print(self.pldrone.drone.data["position"])
        self.pldrone.drone.data["position"] = tuple(self.anchor)
        print(self.pldrone.drone.data["position"])
        self.pldrone.drone.save()

    def on_close(self):
        print("PRINT_blobWindow_on_close")
        self.save()
        return super().on_close()

    def on_resize(self, width, height):
        super().on_resize(width, height)


class droneRender(pyglet.sprite.Sprite):
    def __init__(
        self,
        window,
        img: pyglet.image.TextureRegion,
        name: str = "defaultPlayerDroneName",
        **karg,
    ):
        self.window: blobWindow = window
        self.name: str = name
        super().__init__(img=img, batch=self.window.tilemapBatch, **karg)
        self.position = (
            self.window.width / 2,
            self.window.height / 2,
            1,
        )
        self.scale *= self.window.scaleFactor
        # print(self.window.anchor, self.drone.position)

    # def setWindow(self, window: blobWindow):
    #     self.window = window


class PlayerDroneRender(entiti.entiti):
    def __init__(self, name, **karg) -> None:
        super().__init__(**karg)
        self.name = name
        self.drone: entiti.dron = entiti.dron(name=self.name)
        self.firstBlob = blobWindow(
            width=1000,
            height=600,
            tileSize=16,
            name=self.drone.data["worldBlobName"],
            caption=self.drone.data["worldBlobName"],
            resizable=True,
        )
        self.drone.giveYtem("seed")
        self.drone.giveYtem("dirt")
        self.drone.giveYtem("fastFruit")
        self.firstList: ytemListBatch = ytemListBatch(
            self.drone, self.firstBlob.scaleFactor
        )

        self.firstBlob.YtemBatch = self.firstList
        self.firstBlob.blob.sync(self.drone.data["perspectiveCumulateTime"])
        # renderStuff
        self.mainPlayerDrone = droneRender(
            window=self.firstBlob,
            img=mainAssets.RSV_FOUR_COLOR_DRONE_SQUARE_PIX,
            name="mainPlayerDrone",
        )
        self.mainPlayerDrone.z = 3
        self.mainSelectDrone = droneRender(
            window=self.firstBlob, img=mainAssets.tile011, name="mainSelectDrone"
        )
        self.mainSelectDrone.z = 2
        self.firstBlob.anchor = pyglet.math.Vec3(*self.drone.data["position"])
        self.firstBlob.pldrone = self
        self.firstBlob.drone = self.mainPlayerDrone
        self.firstBlob.selectDrone = self.mainSelectDrone

    def movoto(self, window):
        self.drone.data["worldBlobName"] = window
        self.firstBlob = blobWindow(
            width=1000,
            height=600,
            tileSize=16,
            name=window,
            caption=window,
            resizable=True,
        )
        self.firstList: ytemListBatch = ytemListBatch(
            self.drone, self.firstBlob.scaleFactor
        )

        self.firstBlob.YtemBatch = self.firstList
        self.firstBlob.blob.sync(self.drone.data["perspectiveCumulateTime"])
        # renderStuff
        self.mainPlayerDrone.batch = self.firstBlob.tilemapBatch
        self.mainSelectDrone.batch = self.firstBlob.tilemapBatch
        # the new world anchor
        # self.firstBlob.anchor = pyglet.math.Vec3(
        #     *self.drone.data["position"]
        # )
        self.firstBlob.pldrone = self
        self.firstBlob.drone = self.mainPlayerDrone
        self.firstBlob.selectDrone = self.mainSelectDrone
