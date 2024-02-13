import pygame
import moderngl

pygame.init()
main_screen = pygame.display.set_mode((800, 600))
main_clock = pygame.time.Clock()
section = pygame.Surface((500, 500))
ctx1 = moderngl.create_context(standalone=True, require=430)
tex = ctx1.texture((500, 500), 4, dtype="f1")
pre_tex = ctx1.texture((500, 500), 4, dtype="f1")
tex.use(0)
pre_tex.use(1)
tex.bind_to_image(0, read=False, write=True)
pre_tex.bind_to_image(1, read=True, write=False)
comp_shader_source = """
#version 460 core
layout(local_size_x=1,local_size_y=1,local_size_z=1) in;
layout(rgba8,binding=0) uniform image2D screen;
layout(rgba8,binding=1) uniform image2D pre_screen;

void main()
{
    ivec2 pixel_coords=ivec2(gl_GlobalInvocationID.xy);
    
    vec4 col = imageLoad(pre_screen, pixel_coords);
    float a = col.r;
    
    float num = 0.0;
    for(int i = -1; i < 2; i++) {
        for(int j = -1; j < 2; j++) {
        int x = pixel_coords.x+i ;
        int y = pixel_coords.y+j  ;
        x=(x+500)%500;
        y=(y+500)%500;
        num += imageLoad(pre_screen, ivec2(x, y)).b;
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
    vec4 pixel=vec4(a,a,a,1.0);
    imageStore(screen,pixel_coords,pixel);
}
"""
cps = ctx1.compute_shader(comp_shader_source)
cps.run(500, 500, 1)
import numpy as np

raa = np.frombuffer(tex.read(), dtype=np.uint8)
import cv2

cv2.imwrite("./first.png", np.reshape(raa, (500, 500, -1)))
tex_image = pygame.image.frombuffer(tex.read(), tex.size, "BGRA")
init_image = pygame.image.load("./img.png")
section.blit(init_image, (0, 0))
tex.write(section.get_buffer())
pre_tex.write(tex.read())


is_running = 1
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = 0
    main_screen.fill((0, 0, 0))
    cps.run(500, 500, 1)
    tex_image = pygame.image.frombuffer(pre_tex.read(), tex.size, "BGRA")
    # raa = np.frombuffer(pre_tex.read(), dtype=np.uint8)
    # cv2.imwrite("./first.png", np.reshape(raa, (500, 500, -1)))
    # main_screen.blit(pygame.transform.scale_by(tex_image,5), pygame.mouse.get_pos())
    main_screen.blit(tex_image, pygame.mouse.get_pos())
    pygame.display.flip()
    delta_time = main_clock.tick(60)
    dtime = main_clock.get_time()
    time = pygame.time.get_ticks()
    # cps["time"] = time
    pygame.display.set_caption(
        f"fps:{main_clock.get_fps():3.0f}|{delta_time:2d}|{dtime:2d}|{time/1000:.0f}s"
    )
    pre_tex.write(tex.read())

pygame.quit()
