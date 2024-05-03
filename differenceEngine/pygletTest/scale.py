import pyglet
import pyglet.gl as gl

image = pyglet.resource.image("artAssets/Designer.png")
texture = image.get_texture()
gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
texture.width = 16  # resize from 8x8 to 16x16
texture.height = 16
texture.blit(100, 30)  # draw
pyglet.app.run()
