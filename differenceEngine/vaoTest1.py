import moderngl as gl
import moderngl_window as glw
import numpy as np
import array

ctx = gl.create_context(standalone=True, require=430)
quad_buffer = ctx.buffer(
    data=array.array(
        "f",
        [
            -1.0,
            -1.0,
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
print(quad_buffer.read())
vert_shader = """
#version 430 core

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
#version 430 core

in vec2 uvs;

void main()
{
   gl_FragColor=vec4(0.1,0.2,1.0,1.0);
}
"""

prgstr = """
#version 430 core
in float a;
void main()
{
    gl_Position=vec4(a,0.0,0.0,1.0);
}
"""
prgfrag = """
#version 430 core
void main()
{
    gl_FragColor=vec4(1.0,0.5,0.0,1.0);
}
"""

prg = ctx.program(vertex_shader=prgstr, fragment_shader=prgfrag)
render_object = ctx.vertex_array(prg, [(quad_buffer, "2f1 2f1", "vert","texcoord")])

render_object.render(gl.LINE_STRIP)

print(render_object.ctx.fbo)

# ctx.compute_shader()
