import pyglet
from pyglet.gl import GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA
import entiti
import sys
import os
import math

pyglet.image.Texture.default_mag_filter = pyglet.image.Texture.default_min_filter = (
    pyglet.gl.GL_NEAREST
)
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
if getattr(sys, "frozen", False):
    absPath = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    absPath = os.path.dirname(os.path.abspath(__file__))
print(absPath)
fileList = os.listdir(absPath)
print(fileList)
pyglet.resource.path = [f"{absPath}", ".", f"{os.path.dirname(__file__)}", *sys.path]
pyglet.resource.reindex()
print(pyglet.resource.path)


class assetsManager(entiti.entiti):
    def __init__(self, **karg) -> None:
        super().__init__(**karg)
        filenames: list[str] = os.listdir(self.folder)
        for itm in filenames:
            # print(itm.split(".")[0])
            setattr(
                self,
                itm.split(".")[0],
                pyglet.resource.image(self.folder + itm),
            )
        print("Assets load finished")


mainAssets = assetsManager(folder="artAssets/mainAssets/")


class blobWindow(pyglet.window.Window):
    def __init__(
        self,
        tileSize: int = 256,
        name: str = "default_blobWindow",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.n: float = 3  # the scaling factor default is 3.0
        self.tileSize: int = tileSize  # the sprite real pixel size
        self.name: str = name  # the blobs name
        self.blob: entiti.blob = entiti.blob(self.name, size=(20, 30))
        self.anchor: pyglet.math.Vec3 = pyglet.math.Vec3(0, 0, 0)
        self.tileMapSize: pyglet.math.Vec3 = pyglet.math.Vec3(
            self.blob.size[0] * self.tileSize, self.blob.size[1] * self.tileSize, 0
        )
        self.anchorVelocity: pyglet.math.Vec3 = pyglet.math.Vec3(0, 0, 0)
        self.set_icon(mainAssets.tile034)
        # self.set_vsync(True)
        pyglet.clock.schedule_interval(
            self.update, 1 / 60
        )  # set the update function to be called 60times/second
        pyglet.clock.schedule_interval(self.gameTimeUpdate, 1)
        pyglet.gl.glClearColor(0.35, 0.4, 0.65, 0.5)  # set window clear color
        # set the fpsDisplay at leftbottom corner
        self.fpsDisplay: pyglet.window.FPSDisplay = pyglet.window.FPSDisplay(
            window=self,
            color=(0, 0, 0, 128),
        )  # set a fpsdisplay
        # the main Dict for the tile sprite in this blob
        self.spriteDict: dict[str, pyglet.sprite.Sprite] = {}
        # bath rendering
        self.tilemapBatch: pyglet.graphics.Batch = pyglet.graphics.Batch()
        self.weidgeBatch: pyglet.graphics.Batch = pyglet.graphics.Batch()
        # the command bar at the left bottom corner
        self.commandBar: pyglet.gui.TextEntry = pyglet.gui.TextEntry(
            "", 0 + 5, 0 + 5, 200, batch=self.weidgeBatch
        )
        self.commandBar.set_handler("on_commit", self.commandBarOnCommit)
        self.push_handlers(self.commandBar)
        # set the righttop corner a clock display
        self.timeDisplay: pyglet.gui.TextEntry = pyglet.gui.TextEntry(
            f"tick:{self.blob.data['blobTime']}",
            self.width - 30 - 200,
            self.height - 50,
            200,
            batch=self.weidgeBatch,
        )
        # definate the tile size by the scaleing factor
        self.tileSize *= self.n
        # generate the actual sprite are rendering
        for k, v in self.blob.data["tileMap"].items():
            pos: str = k.split("_")[-1]
            self.spriteDict["loc_" + pos] = pyglet.sprite.Sprite(
                img=getattr(mainAssets, v.tiletype), batch=self.tilemapBatch
            )
            self.spriteDict["loc_" + pos].scale *= self.n
            self.spriteDict["loc_" + pos].initposition = tuple(
                pyglet.math.Vec3(
                    v.position[0] * self.tileSize,
                    v.position[1] * self.tileSize,
                    v.position[2] * self.tileSize,
                )
            )

    def commandBarOnCommit(self, cmd: str):
        print("comlskdfj", cmd)
        if cmd == "quit":
            self.dispatch_event("on_close")
        if cmd.startswith("goto_tyle"):  # for example goto_tyle_(2,3)
            lis = cmd.split("_")
            print(lis, lis[-1], [int(it) for it in lis[-1][1:-1].split(",")])
        if cmd.startswith("create_blob"):  # for example create_blob_newBlob
            name = cmd.split("_")[-1]
            newBlob = entiti.blob(name=name, size=(10, 20))
            print(name, newBlob)
        if cmd.startswith("goto_window"):  # for example goto_window_newBlob
            lis = cmd.split("_")
            print(lis, lis[-1])
            self.save()
            pyglet.clock.unschedule(self.update)
            pyglet.clock.unschedule(self.gameTimeUpdate)
            self.pldrone.movoto(lis[-1])
            self.close()
        if cmd.startswith("set_scale"):  # for example set_scale_4
            lis = cmd.split("_")
            print(lis, lis[-1])
            self.tileSize /= self.n
            self.tileSize *= float(lis[-1])
            self.selectDrone.scale /= self.n
            self.selectDrone.scale *= float(lis[-1])
            self.drone.scale /= self.n
            self.drone.scale *= float(lis[-1])
            for k, v in self.blob.data["tileMap"].items():
                pos: str = k.split("_")[-1]
                # self.spriteDict["loc_" + pos] = pyglet.sprite.Sprite(
                #     img=getattr(mainAssets, v.tiletype), batch=self.tilemapBatch
                # )
                self.spriteDict["loc_" + pos].scale /= self.n
                self.spriteDict["loc_" + pos].scale *= float(lis[-1])
                self.spriteDict["loc_" + pos].position = tuple(
                    pyglet.math.Vec3(
                        v.position[0] * self.tileSize,
                        v.position[1] * self.tileSize,
                        v.position[2],
                    )
                    + self.anchor
                )
            self.n = float(lis[-1])

        self.commandBar.value = ""

    def update(self, dt: float) -> None:
        self.timeDisplay.x = self.width - 30 - 200
        self.timeDisplay.y = self.height - 50
        self.anchor += self.anchorVelocity * dt
        for sprite in self.spriteDict.values():
            position: pyglet.math.Vec3 = pyglet.math.Vec3(*sprite.initposition)
            # print(position + (self.anchorVelocity * dt))
            sprite.position = tuple(position + (self.anchor))
        for k, v in self.blob.data["tileMap"].items():
            pos: str = k.split("_")[-1]
            if ("loc_" + pos) not in self.spriteDict:
                print("PRINT_notINdict")
                pyglet.gl.glDisable(pyglet.gl.GL_DEPTH_TEST)
                self.spriteDict["loc_" + pos] = pyglet.sprite.Sprite(
                    img=getattr(mainAssets, v.tiletype), batch=self.tilemapBatch
                )
                self.spriteDict["loc_" + pos].scale *= self.n
                self.spriteDict["loc_" + pos].initposition = tuple(
                    pyglet.math.Vec3(
                        v.position[0] * self.tileSize,
                        v.position[1] * self.tileSize,
                        v.position[2],
                    )
                )
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
                # v.changed = False

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
        # pyglet.gl.glEnable(pyglet.gl.GL_TEXTURE_2D)
        # pyglet.gl.glTexParameteri(
        #     pyglet.gl.GL_TEXTURE_2D,
        #     pyglet.gl.GL_TEXTURE_MAG_FILTER,
        #     pyglet.gl.GL_NEAREST,
        # )
        # pyglet.gl.glTexParameteri(
        #     pyglet.gl.GL_TEXTURE_2D,
        #     pyglet.gl.GL_TEXTURE_MIN_FILTER,
        #     pyglet.gl.GL_NEAREST,
        # )
        self.tilemapBatch.draw()
        pyglet.gl.glDisable(pyglet.gl.GL_DEPTH_TEST)
        self.weidgeBatch.draw()
        self.fpsDisplay.draw()

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
            # print("sldfj")
            self.anchorVelocity.y /= 2
            self.anchorVelocity.x /= 2
        # print(self.anchorVelocity)
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
        print(x, y, button, modifiers)
        selector: pyglet.sprite.Sprite = self.selectDrone
        if selector.visible:
            tup: tuple[int, int] = (
                math.floor((x - self.anchor.x) / self.tileSize),
                math.floor((y - self.anchor.y) / self.tileSize),
            )
            print(tup)
            if f"loc_({tup[0]},{tup[1]},{0})" in self.blob.data["tileMap"]:
                # print(self.blob.data["tileMap"][f"loc_({tup[0]},{tup[1]},{0})"])
                if button == 4:  # right clic
                    print("PRINT_onMOUSEpressRIGHTclick")
                    self.blob.data["tileMap"][
                        f"loc_({tup[0]},{tup[1]},{0})"
                    ].onRightClick()
                    # self.blob.data["tileMap"][
                    #     f"loc_({tup[0]},{tup[1]},{0})"
                    # ].tiletype = "tile012"
                    # self.blob.data["tileMap"][
                    #     f"loc_({tup[0]},{tup[1]},{0})"
                    # ].ident = "dirt"
                    # self.blob.data["tileMap"][f"loc_({tup[0]},{tup[1]},{0})"].age = 0
                if button == 1:
                    self.blob.data["tileMap"][
                        f"loc_({tup[0]},{tup[1]},{0})"
                    ].tiletype = "RSV_GRASS_GREEN_PIX"
                    self.blob.data["tileMap"][
                        f"loc_({tup[0]},{tup[1]},{0})"
                    ].ident = "salty"
                    self.blob.data["tileMap"][f"loc_({tup[0]},{tup[1]},{0})"].age = 0
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
        print(x, y, dx, dy, buttons, modifiers)
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
            print(tup)
            if f"loc_({tup[0]},{tup[1]},{0})" in self.blob.data["tileMap"]:
                # print(self.blob.data["tileMap"][f"loc_({tup[0]},{tup[1]},{0})"])
                if buttons == 4:
                    self.blob.data["tileMap"][
                        f"loc_({tup[0]},{tup[1]},{0})"
                    ].tiletype = "tile012"
                    self.blob.data["tileMap"][
                        f"loc_({tup[0]},{tup[1]},{0})"
                    ].ident = "dirt"
                    self.blob.data["tileMap"][f"loc_({tup[0]},{tup[1]},{0})"].age = 0
                if buttons == 1:
                    self.blob.data["tileMap"][
                        f"loc_({tup[0]},{tup[1]},{0})"
                    ].tiletype = "RSV_GRASS_GREEN_PIX"
                    self.blob.data["tileMap"][
                        f"loc_({tup[0]},{tup[1]},{0})"
                    ].ident = "salty"
                    self.blob.data["tileMap"][f"loc_({tup[0]},{tup[1]},{0})"].age = 0
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
        print("close")
        self.save()
        return super().on_close()

    def on_resize(self, width, height):
        return super().on_resize(width, height)


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
        self.scale *= self.window.n
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
