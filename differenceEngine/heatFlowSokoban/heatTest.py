import moderngl as mgl
import numpy as np
import cv2

np.set_printoptions(linewidth=400)

ctx = mgl.create_context(standalone=True, require=460)
with open(f"assets/shaders/heatSimulator.glsl") as file:
    computeShaderSource = file.read()
computeShaderProgram = ctx.compute_shader(computeShaderSource)

inField = ctx.texture((50 * 16, 50 * 16), 1, dtype="f4")
outField = ctx.texture((50 * 16, 50 * 16), 1, dtype="f4")
inField.use(0)
outField.use(1)
inField.bind_to_image(0, read=True, write=False)
outField.bind_to_image(1, read=False, write=True)
# NP = 300 * np.ones((10, 10), dtype=np.float32)
# NP[1][1] = 301
NP = np.frombuffer(cv2.imread("./first.png", cv2.IMREAD_UNCHANGED), dtype=np.float32)
print(NP[: 16 * 3])
print(np.reshape(NP, (50 * 16, 50 * 16, -1)).shape)
inField.write(NP)

rrr = np.frombuffer(inField.read(), dtype=np.float32)
print(np.reshape(rrr, (50 * 16, 50 * 16)))
rrr = np.frombuffer(outField.read(), dtype=np.float32)
print(np.reshape(rrr, (50 * 16, 50 * 16)))

for i in range(10000):
    computeShaderProgram.run(50, 50, 1)
    inField.write(outField.read())
rrr = np.frombuffer(inField.read(), dtype=np.float32)
rri = np.frombuffer(inField.read(), dtype=np.uint8)
print(np.reshape(rrr, (50 * 16, 50 * 16)))
print(np.reshape(rrr, (50 * 16, 50 * 16))[46 * 16 : 47 * 16, :16])
# print(np.reshape(rrr, (50 * 16, 50 * 16))[:16, 16:32])
cv2.imwrite("./firstgai.png", np.reshape(rri, (50 * 16, 50 * 16, -1)))