import pyglet
from pyglet.gl import GL_ONE_MINUS_SRC_ALPHA, GL_SRC_ALPHA
import entiti
import os

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
        self, tileSize: int = 256, name: str = "default_blobWindow", *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.tileSize = tileSize
        self.name: str = name
        self.anchor: pyglet.math.Vec3 = pyglet.math.Vec3(0, 0, 0)
        self.anchorVelocity: pyglet.math.Vec3 = pyglet.math.Vec3(0, 0, 0)
        self.set_icon(mainAssets.RSV_GRASS_YELLO_PIX)
        self.set_vsync(True)
        pyglet.clock.schedule_interval(
            self.update, 1 / 60
        )  # set the update function to be called 60times/second
        pyglet.gl.glClearColor(0.35, 0.4, 0.65, 0.5)  # set window clear color
        self.fpsDisplay: pyglet.window.FPSDisplay = pyglet.window.FPSDisplay(
            window=self,
            color=(0, 0, 0, 128),
        )  # set a fpsdisplay
        n = 2
        self.view = self.view.translate(
            (-self.width * (n - 1) / 2, -self.height * (n - 1) / 2, 0)
        )
        self.view = self.view.scale((n, n, 1))
        # self.view = self.view.translate((+self.width / 2, +self.height / 2, 0))
        self.blob: entiti.blob = entiti.blob(self.name, size=(20, 30))
        self.spriteDict: dict[str, pyglet.sprite.Sprite] = {}
        self.tilemapBatch: pyglet.graphics.Batch = pyglet.graphics.Batch()
        self.tileSize *= 1
        for k, v in self.blob.tileMap.items():
            pos: tuple[int, int] = k.split("_")[-1]
            self.spriteDict["sprite_" + pos] = pyglet.sprite.Sprite(
                img=getattr(mainAssets, v.tiletype), batch=self.tilemapBatch
            )
            self.spriteDict["sprite_" + pos].position = tuple(
                pyglet.math.Vec3(
                    v.position[0] * self.tileSize,
                    v.position[1] * self.tileSize,
                    v.position[2] * self.tileSize,
                )
                + self.anchor
            )

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
        self.fpsDisplay.draw()

    def on_key_press(self, symbol, modifiers):
        print(symbol, modifiers, pyglet.window.key.A)
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
            print("sldfj")
            self.anchorVelocity.y /= 2
            self.anchorVelocity.x /= 2
        print(self.anchorVelocity)
        return super().on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        print(symbol, modifiers, pyglet.window.key.A)
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
        print(self.anchorVelocity)


class droneRender(pyglet.sprite.Sprite):
    def __init__(self, window: blobWindow, img: pyglet.image.TextureRegion, **karg):
        self.window: blobWindow = window
        self.velocity = (0, 0, 0)
        super().__init__(img=img, batch=window.tilemapBatch, **karg)
        self.position = (
            self.window.width / 2,
            self.window.height / 2,
            1 * self.window.tileSize,
        )

    def update(self, dt: float):
        pass
