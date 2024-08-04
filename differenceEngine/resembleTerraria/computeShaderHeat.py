import moderngl
import cv2
import numpy as np
import pyglet

imgg = cv2.imread("./artAssets/mainAssets/RST.png", cv2.IMREAD_UNCHANGED)
print(imgg)

ctx1 = moderngl.create_context(standalone=True, require=430)
config = pyglet.gl.Config(double_buffer=True, major_version=4, minor_version=3)
window = pyglet.window.Window(resizable=True, config=config)
window.set_vsync(False)
tex = ctx1.texture((960, 540), 4, dtype="f1")
tex.use(0)
tex.bind_to_image(0, read=False, write=True)

pre_tex = ctx1.texture((960, 540), 4, dtype="f1")
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
        x=(x+960)%960;
        y=(y+540)%540;
        num += imageLoad(pre_screen, ivec2(x, y)).a;
        }
    }
    num /= 4.0;

    float b =a+(num-a)*0.5;
  
    vec4 pixel=vec4(0.0,0.0,0.0,b);
    imageStore(screen,pixel_coords,pixel);
}
"""
cps = ctx1.compute_shader(comp_shader_source)
cps.run(960, 540, 1)

raa = np.frombuffer(pre_tex.read(), dtype=np.uint8)
print(raa)
cv2.imwrite("./first.png", np.reshape(raa, (960, 540, -1)))
raa = np.frombuffer(tex.read(), dtype=np.uint8)
cv2.imwrite("./first1.png", np.reshape(raa, (960, 540, -1)))

print(np.frombuffer(pre_tex.read(), dtype=np.uint8))

print(np.frombuffer(pre_tex.read(), dtype=np.uint8))

fpsDisplay: pyglet.window.FPSDisplay = pyglet.window.FPSDisplay(
    window=window,
    color=(0, 0, 0, 128),
)

pyglet.gl.glClearColor(0.35, 0.4, 0.65, 0.5)
pyglet.image.Texture.default_mag_filter = pyglet.image.Texture.default_min_filter = (
    pyglet.gl.GL_NEAREST
)
hole = np.reshape(raa, (540, 960, -1))
quat = np.reshape(raa, (540, 960, -1))
A = np.array(quat)
A[270:, 480:,:] = hole[:270, :480,:]
A[:270, 480:,:] = hole[:270, :480,:]
A[270:, :480,:] = hole[:270, :480,:]
imm = pyglet.image.ImageData(960, 540, "RGBA", A, -960 * 4)
igm = pyglet.resource.image("artAssets/mainAssets/RST.png")
sp = pyglet.sprite.Sprite(igm, 0, 0, 0)
sp.scale = 2
tex.write(A)
print(np.frombuffer(pre_tex.read(), dtype=np.uint8))
# print(imm.get_texture().get_image_data())
# imm.blit_into(imgg,0,0,0)

pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

sp.x = 1
sp.y = 1


@window.event
def on_draw():
    window.clear()
    # imm.blit(100,100)
    sp.image
    sp.draw()
    # pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    # pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
    # imm.blit(100,100)
    fpsDisplay.draw()


def update(dt: float) -> None:
    pre_tex.write(tex.read())
    cps.run(960, 540, 1)
    imm.set_data("RGBA", -960 * 4, tex.read())


pyglet.clock.schedule_interval(update, 1 / 60)
pyglet.app.run(0)
