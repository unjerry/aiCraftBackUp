import pyglet
import numpy as np

# import os
pyglet.sprite.fragment_source = """#version 150 core
in vec4 vertex_colors;
in vec3 texture_coords;
out vec4 final_colors;

uniform sampler2D sprite_texture;

void main()
{
    final_colors = texture(sprite_texture, texture_coords.xy) * vertex_colors;
    if (final_colors.a < 1.0) discard;
} """


class TileMap:
    def __init__(self, batch, window) -> None:
        self.batch: pyglet.graphics.Batch = batch
        self.window: pyglet.window.Window = window


class MenuWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.matHexCoord: pyglet.math.Mat3 = pyglet.math.Mat3(
            [
                1.01,
                0,
                0.0,
                1 / 2,
                np.sqrt(3.0) / 2 * 0.9,
                -0.0001,
                0.0,
                1 * 0.4,
                1.0,
            ]
        )
        self.mat: pyglet.math.Mat3 = pyglet.math.Mat3(
            [
                1.01,
                0,
                0.0,
                1 / 2,
                np.sqrt(3.0) / 2 * 0.9,
                0.0,
                0.0,
                1 * 0.4,
                1.0,
            ]
        )
        inv = np.linalg.inv(np.array(tuple(self.mat)).reshape(3, 3).T)
        print(inv)
        print(inv.T.flatten().tolist())
        self.matInverse: pyglet.math.Mat3 = pyglet.math.Mat3(inv.T.flatten().tolist())
        print(self.matInverse @ self.mat)
        self.batch: pyglet.graphics.Batch = pyglet.graphics.Batch()
        self.fpsDisplay: pyglet.window.FPSDisplay = pyglet.window.FPSDisplay(
            window=self,
            color=(0, 0, 0, 128),
        )
        self.anchor: pyglet.math.Vec3 = pyglet.math.Vec3(50, 50, 0)
        self.anchorVelocity: pyglet.math.Vec3 = pyglet.math.Vec3(0, 0, 0)
        # absolutePath=os.path.dirname(os.path.abspath(__file__))
        # pyglet.resource.path=[absolutePath]
        # print(absolutePath,pyglet.resource.path)
        pyglet.clock.schedule_interval(self.update, 1 / 60)
        pyglet.gl.glClearColor(0.35, 0.4, 0.65, 0.5)
        pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)
        self.image: pyglet.image.TextureRegion = pyglet.resource.image(
            "rawRsc/hexagonTiles/Tiles/tileSnow.png",
        )
        self.playerImage: pyglet.image.TextureRegion = pyglet.resource.image(
            "rawRsc/hexagonTiles/Tiles/alienGreen.png",
        )
        self.image_tile: pyglet.image.TextureRegion = pyglet.resource.image(
            "rawRsc/hexagonTiles/Tiles/tileSnow_tile.png"
        )
        self.image.anchor_x = self.image.width / 2
        self.image.anchor_y = self.image.height / 2
        self.playerImage.anchor_x = self.playerImage.width / 2
        self.playerImage.anchor_y = self.playerImage.height / 2
        self.image_tile.anchor_x = self.image_tile.width / 2
        self.image_tile.anchor_y = self.image_tile.height / 2

        def onclick():
            print("sdf")

        self.sprites: dict[str, pyglet.sprite.Sprite] = {}
        for i in range(5):
            for j in range(3):
                for k in range(1):
                    self.sprites[f"{i},{j},{k}"] = pyglet.sprite.Sprite(
                        img=self.image, batch=self.batch
                    )
                    self.sprites[f"{i},{j},{k}"].position = tuple(
                        (
                            self.matHexCoord
                            @ (pyglet.math.Vec3(i, j, k))
                            * self.image.width
                        )
                        + self.anchor
                    )
                    self.sprites[f"{i},{j},{k}"].set_handler("on_press", onclick)
        # self.sprite = pyglet.sprite.Sprite(
        #     img=pyglet.resource.image("rawRsc/hexagonTiles/Tiles/tileGrass.png"),
        #     batch=self.batch,
        #     z=0,
        # )
        # self.sprite2 = pyglet.sprite.Sprite(
        #     img=pyglet.resource.image("rawRsc/hexagonTiles/Tiles/tileGrass_tile.png"),
        #     batch=self.batch,
        #     x=self.sprite.width,
        # )
        # self.sprite3 = pyglet.sprite.Sprite(
        #     img=pyglet.resource.image("rawRsc/hexagonTiles/Tiles/tileGrass.png"),
        #     batch=self.batch,
        #     y=25,
        #     z=1,
        # )
        print(self.image.height, self.image.width)
        # print(self.sprite.position, self.sprite2.position, self.sprite3.position)
        self.player: pyglet.sprite.Sprite = pyglet.sprite.Sprite(img=self.playerImage,x=self.width/2,y=self.height/2)

    def update(self, dt):
        self.anchor += self.anchorVelocity * dt
        for sprite in self.sprites.values():
            position: pyglet.math.Vec3 = pyglet.math.Vec3(*sprite.position)
            # print(position + (self.anchorVelocity * dt))
            sprite.position = tuple(position + (self.anchorVelocity * dt))

    def on_draw(self) -> None:
        self.clear()
        pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)
        self.batch.draw()
        pyglet.gl.glDisable(pyglet.gl.GL_DEPTH_TEST)
        self.player.draw()
        self.fpsDisplay.draw()

    def on_key_press(self, symbol, modifiers):
        print(symbol, modifiers, pyglet.window.key.A)
        if symbol == pyglet.window.key.A:
            self.anchorVelocity.x += 100
        if symbol == pyglet.window.key.D:
            self.anchorVelocity.x += -100
        if symbol == pyglet.window.key.S:
            self.anchorVelocity.y += 100
        if symbol == pyglet.window.key.W:
            self.anchorVelocity.y += -100
        print(self.anchorVelocity)
        return super().on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        print(symbol, modifiers, pyglet.window.key.A)
        if symbol == pyglet.window.key.A:
            self.anchorVelocity.x -= 100
        if symbol == pyglet.window.key.D:
            self.anchorVelocity.x -= -100
        if symbol == pyglet.window.key.S:
            self.anchorVelocity.y -= 100
        if symbol == pyglet.window.key.W:
            self.anchorVelocity.y -= -100
        print(self.anchorVelocity)

    def on_mouse_press(self, x, y, button, modifiers):
        print(x, y, button, modifiers)
        p = pyglet.math.Vec3(x, y, 1)
        invp = self.matInverse @ (p - self.anchor) / self.image.width
        if (
            self.sprites[f"{int(np.round(invp.x))},{int(np.round(invp.y))},{0}"].image
            == self.image_tile
        ):
            self.sprites[
                f"{int(np.round(invp.x))},{int(np.round(invp.y))},{0}"
            ].image = self.image
        else:
            self.sprites[
                f"{int(np.round(invp.x))},{int(np.round(invp.y))},{0}"
            ].image = self.image_tile
        print(
            p,
            self.matInverse @ p / self.image.width,
            f"{int(np.round(invp.x))},{int(np.round(invp.y))},{0}",
        )
        return


if __name__ == "__main__":
    menuWindow = MenuWindow(caption="Test")
    pyglet.app.run(0)
