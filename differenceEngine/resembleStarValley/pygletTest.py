# pyglet test field
import pyglet

# pyglet.sprite.fragment_source = """#version 150 core
# in vec4 vertex_colors;
# in vec3 texture_coords;
# out vec4 final_colors;

# uniform sampler2D sprite_texture;

# void main()
# {
#     final_colors = texture(sprite_texture, texture_coords.xy) * vertex_colors;
#     if (final_colors.a < 1.0) discard;
# } """
window: pyglet.window.Window = pyglet.window.Window()
# ball_image = pyglet.image.load("RSV_2.png")
ball_image: pyglet.image.TextureRegion = pyglet.resource.image("RSV_2.png")
# ball = pyglet.sprite.Sprite(ball_image)
batch: pyglet.graphics.Batch = pyglet.graphics.Batch()
ball_sprites: list[pyglet.sprite.Sprite] = []
for i in range(100):
    x, y, z = i * 128, 5 * i, -i
    ball_sprites.append(pyglet.sprite.Sprite(img=ball_image, batch=batch))
    ball_sprites[-1].position = (x, y, z)


@window.event
def on_draw():
    window.clear()  # clear window
    pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)  # enable the z value test
    batch.draw()  # draw the batch


pyglet.app.run()
