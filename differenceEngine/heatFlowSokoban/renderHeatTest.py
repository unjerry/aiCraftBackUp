import moderngl as mgl
import pygame as pg
import numpy as np
import cv2

FIGURE = (50 * 16, 50 * 16)
WINDOWSIZE = (600, 600)
BACKGROUNDCOLOR = (12, 40, 100)
IS_PLAY = True

pg.init()
mainScreen = pg.display.set_mode(WINDOWSIZE, pg.OPENGL | pg.DOUBLEBUF)
mainClock = pg.time.Clock()

ctx = mgl.create_context(require=460)
numpyArrayOfTheTexture = np.frombuffer(
    cv2.imread("./firstgai.png", cv2.IMREAD_UNCHANGED), dtype=np.float32
)
texture = ctx.texture(FIGURE, 1, dtype="f4")
texture.write(numpyArrayOfTheTexture)
texture.use(0)
quadData = np.array(
    [
        [-1.0, -1.0, 0.0, 0.0],
        [1.0, -1.0, 1.0, 0.0],
        [-1.0, 1.0, 0.0, 1.0],
        [1.0, 1.0, 1.0, 1.0],
    ],
    dtype="f",
)
quadBuffer = ctx.buffer(data=quadData)

with open(f"assets/shaders/quadFrag.glsl") as file:
    quadFragSource = file.read()
with open(f"assets/shaders/quadVert.glsl") as file:
    quadVertSource = file.read()
shaderProgram = ctx.program(
    vertex_shader=quadVertSource, fragment_shader=quadFragSource
)
vao = ctx.vertex_array(shaderProgram, [(quadBuffer, "2f 2f", "vert", "uvs")])
shaderProgram["tex"] = 0

while IS_PLAY:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            IS_PLAY = False

    mainScreen.fill(BACKGROUNDCOLOR)

    vao.render(mgl.TRIANGLE_STRIP)

    pg.display.flip()
    mainClock.tick()
