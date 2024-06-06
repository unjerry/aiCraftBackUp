# differenceEngine/graphicsEngine/main.py
# differenceEngine/pygletTest/test2.py
import pyglet
from pyglet.graphics.shader import Shader, ShaderProgram, ComputeShaderProgram
from pyglet.gl import GL_TRIANGLES
from pyglet.math import Mat4, Vec3, Vec4, Vec2


class GraphicsEngine(pyglet.window.Window):
    def __init__(self, winSize: tuple[int, int] = (1600 // 2, 900 // 2)):
        self.winSize: tuple[int, int] = winSize
        self.openglConfig: pyglet.gl.Config = pyglet.gl.Config(
            minor_version=3, major_version=3
        )
        super().__init__(
            *self.winSize, caption="test2", resizable=True, config=self.openglConfig
        )
        self.set_location(100, 100)
        self.set_minimum_size(100, 100)

        with open("shaders/vert1.glsl", "r") as file:
            vert_shader = file.read()
        with open("shaders/frag1.glsl", "r") as file:
            frag_shader = file.read()
        vert = Shader(vert_shader, "vertex")
        frag = Shader(frag_shader, "fragment")

        self.program: ShaderProgram = ShaderProgram(vert, frag)

        self.batch: pyglet.graphics.Batch = pyglet.graphics.Batch()
        self.program.vertex_list(
            3,
            GL_TRIANGLES,
            batch=self.batch,
            vert=("f", (-0.5, -0.5, 0.5, -0.5, 0.0, 0.5)),
            col=("f", (1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1)),
        )

    def on_draw(self):
        pyglet.gl.glClearColor(255, 255, 255, 255)
        self.clear()
        self.batch.draw()

    # def on_resize(self, width, height):
    #     print("resize", width, height)
    #     return super().on_resize(width, height)


if __name__ == "__main__":
    app = GraphicsEngine()
    pyglet.app.run(0)
