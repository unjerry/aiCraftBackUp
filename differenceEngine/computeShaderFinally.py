import pygame
import OpenGL
import moderngl
import array

pygame.init()
mainScreen = pygame.display.set_mode((500, 500), pygame.OPENGL | pygame.DOUBLEBUF)
mainClock = pygame.time.Clock()

ctx = moderngl.create_context(require=460)

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

uniform sampler2D screen;
in vec2 uvs;

void main()
{
   gl_FragColor=texture(screen,uvs);
}
"""
comp_shader = """
#version 460 core
layout(local_size_x=1,local_size_y=1,local_size_z=1) in;
layout(rgba8,binding=0) uniform image2D screen;
uniform float tt;
uniform float portion;

void main()
{
    vec4 pixel=vec4(0.075,0.133,0.173,1.0);
    ivec2 pixel_coords=ivec2(gl_GlobalInvocationID.xy);
    vec3 rgb=imageLoad(screen,pixel_coords).bgr;
    if((rgb.r*portion+rgb.b*(1.0-portion))/(rgb.r+rgb.g+rgb.b)>tt){
        
        imageStore(screen,pixel_coords,imageLoad(screen,pixel_coords).bgra);
    }
    else
    {
        imageStore(screen,pixel_coords,vec4(0.0,0.,0.,1.));
    }
}
"""
comp_shader_white = """
#version 460 core
layout(local_size_x=1,local_size_y=1,local_size_z=1) in;
layout(rgba32f,binding=0) uniform image2D screen;

void main()
{
    vec4 pixel=vec4(0.35,0.3,0.4,1.0);
    ivec2 pixel_coords=ivec2(gl_GlobalInvocationID.xy);
    imageStore(screen,pixel_coords,pixel);
}
"""

imgg = pygame.transform.flip(
    pygame.transform.scale_by(pygame.image.load("images/img.png"), (1.0, 1.0)),
    flip_x=0,
    flip_y=1,
)
dis = pygame.Surface((500, 500))
dis.blit(imgg, (0, 0))
tex = ctx.texture((500, 500), 4, dtype="f1")

# tex.write(dis.get_buffer().raw())
tex.use(0)
tex.bind_to_image(0, read=True, write=True)
program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
vao = ctx.vertex_array(program, [(quad_buffer, "2f 2f", "vert", "texcoord")])
cps = ctx.compute_shader(comp_shader)
cps2 = ctx.compute_shader(comp_shader_white)
cps2.run(500, 500, 1)
# imgg = pygame.tex(tex.read(), tex.size, "RGBA")
# print(imgg.get_buffer().raw)
import numpy as np

raa = np.frombuffer(tex.read(),dtype=np.uint8)
import cv2
# print(np.reshape(raa,(500,500,-1)).shape)
cv2.imwrite("./first.png",np.reshape(raa,(500*2,500*2,-1)))
raa=cv2.imread("./first.png",cv2.IMREAD_UNCHANGED)
tex.write(raa)
# pygame.image.save(imgg, "./imgg.png")
print(raa[:4*5])
# print(tex.read())
with open("varead", "w") as fie:
    fie.write(f"{vao.ctx.fbo.read()}")
print(tex.size)
print(vao.ctx.fbo.size)


isRunning = 1
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = 0
    tex.write(dis.get_view())
    cps["tt"]=pygame.mouse.get_pos()[0]/500
    cps["portion"]=pygame.mouse.get_pos()[1]/500
    cps.run(500, 500, 1)

    # cps2.run(500, 500, 1)
    vao.render(moderngl.TRIANGLE_STRIP)

    pygame.display.set_caption(f"{mainClock.get_fps():.0f}")
    pygame.display.flip()
    mainClock.tick()
