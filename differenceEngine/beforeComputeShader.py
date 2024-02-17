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
            # -1.0,-1.0,0.0,0.0,
            # 1.0,-1.0,1.0,0.0,
            # -1.0, 1.0,0.0,1.0,
            # 1.0, 1.0,1.0,1.0,
            -1.0,
            -1.0,
            0.0,0.0,
            0.0,0.0,
            1.0,
            -1.0,
            1.0,0.0,
            2.0,0.0,
            -1.0,
            1.0,
            0.0,1.0,
            -1.0,5.0,
            1.0,
            1.0,
            1.0,1.0,
            3.0,5.0,
        ],
    )
)
vert_shader = """
#version 460 core

in vec2 vert;
in vec2 texcoord;
in vec2 rr;
out vec2 uvs;
out vec2 uu;

void main()
{
    uvs=texcoord;
    uu=rr;
    gl_Position=vec4(vert,0.0,1.0);
}
"""
frag_shader = """
#version 460 core

in vec2 uvs;
in vec2 uu;
out vec4 f_color;

uniform sampler2D texx;

void main()
{
   f_color=vec4(texture(texx,uu).rgb,1.0);
}
"""
program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
render_object = ctx.vertex_array(program, [(quad_buffer, "2f 2f 2f", "vert", "texcoord","rr")])

import cv2
import numpy as np

rr = cv2.imread("./images/img4.png",cv2.IMREAD_UNCHANGED)
print(rr[:2,:2,:])
# rr=np.array(np.concatenate([rr,255*np.ones_like(rr[:,:,0:1])],axis=2))
# print(rr[:2,:2,:])
cv2.imwrite("./outputs/img4.png",rr)
tex = ctx.texture((rr.shape[1],rr.shape[0]), 4)
tex.write(rr)
print(tex.repeat_x)
tex.repeat_x=False
tex.repeat_y=False
tex.use(0)
program["texx"] = 0

while not window.is_closing:
    window.fbo.clear(0.0, 0.0, 0.0, 1.0)
    render_object.render(gl.TRIANGLE_STRIP)
    window.swap_buffers()
