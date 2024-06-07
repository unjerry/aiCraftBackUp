import ctypes
import pyglet

pyglet.options["shadow_window"] = False
pyglet.options["debug_gl"] = False
import pyglet.gl as gl

import math
import matrix
import shader

vertex_positions = [
    -0.5,
    0.5,
    0.0,
    -0.5,
    -0.5,
    0.0,
    0.5,
    -0.5,
    0.0,
    0.5,
    0.5,
    0.0,
]

indices = [
    0,
    1,
    2,  # first triangle
    0,
    2,
    3,  # second triangle
]


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create vertex array object
        self.vao = gl.GLuint(0)
        gl.glGenVertexArrays(1, ctypes.byref(self.vao))
        gl.glBindVertexArray(self.vao)
        # create vertex buffer object
        self.vbo = gl.GLuint(0)
        gl.glGenVertexArrays(1, ctypes.byref(self.vbo))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)

        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            ctypes.sizeof(gl.GLfloat * len(vertex_positions)),
            (gl.GLfloat * len(vertex_positions))(*vertex_positions),
            gl.GL_STATIC_DRAW,
        )
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, 0)
        gl.glEnableVertexAttribArray(0)
        # create index buffer object
        self.ibo = gl.GLuint(0)
        gl.glGenBuffers(1, self.ibo)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ibo)

        gl.glBufferData(
            gl.GL_ELEMENT_ARRAY_BUFFER,
            ctypes.sizeof(gl.GLuint * len(indices)),
            (gl.GLuint * len(indices))(*indices),
            gl.GL_STATIC_DRAW,
        )
        # create shader
        self.shader = shader.Shader("./shaders/vert.glsl", "./shaders/frag.glsl")
        self.shader_matrix_location = self.shader.find_uniform(b"matrix")
        self.shader.use()
        # create matrices
        self.mv_matrix = matrix.Matrix()
        self.p_matrix = matrix.Matrix()

        self.x = 0
        pyglet.clock.schedule_interval(self.update, 1.0 / 60)

    def update(self, dt):
        self.x += dt

    def on_draw(self):
        # create projection matrix
        self.p_matrix.load_identity()
        self.p_matrix.perspective(90, float(self.width) / float(self.height), 0.1, 500)
        # create modelview matrix
        self.mv_matrix.load_identity()
        self.mv_matrix.translate(0, 0, -1)
        self.mv_matrix.rotate_2d(self.x, math.sin(self.x / 3 * 2) / 2)
        # create modelviewprojection matrix
        mvp_matrix = self.p_matrix * self.mv_matrix
        self.shader.uniform_matrix(self.shader_matrix_location, mvp_matrix)
        # draw stuff
        gl.glClearColor(0, 0, 0, 1)
        self.clear()

        gl.glDrawElements(gl.GL_TRIANGLES, len(indices), gl.GL_UNSIGNED_INT, None)

    def on_resize(self, width, height):
        print(f"Resize {width} * {height}")
        return super().on_resize(width, height)


class Game:
    def __init__(self) -> None:
        self.config = gl.Config(major_version=3)
        self.window = Window(
            config=self.config,
            width=800,
            height=600,
            vsync=False,
            resizable=True,
            caption="MC clone",
        )

    def run(self):
        pyglet.app.run(0)


if __name__ == "__main__":
    game = Game()
    game.run()
