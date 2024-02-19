import moderngl as mgl
import numpy as np
import cv2

np.set_printoptions(linewidth=400)

ctx = mgl.create_context(standalone=True, require=460)
with open(f"assets/shaders/heatSimulator.glsl") as file:
    computeShaderSource = file.read()
computeShaderProgram = ctx.compute_shader(computeShaderSource)

inField = ctx.texture((10, 10), 1, dtype="f4")
outField = ctx.texture((10, 10), 1, dtype="f4")
inField.use(0)
outField.use(1)
inField.bind_to_image(0, read=True, write=False)
outField.bind_to_image(1, read=False, write=True)
NP = 300 * np.ones((10, 10), dtype=np.float32)
NP[1][1] = 301
inField.write(NP)

rrr = np.frombuffer(inField.read(), dtype=np.float32)
print(np.reshape(rrr, (10, 10)))
rrr = np.frombuffer(outField.read(), dtype=np.float32)
print(np.reshape(rrr, (10, 10)))

for i in range(1000000):
    computeShaderProgram.run(10, 10, 1)
    inField.write(outField.read())
rrr = np.frombuffer(inField.read(), dtype=np.float32)
print(np.reshape(rrr, (10, 10)))
