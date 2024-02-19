import pygame as pg
import numpy as np
import cv2


class player:
    def __init__(self, game, scene, tileMap, initialLocation=(15, 7)) -> None:
        self.location = initialLocation
        self.tileMap = tileMap
        self.game = game
        self.scene = scene

    def handelMove(self, delta):
        currentPos = self.location
        nextPos = (currentPos[0] + delta[0], currentPos[1] + delta[1])
        nextPosKey = self.tileMap.posToKey(nextPos)
        if not nextPosKey in self.tileMap.tileMap:
            self.location = nextPos
        else:
            if (
                self.tileMap.tileMap[nextPosKey]["type"] == "box"
                or self.tileMap.tileMap[nextPosKey]["type"] == "heatBox"
            ):
                nextNextPos = (nextPos[0] + delta[0], nextPos[1] + delta[1])
                nextNextPosKey = self.tileMap.posToKey(nextNextPos)
                if not nextNextPosKey in self.tileMap.tileMap:
                    self.location = nextPos
                    self.tileMap.tileMap[nextNextPosKey] = self.tileMap.tileMap[
                        nextPosKey
                    ]
                    # print(self.tileMap.tileMap[nextPosKey])
                    if "heatType" in self.tileMap.tileMap[nextPosKey]:
                        # print("sdfsd")
                        self.scene.heatTexture.write(
                            # np.reshape(
                            0 * np.ones(16 * 16, dtype=np.float32),  # (1, 1, -1)
                            # ),
                            (
                                nextPos[0] * self.tileMap.tileSize,
                                nextPos[1] * self.tileMap.tileSize,
                                self.tileMap.tileSize,
                                self.tileMap.tileSize,
                            ),
                        )
                        self.scene.heatTexture.write(
                            # np.reshape(
                            273.5 * np.ones(16 * 16, dtype=np.float32),  # (1, 1, -1)
                            # ),
                            (
                                nextNextPos[0] * self.tileMap.tileSize,
                                nextNextPos[1] * self.tileMap.tileSize,
                                self.tileMap.tileSize,
                                self.tileMap.tileSize,
                            ),
                        )
                        raa = np.frombuffer(
                            self.scene.heatTexture.read(), dtype=np.uint8
                        )
                        raa = np.reshape(
                            raa,
                            (
                                self.scene.size[0] * self.tileMap.tileSize,
                                self.scene.size[0] * self.tileMap.tileSize,
                                4,
                            ),
                        )
                        # print(
                        #     raa[
                        #         nextNextPos[1]
                        #         * self.tileMap.tileSize : nextNextPos[1]
                        #         * self.tileMap.tileSize
                        #         + self.tileMap.tileSize,
                        #         nextNextPos[0]
                        #         * self.tileMap.tileSize : nextNextPos[0]
                        #         * self.tileMap.tileSize
                        #         + self.tileMap.tileSize,
                        #         :,
                        #     ]
                        # )
                        # print(nextNextPos[0], nextNextPos[1])
                        cv2.imwrite(
                            f"./first.png",
                            np.reshape(
                                raa,
                                (
                                    self.scene.size[0] * self.tileMap.tileSize,
                                    self.scene.size[1] * self.tileMap.tileSize,
                                    -1,
                                ),
                            ),
                        )

                    self.tileMap.tileMap.pop(nextPosKey)
                    self.tileMap.tileMap[nextNextPosKey]["pos"] = nextNextPos

    def checkEvents(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT or event.key == pg.K_a:
                self.handelMove(delta=(-1, 0))
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                self.handelMove(delta=(+1, 0))
            if event.key == pg.K_UP or event.key == pg.K_w:
                self.handelMove(delta=(0, -1))
            if event.key == pg.K_DOWN or event.key == pg.K_s:
                self.handelMove(delta=(0, +1))

    def render(self, surf):
        self.tileMap.putSqare(self.game.assets["player"][0], self.location, surf)
