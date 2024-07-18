import pyglet
import os
import entiti

# pyglet.sprite.fragment_source = """#version 150 core
#     in vec4 vertex_colors;
#     in vec3 texture_coords;
#     out vec4 final_colors;

#     uniform sampler2D sprite_texture;

#     void main()
#     {
#         final_colors = texture(sprite_texture, texture_coords.xy) * vertex_colors;

#         // No GL_ALPHA_TEST in core, use shader to discard.
#         if(final_colors.a < 0.01){
#             discard;
#         }
#     }
# """


class assetsManager(entiti.entiti):
    def __init__(self, **karg) -> None:
        super().__init__(**karg)
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


mainAssets: assetsManager = assetsManager(folder="artAssets/mainAssets/")
window: pyglet.window.Window = pyglet.window.Window(resizable=True, caption="dsd")
window.set_vsync(False)
fpsDisplay: pyglet.window.FPSDisplay = pyglet.window.FPSDisplay(window=window)
batch: pyglet.graphics.Batch = pyglet.graphics.Batch()
batch2: pyglet.graphics.Batch = pyglet.graphics.Batch()
grp0: pyglet.graphics.Group = pyglet.graphics.Group(0)
grp1: pyglet.graphics.Group = pyglet.graphics.Group(1)
sprite: pyglet.sprite.Sprite = pyglet.sprite.Sprite(
    mainAssets.dirt, z=3, batch=batch, subpixel=True
)
sprite2: pyglet.sprite.Sprite = pyglet.sprite.Sprite(
    mainAssets.dirt, z=3, batch=batch, subpixel=True, x=100
)
lis: list[pyglet.sprite.Sprite] = [
    pyglet.sprite.Sprite(mainAssets.dirt, z=3, batch=batch, subpixel=True, x=i * 100)
    for i in range(1000)
]
for it in lis:
    it.scale*=10
    it.opacity=100
grass: pyglet.sprite.Sprite = pyglet.sprite.Sprite(
    mainAssets.grass, batch=batch2, z=1, subpixel=True
)
sprite.scale *= 10
grass.scale *= 20
sprite.opacity = 60
sprite2.scale *= 10


@window.event
def on_draw():
    pyglet.gl.glClearColor(0.35, 0.4, 0.65, 0.5)
    window.clear()
    # pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)
    # grass.draw()
    # sprite.draw()
    # batch2.draw()
    # batch.draw()
    # sprite2.draw()
    # sprite.draw()
    batch.draw()
    # for it in lis:
    #     it.draw()
    # pyglet.gl.glDisable(pyglet.gl.GL_DEPTH_TEST)
    fpsDisplay.draw()


pyglet.app.run(0)
