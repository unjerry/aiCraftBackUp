import pyglet
from pyglet.gl import GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA
import entiti
import sys
import os

pyglet.sprite.fragment_source = """#version 150 core
in vec4 vertex_colors;
in vec3 texture_coords;
out vec4 final_colors;

uniform sampler2D sprite_texture;

void main()
{
    final_colors = texture(sprite_texture, texture_coords.xy) * vertex_colors;
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

artAssetsFolder = "artAssets/"


class assetsManager(entiti.entiti):
    def __init__(self, **karg) -> None:
        super().__init__(**karg)
        filenames: list[str] = os.listdir(self.folder)
        for itm in filenames:
            print(itm.split(".")[0])
            setattr(
                self,
                itm.split(".")[0],
                pyglet.resource.image("artAssets/" + itm),
            )


mainAssets = assetsManager(folder=artAssetsFolder)


class blobWindow(pyglet.window.Window):
    def __init__(
        self,
        tileSize: int = 256,
        name: str = "default_blobWindow",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.tileSize = tileSize
        self.name: str = name
        self.blob: entiti.blob = entiti.blob(self.name, size=(20, 30))
        self.anchor: pyglet.math.Vec3 = pyglet.math.Vec3(0, 0, 0)
        self.tileMapSize: pyglet.math.Vec3 = pyglet.math.Vec3(
            self.blob.size[0] * self.tileSize, self.blob.size[1] * self.tileSize, 0
        )
        self.anchorVelocity: pyglet.math.Vec3 = pyglet.math.Vec3(0, 0, 0)
        self.set_icon(mainAssets.RSV_GRASS_YELLO_PIX)
        # self.set_vsync(True)
        pyglet.clock.schedule_interval(
            self.update, 1 / 60
        )  # set the update function to be called 60times/second
        pyglet.gl.glClearColor(0.35, 0.4, 0.65, 0.5)  # set window clear color
        self.fpsDisplay: pyglet.window.FPSDisplay = pyglet.window.FPSDisplay(
            window=self,
            color=(0, 0, 0, 128),
        )  # set a fpsdisplay
        n = 1
        self.view = self.view.translate(
            (-self.width * (n - 1) / 2, -self.height * (n - 1) / 2, 0)
        )
        self.view = self.view.scale((n, n, 1))
        # self.view = self.view.translate((+self.width / 2, +self.height / 2, 0))
        self.spriteDict: dict[str, pyglet.sprite.Sprite] = {}
        self.tilemapBatch: pyglet.graphics.Batch = pyglet.graphics.Batch()
        self.weidgeBatch: pyglet.graphics.Batch = pyglet.graphics.Batch()
        self.commandBar: pyglet.gui.TextEntry = pyglet.gui.TextEntry(
            "amount", 0 + 5, 0 + 5, 200, batch=self.weidgeBatch
        )
        self.commandBar.set_handler("on_commit", self.commandBarOnCommit)
        self.push_handlers(self.commandBar)
        self.tileSize *= 1
        for k, v in self.blob.tileMap.items():
            pos: str = k.split("_")[-1]
            self.spriteDict["sprite_" + pos] = pyglet.sprite.Sprite(
                img=getattr(mainAssets, v.tiletype), batch=self.tilemapBatch
            )
            self.spriteDict["sprite_" + pos].scale *= 2
            self.spriteDict["sprite_" + pos].position = tuple(
                pyglet.math.Vec3(
                    v.position[0] * self.tileSize,
                    v.position[1] * self.tileSize,
                    v.position[2] * self.tileSize,
                )
                + self.anchor
            )

    def commandBarOnCommit(self, cmd: str):
        print("comlskdfj", cmd)
        if cmd == "quit":
            self.dispatch_event("on_close")
        if cmd.startswith("goto_tyle"):
            lis = cmd.split("_")
            print(lis, lis[-1], [int(it) for it in lis[-1][1:-1].split(",")])
        if cmd.startswith("create_blob"):
            name = cmd.split("_")[-1]
            newBlob = entiti.blob(name=name, size=(10, 20))
            print(name, newBlob)
        if cmd.startswith("goto_window"):
            lis = cmd.split("_")
            print(lis, lis[-1])
            firstBlob = blobWindow(tileSize=self.tileSize, name=lis[-1], caption="sdf")
            self.drone.window = firstBlob
            self.drone.batch = firstBlob.tilemapBatch
            firstBlob.drone = self.drone
            # self.blob.save()
            self.close()

        self.commandBar.value = ""

    def update(self, dt: float) -> None:
        self.anchor += self.anchorVelocity * dt
        for sprite in self.spriteDict.values():
            position: pyglet.math.Vec3 = pyglet.math.Vec3(*sprite.position)
            # print(position + (self.anchorVelocity * dt))
            sprite.position = tuple(position + (self.anchorVelocity * dt))

    def on_draw(self) -> None:
        self.clear()
        pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)
        # pyglet.gl.glEnable(pyglet.gl.GL_TEXTURE_2D)
        pyglet.gl.glTexParameteri(
            pyglet.gl.GL_TEXTURE_2D,
            pyglet.gl.GL_TEXTURE_MAG_FILTER,
            pyglet.gl.GL_NEAREST,
        )
        pyglet.gl.glTexParameteri(
            pyglet.gl.GL_TEXTURE_2D,
            pyglet.gl.GL_TEXTURE_MIN_FILTER,
            pyglet.gl.GL_NEAREST,
        )
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
                int((x - self.anchor.x) / self.tileSize),
                int((y - self.anchor.y) / self.tileSize),
            )
            print(tup)
            if f"loc_({tup[0]},{tup[1]})" in self.blob.tileMap:
                print(self.blob.tileMap[f"loc_({tup[0]},{tup[1]})"])
                if button == 4:
                    self.blob.tileMap[f"loc_({tup[0]},{tup[1]})"].tiletype = (
                        "RSV_GRASS_YELLO_PIX"
                    )
                if button == 1:
                    self.blob.tileMap[f"loc_({tup[0]},{tup[1]})"].tiletype = (
                        "RSV_GRASS_GREEN_PIX"
                    )
                self.spriteDict[f"sprite_({tup[0]},{tup[1]})"].image = getattr(
                    mainAssets, self.blob.tileMap[f"loc_({tup[0]},{tup[1]})"].tiletype
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
        #     int((x - self.anchor.x) / self.tileSize),
        #     int((y - self.anchor.y) / self.tileSize),
        #     int((self.drone.x - self.anchor.x) / self.tileSize),
        #     int((self.drone.y - self.anchor.y) / self.tileSize),
        # )
        drone: pyglet.sprite.Sprite = self.selectDrone
        self.selectDrone.x = (
            int((x - self.anchor.x) / self.tileSize) * self.tileSize
        ) + self.anchor.x
        self.selectDrone.y = (
            int((y - self.anchor.y) / self.tileSize) * self.tileSize
        ) + self.anchor.y
        if (
            abs(
                int((x - self.anchor.x) / self.tileSize)
                - (int((self.drone.x - self.anchor.x) / self.tileSize) + 0.5)
            )
            > 1.5
        ) or (
            abs(
                int((y - self.anchor.y) / self.tileSize)
                - (int((self.drone.y - self.anchor.y) / self.tileSize) + 0.5)
            )
            > 1.5
        ):
            drone.visible = False
        else:
            drone.visible = True
        return

    def on_close(self):
        self.blob.save()
        return super().on_close()


class droneRender(pyglet.sprite.Sprite):
    def __init__(self, window: blobWindow, img: pyglet.image.TextureRegion, **karg):
        self.window: blobWindow = window
        self.velocity = (0, 0, 0)
        super().__init__(img=img, batch=window.tilemapBatch, **karg)
        self.position = (
            self.window.width / 2,
            self.window.height / 2,
            1,
        )
        # self.window.drone = self
        self.scale *= 2

    def update(self, dt: float):
        pass
