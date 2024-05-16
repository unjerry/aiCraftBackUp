# https://www.youtube.com/watch?v=GMUhXMw1zZE
# https://www.youtube.com/watch?v=GMUhXMw1zZE
import pyglet
from pyglet.graphics.shader import Shader, ShaderProgram, ComputeShaderProgram
from pyglet.gl import GL_TRIANGLES,GL_LINES
from pyglet.math import Mat4, Vec3, Vec4, Vec2

with open("shaders/vert1.glsl", "r") as file:
    vert_shader = file.read()
with open("shaders/frag1.glsl", "r") as file:
    frag_shader = file.read()

opengl_config = pyglet.gl.Config(minor_version=6, major_version=4)
window = pyglet.window.Window(
    width=500, height=500, caption="test2", resizable=True, config=opengl_config
)
window.set_location(100, 100)
window.set_minimum_size(100, 100)
icon_image = pyglet.image.load("../images/compositionIcon.png")
window.set_icon(icon_image)

vert = Shader(vert_shader, "vertex")
frag = Shader(frag_shader, "fragment")
program = ShaderProgram(vert, frag)


view_mat = Mat4.from_translation(Vec3(0, 0, -1))
proj_mat = Mat4.orthogonal_projection(0, 100, 0, 200, 0.01, 100)

vp = proj_mat @ view_mat

batch = pyglet.graphics.Batch()

# program.vertex_list(
#     3,
#     GL_TRIANGLES,
#     batch=batch,
#     vert=("f", (-0.5, -0.5, 0.5, -0.5, 0.0, 0.5)),
#     col=("f", (1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1)),
# )

program.vertex_list_indexed(
    4,
    GL_LINES,
    indices=(0, 1, 3, 0, 2, 1),
    batch=batch,
    vert=("f", (-0.5, -0.5, -0.5, 0.5, 0.5, -0.5, 0.5, 0.5)),
    col=("f", (1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1)),
)


@window.event
def on_draw():
    window.clear()
    batch.draw()


pyglet.app.run()
