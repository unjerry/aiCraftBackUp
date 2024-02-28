import json


class tileMap:
    def __init__(self, game, tileSize=16) -> None:
        self.tileSize = tileSize
        self.tileMap = {}
        self.baseTile = {}
        self.checkPoint = {}
        self.heatObject = {}
        self.game = game
        for i in range(10):
            self.tileMap[f"{3+i}_10"] = {
                "type": "grass",
                "variant": 0,
                "pos": (3 + i, 10),
            }
            self.tileMap[f"10_{i+5}"] = {
                "type": "grass",
                "variant": 0,
                "pos": (10, i + 5),
            }
        self.tileMap["15_5"] = {
            "type": "box",
            "variant": 0,
            "pos": (15, 5),
        }
        self.tileMap["15_6"] = {
            "type": "heatBox",
            "variant": 0,
            "pos": (15, 6),
            "heatType": True,
        }
        self.tileMap["15_7"] = {
            "type": "heatBox",
            "variant": 0,
            "pos": (15, 7),
            "heatType": True,
        }
        self.checkPoint["2_5"] = {
            "type": "base",
            "variant": 0,
            "pos": (2, 5),
        }
        # self.tileMap["playerInitialLocation"] = (2, 2)
        # print(self.baseTile, self.checkPoint, self.tileMap, sep="\n")
        # with open("level0.json", "w") as file:
        #     json.dump(self.tileMap, file)

    def putSqare(self, sqare, location, surf):
        surf.blit(
            sqare,
            (location[0] * self.tileSize, location[1] * self.tileSize),
        )

    @staticmethod
    def posToKey(pos):
        # print(f"{pos[0]}_{pos[1]}")
        return f"{pos[0]}_{pos[1]}"

    def render(self, surf):
        for location in self.baseTile:
            tile = self.baseTile[location]
            self.putSqare(
                self.game.assets[tile["type"]][tile["variant"]], tile["pos"], surf
            )
        for location in self.checkPoint:
            tile = self.checkPoint[location]
            self.putSqare(
                self.game.assets[tile["type"]][tile["variant"]], tile["pos"], surf
            )
        for location in self.tileMap:
            tile = self.tileMap[location]
            self.putSqare(
                self.game.assets[tile["type"]][tile["variant"]], tile["pos"], surf
            )

    def load(self, n):
        with open(f"assets/levelsInfo/level{n}.json", "r") as file:
            dcc = json.load(file)
        # print(dcc)
        del self.tileMap
        self.tileMap = dcc
        with open(f"assets/levelsInfo/checkPoint{n}.json", "r") as file:
            dcl = json.load(file)
        del self.checkPoint
        self.checkPoint = dcl
