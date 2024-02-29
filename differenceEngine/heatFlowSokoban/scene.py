from tileMap import tileMap
from player import player
import moderngl as mgl
import numpy as np
import cv2


class scene:

    def __init__(self, game, size=[50, 50]) -> None:
        self.textureIndex = 0
        self.game = game
        self.size = size
        self.tileMap = tileMap(self.game)
        self.player = player(self.game, self, self.tileMap)
        self.isPass = False
        # self.update()
        self.ctx = mgl.create_context(standalone=True, require=460)
        with open(f"assets/shaders/heatSimulator.glsl") as file:
            computeShaderSource = file.read()
        self.computeShaderProgram = self.ctx.compute_shader(computeShaderSource)
        self.FrameBuffer = [None, None]
        self.heatTexture = [self.getTexture(code=0), self.getTexture(code=1)]

    def getTexture(self, code):
        tex = self.ctx.texture(
            [
                self.size[0] * self.tileMap.tileSize,
                self.size[1] * self.tileMap.tileSize,
            ],
            1,
            dtype="f4",
        )
        # tex.use(code)
        tex.bind_to_image(code, read=True, write=True)

        raa = np.frombuffer(tex.read(), dtype=np.uint8)

        # print(np.reshape(raa,(500,500,-1)).shape)
        cv2.imwrite(
            f"./first{code}.png",
            np.reshape(
                raa,
                (
                    self.size[0] * self.tileMap.tileSize,
                    self.size[1] * self.tileMap.tileSize,
                    -1,
                ),
            ),
        )
        self.FrameBuffer[code] = self.ctx.framebuffer(tex)
        return tex

    def checkPass(self):
        self.isPass = True
        for location in self.tileMap.checkPoint:
            tile = self.tileMap.checkPoint[location]
            if tile["type"] == "base":
                if not (location in self.tileMap.tileMap):
                    self.isPass = False
                elif not (self.tileMap.tileMap[location]["type"] == "box"):
                    self.isPass = False

    def checkEvents(self, event):
        self.player.checkEvents(event)
        self.checkPass()

    def update(self):
        print("scene update")
        self.heatTexture[0].bind_to_image(
            (self.textureIndex + 0) % 2,
            read=(self.textureIndex + 1) % 2,
            write=(self.textureIndex + 0) % 2,
        )
        self.heatTexture[1].bind_to_image(
            (self.textureIndex + 1) % 2,
            read=(self.textureIndex + 0) % 2,
            write=(self.textureIndex + 1) % 2,
        )
        self.computeShaderProgram.run(50, 50, 1)
        # raa = np.frombuffer(
        #     self.heatTexture[0].read(),
        #     dtype=np.uint8,
        # )
        # raa = np.reshape(
        #     raa,
        #     (
        #         self.size[0] * self.tileMap.tileSize,
        #         self.size[0] * self.tileMap.tileSize,
        #         4,
        #     ),
        # )
        # cv2.imwrite(
        #     f"./first.png",
        #     np.reshape(
        #         raa,
        #         (
        #             self.size[0] * self.tileMap.tileSize,
        #             self.size[1] * self.tileMap.tileSize,
        #             -1,
        #         ),
        #     ),
        # )

        # for location in self.tileMap.tileMap:
        #     tile = self.tileMap.tileMap[location]
        #     if "heatType" in tile:
        #         self.heatTexture[0].write(
        #             np.reshape(255 * np.ones(16 * 16 * 4, dtype=np.uint8), (1, 1, -1)),
        #             (
        #                 tile["pos"][0] * self.tileMap.tileSize,
        #                 tile["pos"][1] * self.tileMap.tileSize,
        #                 self.tileMap.tileSize,
        #                 self.tileMap.tileSize,
        #             ),
        #         )
        # raa = np.frombuffer(self.heatTexture[0].read(), dtype=np.uint8)

        # # print(np.reshape(raa,(500,500,-1)).shape)
        # cv2.imwrite(
        #     f"./first.png",
        #     np.reshape(
        #         raa,
        #         (
        #             self.size[0] * self.tileMap.tileSize,
        #             self.size[1] * self.tileMap.tileSize,
        #             -1,
        #         ),
        #     ),
        # )

    def render(self, surf):
        self.tileMap.render(surf)
        self.player.render(surf)

    def load(self, n):
        self.player.load(n)
        self.tileMap.load(n)
