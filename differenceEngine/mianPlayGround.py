import pygame
import sys
import moderngl
import array

pygame.init()

screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
display = pygame.Surface((800, 600))
disp = pygame.Surface((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

ctx = moderngl.create_context()
ctx.gc_mode = "auto"

img = pygame.transform.flip(
    pygame.transform.scale_by(pygame.image.load("./images/1.png"), (1.0, 1.0)),
    flip_x=0,
    flip_y=1,
)
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

B_shader = """
#version 430 core
uniform sampler2D tex;

in vec2 uvs;
uniform vec2 normalRes;

void main()
{
    float tao=0.1;
    
    float Ex = texture2D(tex, uvs).r;
    float Ey = texture2D(tex, uvs).g;
    float Ez = texture2D(tex, uvs).b;
    float EzY=texture2D(tex, vec2(uvs.x,uvs.y+1.0*normalRes.y)).b;
    float EzX=texture2D(tex, vec2(uvs.x+1.0*normalRes.x,uvs.y)).b;
    float ExY=texture2D(tex, vec2(uvs.x,uvs.y+1.0*normalRes.y)).r;
    float EyX=texture2D(tex, vec2(uvs.x+1.0*normalRes.x,uvs.y)).g;
    
    gl_FragColor=vec4(0.5,0.5,tao*((EyX-Ey+0.5)-(ExY-Ex+0.5)+0.5)/normalRes.y,1.);//-tao*(EzX-Ez)/normalRes.y,tao*(EzY-Ez)/normalRes.y,1.0);
    
}
"""
updater = """
#version 430 core
uniform sampler2D tex;
uniform sampler2D ori;

in vec2 uvs;

void main()
{
    
    gl_FragColor=vec4(texture(tex,uvs).bgr+texture(ori,uvs).bgr,1.0);
    
}
"""

E_shader = """
#version 430 core
uniform sampler2D tex;

in vec2 uvs;
uniform vec2 normalRes;
//out vec4 f_color;

void main()
{
    float tao=0.01;
    float s=100.0*normalRes.x;
    float k=10*tao*s*s/normalRes.x;
    
    float Bx = texture2D(tex, vec2(uvs.x,uvs.y)).b;
    float By = texture2D(tex, uvs).g;
    float Bz = texture2D(tex, uvs).r;
    float BzY=texture2D(tex, vec2(uvs.x,uvs.y+1.0*normalRes.y)).r;
    float BzX=texture2D(tex, vec2(uvs.x+1.0*normalRes.x,uvs.y)).r;
    float BxY=texture2D(tex, vec2(uvs.x,uvs.y+1.0*normalRes.y)).b;
    float BxX=texture2D(tex, vec2(uvs.x+1.0*normalRes.x,uvs.y)).b;
    float ByX=texture2D(tex, vec2(uvs.x+1.0*normalRes.x,uvs.y)).g;
    
    gl_FragColor=vec4(k*((ByX-By)-(BxY-Bx)),-k*(BzX-Bz),k*(BzY-Bz),1.0);
    //gl_FragColor=vec4(texture(tex,uvs).bgr,1.0);
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
frag_shader_simp = """
#version 430 core
uniform sampler2D tex;

in vec2 uvs;
out vec4 f_color;

void main()
{
   f_color=vec4(texture2D(tex, uvs).bgra);
}
"""

program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
E_program = ctx.program(vertex_shader=vert_shader, fragment_shader=E_shader)
B_program = ctx.program(vertex_shader=vert_shader, fragment_shader=B_shader)
UPDT_program = ctx.program(vertex_shader=vert_shader, fragment_shader=updater)
program_simp = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader_simp)
render_object = ctx.vertex_array(program, [(quad_buffer, "2f 2f", "vert", "texcoord")])
render_object_E = ctx.vertex_array(
    E_program, [(quad_buffer, "2f 2f", "vert", "texcoord")]
)
render_object_B = ctx.vertex_array(
    B_program, [(quad_buffer, "2f 2f", "vert", "texcoord")]
)
render_object_update = ctx.vertex_array(
    UPDT_program, [(quad_buffer, "2f 2f", "vert", "texcoord")]
)
render_object_simp = ctx.vertex_array(
    program_simp, [(quad_buffer, "2f 2f", "vert", "texcoord")]
)


frm = program["normalRes"]
frm.value = 1.0 / 800, 1.0 / 600
frm = E_program["normalRes"]
frm.value = 1.0 / 800, 1.0 / 600
frm = B_program["normalRes"]
frm.value = 1.0 / 800, 1.0 / 600

B = pygame.Surface((800, 600))
display.fill((128, 128, 128))

draw = 0
for i in range(5):
    # display.unlock()
    x, y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.image.save(pygame.transform.flip(display, 0, 1), "./final.png")
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            draw = 1
        if event.type == pygame.MOUSEBUTTONUP:
            draw = 0

    # if 1:
    display.blit(img, (100 + i * 11, 200))

    frame_tex = ctx.texture(display.get_size(),4)
    frame_tex.write(display.get_view())
    frame_tex.use(0)
    E_program["tex"] = 1
    frame_tex_B = ctx.texture(B.get_size(), 4)
    frame_tex_B.write(B.get_view())
    frame_tex_B.use(1)
    B_program["tex"] = 0
    # render_object.render(mode=moderngl.TRIANGLE_STRIP)
    render_object_B.render(mode=moderngl.TRIANGLE_STRIP)
    BUdp = pygame.image.frombuffer(
        render_object_B.ctx.fbo.read(components=4), render_object_E.ctx.fbo.size, "RGBA"
    )
    pygame.image.save(pygame.transform.flip(BUdp, 0, 1), f"outputs/BUdp{i}.png")
    # render_object_simp.render(mode=moderngl.TRIANGLE_STRIP)
    # render_object_B.render(mode=moderngl.TRIANGLE_STRIP)
    # EUdp = pygame.image.frombuffer(
    #     render_object_B.ctx.fbo.read(components=4), render_object_B.ctx.fbo.size, "BGRA"
    # )
    # pygame.image.save(pygame.transform.flip(EUdp, 0, 1), f"./EUdp{i}.png")
    # render_object_simp.render(mode=moderngl.TRIANGLE_STRIP)
    # EUdp_frame_tex = ctx.texture(EUdp.get_size(), 4)
    # EUdp_frame_tex.write(EUdp.get_view())
    # EUdp_frame_tex.use(2)
    # BUdp_frame_tex = ctx.texture(BUdp.get_size(), 4)
    # BUdp_frame_tex.write(BUdp.get_view())
    # BUdp_frame_tex.use(3)

    # UPDT_program["tex"] = 3
    # UPDT_program["ori"] = 1
    # render_object_update.render(mode=moderngl.TRIANGLE_STRIP)
    # BN = pygame.image.frombuffer(
    #     render_object_update.ctx.fbo.read(components=4),
    #     render_object_update.ctx.fbo.size,
    #     "RGBA",
    # )
    # B.blit(BN, (0, 0))
    # pygame.image.save(pygame.transform.flip(B, 0, 1), f"./B{i}.png")
    # render_object_simp.render(mode=moderngl.TRIANGLE_STRIP)

    # UPDT_program["tex"] = 2
    # UPDT_program["ori"] = 0
    # render_object_update.render(mode=moderngl.TRIANGLE_STRIP)
    # EN = pygame.image.frombuffer(
    #     render_object_update.ctx.fbo.read(components=4),
    #     render_object_update.ctx.fbo.size,
    #     "RGBA",
    # )
    # display.blit(EN, (0, 0))
    # pygame.image.save(pygame.transform.flip(display, 0, 1), f"./display{i}.png")
    # render_object_simp.render(mode=moderngl.TRIANGLE_STRIP)

    # # display.blit(display, (0, 0))

    # frame_texN = ctx.texture(display.get_size(), 4)
    # frame_texN.write(display.get_view())
    # frame_texN.use(0)
    # program["tex"] = 0
    # render_object_simp.render(mode=moderngl.TRIANGLE_STRIP)

    # with open("imaa","w") as file:
    # file.write(f"{aa.raw}")
    # with open("im","w") as file:
    # file.write(f"{render_object.ctx.fbo.read()}")
    # aa = display.get_buffer()
    # aa.write(render_object.ctx.fbo.read(components=4))
    # bb.write(render_object.ctx.fbo.read(components=4))
    # frame_tex = surf_to_texture(ll)
    # # frame_tex.swizzle="RGBA"
    # bb.write(frame_tex.ctx.fbo.read(components=4))
    # del aa
    # pygame.image.save(ll, "./imgl.png")
    # pygame.image.save(display, "./imgd.png")
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

    clock.tick(1)
