import pyglet
import entiti
import os
import math

# pyglet.sprite.fragment_source = """#version 150 core
# in vec4 vertex_colors;
# in vec3 texture_coords;
# out vec4 final_colors;

# uniform sampler2D loc_texture;

# void main()
# {
#     final_colors = texture(loc_texture, texture_coords.xy) * vertex_colors;
#     if (final_colors.a < 0.01) discard;
# } """


class assetsManager(entiti.entiti):
    def __init__(self, name: str, **karg) -> None:
        super().__init__(name, **karg)
        pyglet.image.Texture.default_mag_filter = (
            pyglet.image.Texture.default_min_filter
        ) = pyglet.gl.GL_NEAREST
        filenames: list[str] = os.listdir(self.folder)
        for itm in filenames:
            setattr(
                self,
                itm.split(".")[0],
                pyglet.resource.image(self.folder + itm),
            )
        print("Assets load finished")


if __name__ == "__main__":
    mainAssets = assetsManager("mainAssets", folder="artAssets/mainAssets/")
    mainGrid = entiti.tyleMap("mainGrid")
    config = pyglet.gl.Config(double_buffer=True)
    window = pyglet.window.Window(resizable=True, config=config)
    window.set_vsync(False)
    batch = pyglet.graphics.Batch()
    batch_1 = pyglet.graphics.Batch()
    sprites = {}
    sprites_dark = {}
    for key, itt in mainGrid.gridMap.items():
        key: str
        itt: entiti.tyleBlock
        sprite = pyglet.sprite.Sprite(
            getattr(mainAssets, itt.type),
            group=pyglet.graphics.Group(-1),
            batch=batch,
        )
        sprite.gridLoc = (int(key.split(";")[0]), int(key.split(";")[1]))
        # sprite.visible = False
        sprites[key] = sprite
        # add darkness
        sprite = pyglet.sprite.Sprite(
            getattr(mainAssets, "darkness"),
            # group=pyglet.graphics.Group(-1),
            z=0,
            batch=batch_1,
        )
        sprite.opacity = 100
        sprite.ilum = 0
        sprite.gridLoc = (int(key.split(";")[0]), int(key.split(";")[1]))
        sprites_dark[key] = sprite

    # sprite: pyglet.sprite.Sprite = pyglet.sprite.Sprite(
    #     mainAssets.dirt, group=pyglet.graphics.Group(3), batch=batch
    # )
    # sprite.scale *= 16
    # sprite.initposition = (0, 0, 0)
    # sprite.opacity = 100
    # darkness = pyglet.sprite.Sprite(mainAssets.brightness,batch=batch_1,z=1)
    # darkness.scale = 20
    # darkness.opacity =100

    anchor_p: pyglet.math.Vec2 = pyglet.math.Vec2(0, 0)
    anchor_v: pyglet.math.Vec2 = pyglet.math.Vec2(0, 0)
    anchor_v_mul = 1
    scl = 16
    angle = 0
    fpsDisplay: pyglet.window.FPSDisplay = pyglet.window.FPSDisplay(
        window=window,
        color=(0, 0, 0, 128),
    )

    pyglet.gl.glClearColor(0.35, 0.4, 0.65, 0.5)

    @window.event
    def on_draw():
        window.clear()
        batch.draw()
        # pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)
        batch_1.draw()
        fpsDisplay.draw()
        # pyglet.gl.glDisable(pyglet.gl.GL_DEPTH_TEST)

    @window.event
    def on_key_press(symbol, modifiers):
        global anchor_v_mul
        if symbol == pyglet.window.key.A:
            anchor_v.x += -5
        if symbol == pyglet.window.key.D:
            anchor_v.x += 5
        if symbol == pyglet.window.key.S:
            anchor_v.y += -5
        if symbol == pyglet.window.key.W:
            anchor_v.y += 5
        if (
            symbol == pyglet.window.key.LSHIFT
            or symbol == pyglet.window.key.RSHIFT
            or symbol == pyglet.window.key.SPACE
        ):
            anchor_v_mul *= 2
        print("ON_KEY_PRESS.window", symbol, modifiers, pyglet.window.key.A)

    @window.event
    def on_key_release(symbol, modifiers):
        global anchor_v_mul
        if symbol == pyglet.window.key.A:
            anchor_v.x -= -5
        if symbol == pyglet.window.key.D:
            anchor_v.x -= 5
        if symbol == pyglet.window.key.S:
            anchor_v.y -= -5
        if symbol == pyglet.window.key.W:
            anchor_v.y -= 5
        if (
            symbol == pyglet.window.key.LSHIFT
            or symbol == pyglet.window.key.RSHIFT
            or symbol == pyglet.window.key.SPACE
        ):
            anchor_v_mul /= 2
        print("ON_KEY_RELEASE.window", symbol, modifiers, pyglet.window.key.A)

    @window.event
    def on_mouse_scroll(x, y, scroll_x, scroll_y):
        print("PRINT_onMouse_scroll", x, y, scroll_x, scroll_y)
        global scl
        scl *= 1.1 ** (scroll_y)
        if scl < 8:
            scl = 8
        if scl > 100:
            scl = 100
        # if self.pldrone.drone.data["itemSelected"] < 0:
        #     self.pldrone.drone.data["itemSelected"] = 0

    def update(dt: float) -> None:
        global anchor_p, angle
        anchor_p += anchor_v * dt * anchor_v_mul
        angle += dt * 2 * math.pi / 60
        for sprite in sprites.values():
            sprite: pyglet.sprite.Sprite
            dif_frac: pyglet.math.Vec2 = pyglet.math.Vec2(*sprite.gridLoc) - anchor_p
            sprite.position = (
                (dif_frac * scl)[0] + window.width / 2,
                (dif_frac * scl)[1] + window.height / 2,
                0,
            )
            sprite.scale = scl / 16
        for sprite in sprites_dark.values():
            sprite: pyglet.sprite.Sprite
            dif_frac: pyglet.math.Vec2 = pyglet.math.Vec2(*sprite.gridLoc) - anchor_p
            sprite.position = (
                (dif_frac * scl)[0] + window.width / 2,
                (dif_frac * scl)[1] + window.height / 2,
                sprite.position[2],
            )
            sprite.scale = scl / 16
            sprite.opacity = 255 * (math.sin(angle) + 1) / 2
        for val in sprites_dark.values():
            val: pyglet.sprite.Sprite
            x, y = val.gridLoc
            if mainGrid.gridMap[f"{x};{y}"].type == "dirtOnGrass00000000":
                val.ilum = 5
            else:
                # vv = val.ilum - 0.2 * (6 - val.ilum)
                vv = 0
                num=0
                if f"{x+1};{y}" in sprites_dark:
                    vv += sprites_dark[f"{x+1};{y}"].ilum
                    num+=1
                if f"{x};{y+1}" in sprites_dark:
                    vv += sprites_dark[f"{x};{y+1}"].ilum
                    num+=1
                if f"{x-1};{y}" in sprites_dark:
                    vv += sprites_dark[f"{x-1};{y}"].ilum
                    num+=1
                if f"{x};{y-1}" in sprites_dark:
                    vv += sprites_dark[f"{x};{y-1}"].ilum
                    num+=1
                vv /= 4
                vv -= 0.01
                val.ilum += 0.1 * (vv - val.ilum)
            val.ilum = max(val.ilum, 0)
            # val.opacity -= val.ilum * 51
            val.opacity -= val.ilum * 100
            val.opacity = max(val.opacity, 0)
            val.opacity = min(val.opacity, 255)

        print("UPDATE.window", anchor_p, anchor_v)

    pyglet.clock.schedule_interval(update, 1 / 60)
    pyglet.app.run(0)
