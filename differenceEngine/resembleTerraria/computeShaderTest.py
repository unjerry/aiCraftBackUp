import moderngl
import cv2
import numpy as np

imgg = cv2.imread("./artAssets/mainAssets/RST.png", cv2.IMREAD_UNCHANGED)
print(imgg)

ctx1 = moderngl.create_context(standalone=True, require=430)
tex = ctx1.texture((16, 16), 4, dtype="f1")
tex.use(0)
tex.bind_to_image(0, read=False, write=True)

pre_tex = ctx1.texture((16, 16), 4, dtype="f1")
pre_tex.use(1)
pre_tex.bind_to_image(1, read=True, write=False)

tex.write(imgg)
pre_tex.write(tex.read())

comp_shader_source = """
#version 430 core
layout(local_size_x=1,local_size_y=1,local_size_z=1) in;
layout(rgba8,binding=0) uniform image2D screen;
layout(rgba8,binding=1) uniform image2D pre_screen;

void main()
{
    ivec2 pixel_coords=ivec2(gl_GlobalInvocationID.xy);
    
    vec4 col = imageLoad(pre_screen, pixel_coords);
    float a = col.a;
    
    float num = 0.0;
    for(int i = -1; i < 2; i++) {
        for(int j = -1; j < 2; j++) {
        int x = pixel_coords.x+i ;
        int y = pixel_coords.y+j  ;
        x=(x+16)%16;
        y=(y+16)%16;
        num += imageLoad(pre_screen, ivec2(x, y)).a;
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
    vec4 pixel=vec4(0.0,0.0,0.0,a);
    imageStore(screen,pixel_coords,pixel);
}
"""
cps = ctx1.compute_shader(comp_shader_source)
cps.run(16, 16, 1)

raa = np.frombuffer(pre_tex.read(), dtype=np.uint8)
cv2.imwrite("./first.png", np.reshape(raa, (16, 16, -1)))
raa = np.frombuffer(tex.read(), dtype=np.uint8)
cv2.imwrite("./first1.png", np.reshape(raa, (16, 16, -1)))

