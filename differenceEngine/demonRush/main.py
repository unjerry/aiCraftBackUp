import moderngl
import cv2
import array
import numpy as np
import pandas as pd
import pygame

pygame.init()
screen=pygame.display.set_mode((500,500),pygame.OPENGL|pygame.DOUBLEBUF)
ctx = moderngl.create_context(require=430)

raa = cv2.imread("./assets/images/ore/ore.png", cv2.IMREAD_UNCHANGED)

cv2.imwrite("./assets/images/ore/ore1_1.png", raa[220:350, 330:470, :])
cv2.imwrite("./assets/images/ore/ore1_2.png", raa[220:350, 490:640, :])
cv2.imwrite("./assets/images/ore/ore1_3.png", raa[220:350, 640 : 840 - 20, :])
# cv2.imwrite("./assets/images/ore/ore1_4.png",raa[220:350,1040-40:1040-60,:])

cv2.imwrite("./assets/images/ore/ore1_5.png", raa[220:350, 1200:1400, :])
cv2.imwrite("./assets/images/ore/ore1_6.png", raa[220:350, 1400:1500, :])
cv2.imwrite("./assets/images/ore/ore1_7.png", raa[220:350, 1500:1600, :])
print(raa[220, 330, :])

with open("./frag.glsl", "r") as file:
    fragment_shader_source = file.read()
with open("./vert.glsl", "r") as file:
    vertex_shader_source = file.read()

rrr = pd.read_csv("./quad.uvs", sep=",")
nn=rrr.to_numpy(dtype="f")
print(nn.dtype)
print(nn.tobytes())
print(nn)
quad_buffer = ctx.buffer(
    data=nn.tobytes()
)
print(array.array(
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
    ))
print(quad_buffer.read())
# quad_buffer = ctx.buffer(data=np.frombuffer(rrr.to_numpy().tobytes(), dtype=np.uint8))
program = ctx.program(
    vertex_shader=vertex_shader_source, fragment_shader=fragment_shader_source
)
vao = ctx.vertex_array(program, [(quad_buffer, "2f 2f", "vert", "texcoord")])

vao.render(moderngl.TRIANGLE_STRIP)
# pygame.display.flip()

raa = np.frombuffer(vao.ctx.fbo.read((500,500),4), dtype=np.uint8)
print(np.reshape(raa, (500 , 500 , -1))[0,0,:])
import cv2

# print(np.reshape(raa,(500,500,-1)).shape)
cv2.imwrite("./first.png", np.reshape(raa, (500 , 500 , -1)))

# print(raa.shape[])
