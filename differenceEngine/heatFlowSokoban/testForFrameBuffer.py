import moderngl as mgl
import numpy as np
import cv2

ctx = mgl.create_context(standalone=True, require=460)
NP = np.frombuffer(cv2.imread("./first.png", cv2.IMREAD_UNCHANGED), dtype=np.float32)
# print(NP[: 16 * 3])
# print(np.reshape(NP, (50 * 16, 50 * 16, -1)).shape)


tex = ctx.texture((2, 1), 1, dtype="f4")
buf = ctx.framebuffer(tex)
tex.write(NP[0:2])
# print(np.frombuffer(tex.read(), dtype="f4"))
print(buf.read((0, 0, 2, 1), dtype="f4", components=1))
print(buf.color_attachments[0].read())
print(tex.read())
