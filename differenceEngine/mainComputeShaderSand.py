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
    vec4 ucol = imageLoad(pre_screen, ivec2(pixel_coords.x,pixel_coords.y-1));
    vec4 dcol = imageLoad(pre_screen, ivec2(pixel_coords.x,pixel_coords.y+1));
    float a = col.r;
    float u = ucol.r;
    float d = dcol.r;
    
    float num=((a<0.9)?(0.0):(1.0));
    float um =((u<0.9)?(0.0):(1.0));
    float dm =((d<0.9)?(0.0):(1.0));
    
    float ll;
    if(um>0.8)
    {
        if(num>0.8&&dm<0.8)
        {
            ll=0.0;
        }
        else
        {
            
            ll=1.0;
        }
    }
    else
    {
        if(num>0.8&&dm>0.8)
        {
            
            ll=1.0;
        }
        else
        {
            ll=0.0;
        }
    }
    if(num>0.8&&dm>0.8)
    {
        vec4 ldcol = imageLoad(pre_screen, ivec2(pixel_coords.x-1,pixel_coords.y+1));
        vec4 rdcol = imageLoad(pre_screen, ivec2(pixel_coords.x+1,pixel_coords.y+1));
        float ld = ldcol.r;
        float rd = rdcol.r;
        float ldm =((ld<0.9)?(0.0):(1.0));
        float rdm =((rd<0.9)?(0.0):(1.0));

        if(ldm<0.8&&rdm<0.8)
        {
//            float noise1 nz;
  //          if(nz<0.0)
    //        {
                
      //      }
        }
    }
    if(pixel_coords.y==499&&num>0.8)
    {
        ll=1.0;
    }
    
    imageStore(screen,pixel_coords,vec4(ll,ll,ll,1.0));
    
    
}
"""
cps = ctx1.compute_shader(comp_shader_source)

cps.run(500, 500, 1)
import numpy as np

raa = np.frombuffer(tex.read(), dtype=np.uint8)
import cv2

cv2.imwrite("./first.png", np.reshape(raa, (500, 500, -1)))
tex_image = pygame.image.frombuffer(tex.read(), tex.size, "BGRA")
init_image = pygame.image.load("./images/img.png")
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
    raa = np.frombuffer(pre_tex.read(), dtype=np.uint8)
    # cv2.imwrite(f"./outputs/first{i}.png", np.reshape(raa, (500, 500, -1)))
    # main_screen.blit(pygame.transform.scale_by(tex_image,5), pygame.mouse.get_pos())
    main_screen.blit(tex_image, (10, 10))
    pygame.display.flip()
    delta_time = main_clock.tick()
    dtime = main_clock.get_time()
    time = pygame.time.get_ticks()
    # cps["time"] = time
    pygame.display.set_caption(
        f"fps:{main_clock.get_fps():3.0f}|{delta_time:2d}|{dtime:2d}|{time/1000:.0f}s"
    )
    pre_tex.write(tex.read())

pygame.quit()
