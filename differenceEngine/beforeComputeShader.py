import moderngl as gl
import moderngl_window as glw
from moderngl_window.conf import settings
import array

# settings.WINDOW["class"] = "moderngl_window.context.glfw.Window"
# settings.WINDOW["gl_version"] = (4, 6)
# settings.WINDOW["size"] = (500, 500)
# window = moderngl_window.create_window_from_settings()
window_cls = glw.get_local_window_cls("glfw.window")
window = window_cls(
    size=(500, 500),
    fullscreen=False,
    title="ModernGL Window",
    resizable=False,
    vsync=True,
    gl_version=(4, 3),
)
ctx = window.ctx
quad_buffer = ctx.buffer(
    data=array.array(
        "f",
        [
            -.5,-.9,0.0,0.0,
            1.0,-1.0,0.0,0.0,
            -1.0,1.0,0.0,1.0,
            .5,.5,1.0,0.0,
        ],
    )
)
vert_shader = """
#version 460 core

in vec2 vert;
in vec2 texcoord;
out vec2 uvs;

void main()
{
    uvs=texcoord;
    gl_Position=vec4(vert,0.0,1.0);
}
"""
frag_shader = """
#version 460 core

in vec2 uvs;
out vec4 f_color;

void main()
{
   f_color=vec4(uvs/2.0+0.5,0.0,1.0);
}
"""
program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
render_object = ctx.vertex_array(program, [(quad_buffer, "2f 2f", "vert", "texcoord")])


while not window.is_closing:
    window.fbo.clear(0.0, 0.0, 0.0, 1.0)
    render_object.render(gl.TRIANGLE_STRIP)
    window.swap_buffers()
