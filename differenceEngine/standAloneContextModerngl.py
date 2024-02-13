import moderngl as gl
import moderngl_window as glw
import numpy as np

ctx = gl.create_context(standalone=True)
# 100x100 RGBA8 texture attached to a framebuffer
fbo = ctx.framebuffer(
    color_attachments=[ctx.texture(size=(100, 100), components=4,dtype='f4')],
)
fbo.use()
# Fake some rendering (clear with red)
fbo.clear(1.0, 0.0, 0.0, 1.0)
# Byte data of the framebuffer we can for example
# dump into a Pillow image and show/save
data = fbo.read(components=4, dtype="f4")
print(data)
