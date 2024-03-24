from tileMap import tileMap
from player import player
from heatViewPort import ppline
import moderngl as mgl
import numpy as np
import cv2
import pygame as pg


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
        with open(f"assets/shaders/heatSimulator0.glsl") as file:
            computeShaderSource0 = file.read()
        with open(f"assets/shaders/heatSimulator1.glsl") as file:
            computeShaderSource1 = file.read()
        self.computeShaderProgramList = [
            self.ctx.compute_shader(computeShaderSource0),
            self.ctx.compute_shader(computeShaderSource1),
        ]
        self.computeShaderProgram = self.ctx.compute_shader(computeShaderSource)
        self.FrameBuffer = [None, None]
        self.heatTexture = [self.getTexture(code=0), self.getTexture(code=1)]
        self.renderWindow = pg.Surface((50 * 16, 50 * 16))
        self.Pp = ppline(self.ctx)

    def getTexture(self, code):
        tex = self.ctx.texture(
            [
                self.size[0] * self.tileMap.tileSize,
                self.size[1] * self.tileMap.tileSize,
            ],
            1,
            dtype="f4",
        )
        tex.use(code)
        tex.bind_to_image(code, read=True, write=True)

        # raa = np.frombuffer(tex.read(), dtype=np.uint8)

        # # print(np.reshape(raa,(500,500,-1)).shape)
        # cv2.imwrite(
        #     f"./first{code}.png",
        #     np.reshape(
        #         raa,
        #         (
        #             self.size[0] * self.tileMap.tileSize,
        #             self.size[1] * self.tileMap.tileSize,
        #             -1,
        #         ),
        #     ),
        # )
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
        # print("scene update")
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
        self.computeShaderProgram["dt"] = self.game.deltaTime
        self.computeShaderProgram["conductionRate"] = 30
        # self.FrameBuffer[0] = self.ctx.framebuffer(self.heatTexture[0])
        # self.FrameBuffer[1] = self.ctx.framebuffer(self.heatTexture[1])
        # self.computeShaderProgramList[self.textureIndex].run(50, 50, 1)
        self.computeShaderProgram.run(50, 50, 1)
        temp = self.FrameBuffer[(self.textureIndex + 1) % 2].read(
            (
                0,
                0,
                self.tileMap.tileSize,
                self.tileMap.tileSize,
            ),
            components=1,
            dtype="f4",
        )
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
        self.renderWindow.fill((120, 130, 90))
        self.tileMap.render(self.renderWindow)
        self.player.render(self.renderWindow)
        surf.blit(self.renderWindow, (0, 10))
        self.Pp.render(surf)

    def load(self, n):
        self.player.load(n)
        self.tileMap.load(n)
