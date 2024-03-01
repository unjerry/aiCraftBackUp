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
    cv2.imread("./first.png", cv2.IMREAD_UNCHANGED), dtype=np.float32
)
inField = ctx.texture(FIGURE, 1, dtype="f4")
outField = ctx.texture(FIGURE, 1, dtype="f4")
inField.write(numpyArrayOfTheTexture)
inField.use(0)
quadData = np.array(
    [
        [-1.0, -1.0, 0.0, 1.0],
        [1.0, -1.0, 1.0, 1.0],
        [-1.0, 1.0, 0.0, 0.0],
        [1.0, 1.0, 1.0, 0.0],
    ],
    dtype="f",
)
quadBuffer = ctx.buffer(data=quadData)

with open(f"assets/shaders/quadFrag.glsl") as file:
    quadFragSource = file.read()
with open(f"assets/shaders/quadVert.glsl") as file:
    quadVertSource = file.read()
with open(f"assets/shaders/heatSimulator.glsl") as file:
    computeSource = file.read()
shaderProgram = ctx.program(
    vertex_shader=quadVertSource, fragment_shader=quadFragSource
)
computeProgram = ctx.compute_shader(computeSource)
vao = ctx.vertex_array(shaderProgram, [(quadBuffer, "2f 2f", "vert", "uvs")])
shaderProgram["tex"] = 0

i = 0
while IS_PLAY:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            IS_PLAY = False

    inField.bind_to_image((i) % 2, read=(i + 1) % 2, write=(i) % 2)
    outField.bind_to_image((i + 1) % 2, read=(i) % 2, write=(i + 1) % 2)
    computeProgram.run(50, 50, 1)
    mainScreen.fill(BACKGROUNDCOLOR)

    vao.render(mgl.TRIANGLE_STRIP)

    pg.display.flip()
    pg.display.set_caption(f"fps:{mainClock.get_fps():.0f}")
    mainClock.tick()
    i = (i + 1) % 2
rrr = np.frombuffer(inField.read(), dtype=np.float32)
rri = np.frombuffer(inField.read(), dtype=np.uint8)
print(np.reshape(rrr, (50 * 16, 50 * 16)))
print(np.reshape(rrr, (50 * 16, 50 * 16))[46 * 16 : 47 * 16, :16])
cv2.imwrite("./firstim.png", np.reshape(rri, (50 * 16, 50 * 16, -1)))
