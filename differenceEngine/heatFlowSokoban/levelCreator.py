import json

n = 3
tileMap = {}

for i in range(4):
    tileMap[f"{2+i}_0"] = {
        "type": "grass",
        "variant": 0,
        "pos": (2 + i, 0),
    }
for i in range(4):
    tileMap[f"4_{2+i}"] = {
        "type": "grass",
        "variant": 0,
        "pos": (4, 2 + i),
    }
for i in range(3):
    tileMap[f"1_{1+i}"] = {
        "type": "grass",
        "variant": 0,
        "pos": (1, 1 + i),
    }
for i in range(3):
    tileMap[f"6_{0+i}"] = {
        "type": "grass",
        "variant": 0,
        "pos": (6, 0 + i),
    }
for i in range(3):
    tileMap[f"{2+i}_6"] = {
        "type": "grass",
        "variant": 0,
        "pos": (2 + i, 6),
    }
for i in range(2):
    tileMap[f"0_{4+i}"] = {
        "type": "grass",
        "variant": 0,
        "pos": (0, 4 + i),
    }
for i in range(2):
    tileMap[f"1_{5+i}"] = {
        "type": "grass",
        "variant": 0,
        "pos": (1, 5 + i),
    }
tileMap[f"5_2"] = {
    "type": "grass",
    "variant": 0,
    "pos": (5, 2),
}
tileMap[f"2_3"] = {
    "type": "grass",
    "variant": 0,
    "pos": (2, 3),
}
tileMap[f"2_4"] = {
    "type": "box",
    "variant": 0,
    "pos": (2, 4),
}
#     tileMap[f"10_{i+5}"] = {
#         "type": "grass",
#         "variant": 0,
#         "pos": (10, i + 5),
#     }
# tileMap["15_5"] = {
#     "type": "box",
#     "variant": 0,
#     "pos": (15, 5),
# }
# tileMap["15_6"] = {
#     "type": "heatBox",
#     "variant": 0,
#     "pos": (15, 6),
#     "heatType": True,
# }
# tileMap["15_7"] = {
#     "type": "heatBox",
#     "variant": 0,
#     "pos": (15, 7),
#     "heatType": True,
# }
# self.checkPoint["2_5"] = {
#     "type": "base",
#     "variant": 0,
#     "pos": (2, 5),
# }
# tileMap["playerInitialLocation"] = (2, 2)
# print(self.baseTile, self.checkPoint, tileMap, sep="\n")
with open(f"assets/levelsInfo/level{n}.json", "w") as file:
    json.dump(tileMap, file)


player = {"pos": (1, 4)}
with open(f"assets/levelsInfo/player{n}.json", "w") as file:
    json.dump(player, file)

checkPoint = {
    "5_1": {
        "type": "base",
        "variant": 0,
        "pos": (5, 1),
    }
}
with open(f"assets/levelsInfo/checkPoint{n}.json", "w") as file:
    json.dump(checkPoint, file)
