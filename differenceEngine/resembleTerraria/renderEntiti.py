import pyglet
import entiti
import os


class assetsManager(entiti.entiti):
    def __init__(self, name: str, **karg) -> None:
        super().__init__(name, **karg)
        pyglet.image.Texture.default_mag_filter = (
            pyglet.image.Texture.default_min_filter
        ) = pyglet.gl.GL_NEAREST
        filenames: list[str] = os.listdir(self.folder)
        for itm in filenames:
            if itm.split(".")[-1] == "png":
                setattr(
                    self,
                    itm,
                    pyglet.resource.image(self.folder + itm),
                )
            if itm.split(".")[-1] == "gif":
                setattr(
                    self,
                    itm,
                    pyglet.resource.animation(self.folder + itm),
                )
        print("Assets load finished")


class blob(entiti.entiti):
    def __init__(self, name: str, **karg) -> None:
        super().__init__(name, **karg)
        self.mainGrid = entiti.tyleMap(f"mainGrid_of_{self.name}")
        self.mainAssets = assetsManager(
            f"mainAssets_of_{self.name}", folder="artAssets/mainAssets/"
        )


class blobWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_vsync(False)  # close verticle sync
        self.baseBatch = pyglet.graphics.Batch()
        self.flotBatch = pyglet.graphics.Batch()
        self.sprites = {}
        self.fpsDisplay: pyglet.window.FPSDisplay = pyglet.window.FPSDisplay(
            window=self,
            color=(255, 255, 255, 255),
        )

    def on_draw(self):
        pyglet.gl.glClearColor(0.35, 0.4, 0.65, 0.5)
        self.clear()
        self.baseBatch.draw()
        self.flotBatch.draw()
        self.fpsDisplay.draw()
