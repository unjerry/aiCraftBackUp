import pygame
import sys
import moderngl
import array
import pygame.camera

pygame.init()
pygame.camera.init()
# cameras = pygame.camera.list_cameras()
# cam = pygame.camera.Camera(cameras[0])
# cam.start()

screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
display = pygame.Surface((800, 600))
clock = pygame.time.Clock()

ctx = moderngl.create_context()
ctx.gc_mode = "auto"

img = pygame.transform.scale_by(pygame.image.load("images/img.png"), (0.5, 0.5))
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
uniform sampler2D tex;

in vec2 uvs;
uniform vec2 normalRes;
out vec4 f_color;

void main()
{
    vec4 col = texture2D(tex, uvs);
    float a = col.r;
    
    float num = 0.0;
    for(float i = -1.0; i < 2.0; i++) {
        for(float j = -1.0; j < 2.0; j++) {
        float x = uvs.x + i * normalRes.x;
        float y = uvs.y + j * normalRes.y;

        num += texture2D(tex, vec2(x, y)).r;
        }
    }
    num -= a;
  
    if(a > 0.5) {
        if(num < 1.5) {
            a = 0.0;
        }
        if(num > 3.5) {
            a = 0.0;
        }
    } else {
        if(num > 2.5 && num < 3.5) {
            a = 1.0;
        }
    }
    f_color=vec4(a,a,a,1.0);
}
"""

program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
render_object = ctx.vertex_array(program, [(quad_buffer, "2f 2f", "vert", "texcoord")])


def surf_to_texture(surf):
    tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = "BGRA"
    # ctx.copy_framebuffer(tex, render_object.ctx.fbo)
    tex.write(surf.get_view("1"))
    return tex


frm = program["normalRes"]
frm.value = 1.0 / 800, 1.0 / 600

ll = pygame.Surface((800, 600))
bb = ll.get_buffer()
while True:
    display.unlock()
    x, y = pygame.mouse.get_pos()
    display.blit(img, (x, 600-y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    frame_tex = surf_to_texture(display)
    frame_tex.use(0)
    program["tex"] = 0
    render_object.render(mode=moderngl.TRIANGLE_STRIP)
    # with open("imaa","w") as file:
    # file.write(f"{aa.raw}")
    # with open("im","w") as file:
    # file.write(f"{render_object.ctx.fbo.read()}")
    aa = display.get_buffer()
    aa.write(render_object.ctx.fbo.read(components=4))
    bb.write(aa.raw)
    del aa
    # pygame.image.save(ll,"./imgl.png")
    # pygame.image.save(display,"./imgd.png")
    # display.unlock()
    # print(render_object.ctx.fbo)
    # render_object.ctx.fbo.read_into(frame_tex.ctx.fbo.read())
    # print(frame_tex)
    # pygame.image.save(display, "./rrr.png")
    # cam.start()
    # image = cam.get_image()
    # pygame.image.save(pygame.display.get_surface(), "./rrl.png")

    pygame.display.set_caption(f"{clock.get_fps():.0f}")
    # screen.get_pitch
    # ctx.copy_framebuffer(frame_tex, render_object.ctx.fbo)
    # buffer = ctx.glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
    pygame.display.flip()

    # frame_tex.release()

    clock.tick(60)
