import pygame as pg
import moderngl as mgl
import numpy as np
import cv2


class ppline:
    def __init__(
        self, ctx, windowSize=(50 * 16, 50 * 16), windowClearColor=(12, 40, 100)
    ) -> None:
        self.ctx = ctx
        self.FIGURE = windowSize
        self.BACKGROUNDCOLOR = windowClearColor

        # numpyArrayOfTheTexture = np.frombuffer(
        #     cv2.imread("./first.png", cv2.IMREAD_UNCHANGED), dtype=np.float32
        # )
        # inField = self.ctx.texture(self.FIGURE, 1, dtype="f4")
        # inField.write(numpyArrayOfTheTexture)
        # inField.use(0)

        self.quadData = np.array(
            [
                [-1.0, -1.0, 0.0, 0.0],
                [1.0, -1.0, 1.0, 0.0],
                [-1.0, 1.0, 0.0, 1.0],
                [1.0, 1.0, 1.0, 1.0],
            ],
            dtype="f",
        )
        self.quadBuffer = self.ctx.buffer(data=self.quadData)
        self.fbo = self.ctx.framebuffer(self.ctx.texture(self.FIGURE, 4))
        self.fbo.use()
        with open(f"assets/shaders/quadFrag.glsl") as file:
            quadFragSource = file.read()
        with open(f"assets/shaders/quadVert.glsl") as file:
            quadVertSource = file.read()
        self.shaderProgram = self.ctx.program(
            vertex_shader=quadVertSource, fragment_shader=quadFragSource
        )
        self.vao = self.ctx.vertex_array(
            self.shaderProgram, [(self.quadBuffer, "2f 2f", "vert", "uvs")]
        )
        self.shaderProgram["tex"] = 0

    def render(self, surf):
        # self.fbo.clear(0.5, 0.6, 0.3, 1.0)
        self.vao.render(mgl.TRIANGLE_STRIP)
        # rri = np.frombuffer(self.fbo.read(components=4, dtype="f1"), dtype=np.uint8)
        # cv2.imwrite("./firstvp.png", np.reshape(rri, (50 * 16, 50 * 16, -1)))
        IMG = pg.image.frombuffer(self.fbo.read(components=4), self.fbo.size, "BGRA")
        surf.blit(IMG, (600, 0))


if __name__ == "__main__":
    Pp = ppline("ll")
    Pp.render()
