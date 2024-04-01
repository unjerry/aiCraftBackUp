# https://www.youtube.com/watch?v=GMUhXMw1zZE
# https://www.youtube.com/watch?v=GMUhXMw1zZE
import pyglet
import moderngl as mgl
import array

vert_shader = """
#version 460 core

in vec2 vert;
in vec2 texcoord;

void main()
{
    gl_Position=vec4(vert,0.0,1.0);
}
"""
frag_shader = """
#version 460 core


void main()
{
   gl_FragColor=vec4(1,1,1,1);
}
"""

config = pyglet.gl.Config(minor_version=6,major_version=4)
window = pyglet.window.Window(width=500, height=500, caption="test2gai",resizable=True,config=config)
window.set_location(10, 10)
icon_image=pyglet.image.load("../images/compositionIcon.png")
window.set_icon(icon_image)

ctx=mgl.create_context(require=460)
quad_buffer = ctx.buffer(
    data=array.array(
        "f",
        [
            -0.5,
            -0.5,
            0.0,
            0.0,
            1.0,
            -1.0,
            1.0,
            0.0,
            -1.0,
            1.0,
            0.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
        ],
    )
)

# vert = Shader(vert_shader, "vertex")
# frag = Shader(frag_shader, "fragment")
# program = ShaderProgram(vert, frag)

program=ctx.program(vertex_shader=vert_shader,fragment_shader=frag_shader)
vao = ctx.vertex_array(program, [(quad_buffer, "2f 2f", "vert", "texcoord")])
vao.render(mgl.TRIANGLE_STRIP)

# batch = pyglet.graphics.Batch()

# program.vertex_list(
#     3, GL_TRIANGLES, batch=batch, vert=("f", (-0.5, -0.5, 0.5, -0.5, 0.0, 0.5))
# )




@window.event
def on_draw():
    window.clear()
    vao.render(mgl.TRIANGLE_STRIP)
    # batch.draw()


pyglet.app.run()
