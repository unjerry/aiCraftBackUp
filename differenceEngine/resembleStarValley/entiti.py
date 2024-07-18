# basic entities in game
import pickle
import os
import random
import json

gameDir: str = "gameData/"
gameDirblob: str = "gameData/blobs/"
# 「」


def checkDir(dir: str):
    if not os.path.exists(dir):  # if there is no dir directory then create
        os.makedirs(dir)
        print(f"The directory 「{dir}」 has been created.")
    else:
        print(f"The directory 「{dir}」 already exists.")


def checkGameDir() -> None:
    checkDir(gameDir)
    checkDir(gameDirblob)


class entiti(object):
    def __init__(self, **karg) -> None:
        # iterate the args to attributes
        for k, v in karg.items():
            setattr(self, k, v)

    def __str__(self) -> str:
        # print the object id and the list of attributes
        ans = f"id={id(self)}:[\n"
        for attr in dir(self):
            if not attr.startswith("__"):
                ans += f"{attr} {getattr(self,attr)} {type(getattr(self,attr))}\n"
        ans += "]"
        return ans


class tyle(entiti):  # tile blocks
    def __init__(
        self,
        name,
        position,
        ident,
        blobResid,
        **karg,
    ) -> None:
        super().__init__(**karg)
        self.name = name
        self.position = position
        self.ident = ident
        self.changed = False
        self.age = 0
        self.blobRes: blob = blobResid

    def update(self):
        # if self.ident == "grass":
        #     rd = random.randint(0, 5)
        #     self.tiletype = f"tile00{rd}"
        if self.ident == "dirt":
            rd = random.randint(0, min(100, self.age))
            # print("PRINT_dirt2grass", rd)
            if rd > 90:
                self.ident = "grass"
                self.tiletype = f"tile002"
                self.changed = True
                self.age = 0
                self.blobRes.autoTileGen()
                self.changed = True
        if self.ident == "seed":
            if self.age < 5 and self.tiletype != "tile031":
                self.tiletype = f"tile031"
                self.changed = True
            if 5 <= self.age and self.age < 10 and self.tiletype != "tile032":
                self.tiletype = f"tile032"
                self.changed = True
            if 10 <= self.age and self.age < 30 and self.tiletype != "tile033":
                self.tiletype = f"tile033"
                self.changed = True
            if 30 <= self.age and self.age < 35 and self.tiletype != "tile034":
                self.tiletype = f"tile034"
                self.changed = True

    def onRightClick(self, drone=None):
        print("PRINT_tile_CHECKRIGHTclick")
        if (
            f"loc_({self.position[0]},{self.position[1]},{1})"
            in self.blobRes.data["tileMap"]
        ):
            if (
                self.blobRes.data["tileMap"][
                    f"loc_({self.position[0]},{self.position[1]},{1})"
                ].ident
                == "seed"
                and self.blobRes.data["tileMap"][
                    f"loc_({self.position[0]},{self.position[1]},{1})"
                ].age
                >= 30
            ):
                print("PRINT_age>30")
                self.blobRes.data["tileMap"].pop(
                    f"loc_({self.position[0]},{self.position[1]},{1})"
                )
                rd = random.randint(1, 5)
                drone.giveYtem("fastFruit", rd)
        # if self.ident == "dirt":
        #     self.map.data["tileMap"][
        #         f"loc_({self.position[0]},{self.position[1]},{1})"
        #     ] = tyle(
        #         name=f"earth_at_loc_({self.position[0]},{self.position[1]},{1})",
        #         position=(self.position[0], self.position[1], 1),
        #         ident="seed",
        #         blobResid=self.blobRes,
        #         tiletype="tile031",
        #     )
        #     self.changed = True
        # if self.ident == "grass":
        #     self.ident = "dirt"
        #     self.tiletype = "tile012"
        #     self.changed = True
        #     self.age = 0

    def onRightDrag(self, drone=None):
        if (
            f"loc_({self.position[0]},{self.position[1]},{1})"
            in self.blobRes.data["tileMap"]
        ):
            if (
                self.blobRes.data["tileMap"][
                    f"loc_({self.position[0]},{self.position[1]},{1})"
                ].ident
                == "seed"
                and self.blobRes.data["tileMap"][
                    f"loc_({self.position[0]},{self.position[1]},{1})"
                ].age
                >= 30
            ):
                print("PRINT_age>30")
                self.blobRes.data["tileMap"].pop(
                    f"loc_({self.position[0]},{self.position[1]},{1})"
                )
                rd = random.randint(1, 5)
                drone.giveYtem("fastFruit", rd)


class ytem(entiti):  # unified scattering items
    def __init__(self, ident: str, scattered, tileType: str, num: int, **karg) -> None:
        super().__init__(**karg)
        self.ident: str = ident
        self.scattered = scattered
        self.tileType: str = tileType
        self.num: int = num

    def onRightClick(self, tile: tyle):
        print("PRINT_YTEM_ONrIGHTclick")
        if (
            self.ident == "seed"
            and tile.ident == "dirt"
            and (
                f"loc_({tile.position[0]},{tile.position[1]},{1})"
                not in tile.blobRes.data["tileMap"]
            )
        ):
            print("PRINT_grassIdent")
            tile.blobRes.data["tileMap"][
                f"loc_({tile.position[0]},{tile.position[1]},{1})"
            ] = tyle(
                name=f"earth_at_loc_({tile.position[0]},{tile.position[1]},{1})",
                position=(tile.position[0], tile.position[1], 1),
                ident="seed",
                blobResid=tile.blobRes,
                tiletype="tile031",
                age=0,
            )
            self.num -= 1
        if self.ident == "dirt" and tile.ident == "grass":
            tile.ident = "dirt"
            tile.tiletype = "tile012"
            tile.age = 0
            self.num -= 1

    def onRightDrag(self, tile: tyle):
        print("PRINT_YTEM_ONrIGHTclick")
        if (
            self.ident == "seed"
            and tile.ident == "dirt"
            and (
                f"loc_({tile.position[0]},{tile.position[1]},{1})"
                not in tile.blobRes.data["tileMap"]
            )
        ):
            print("PRINT_grassIdent")
            tile.blobRes.data["tileMap"][
                f"loc_({tile.position[0]},{tile.position[1]},{1})"
            ] = tyle(
                name=f"earth_at_loc_({tile.position[0]},{tile.position[1]},{1})",
                position=(tile.position[0], tile.position[1], 1),
                ident="seed",
                blobResid=tile.blobRes,
                tiletype="tile031",
                age=0,
            )
            self.num -= 1


class ytemMap(entiti):  # the id map with the id:int and the pixture name:str
    def __init__(self, name, **karg) -> None:
        super().__init__(**karg)
        self.name: str = name
        self.data: dict[str, str] = {}
        checkGameDir()
        # read the drone data
        print(f"Loading drone:「{self.name}」.")
        # if there is no data before then report an error.
        if not os.path.exists(gameDir + self.name + ".json"):
            print(f"Data of map:{self.name} unexist.")
        # if there is data before then read.
        else:
            self.load()
        print(self)

    def load(self):
        print(f"Start loading the data of drone:「{self.name}」.")
        with open(gameDir + self.name + ".json", "rb") as file:
            self.data = json.load(file)
        print(f"Data of drone:「{self.name}」 loaded.")


class dron(entiti):  # floating drone
    def __init__(self, name: str = "defaultDron", **karg) -> None:
        super().__init__(**karg)
        self.itemChanged = False
        self.name: str = name
        self.data: dict = {
            "worldBlobName": "mainLandAnich",
            "position": (0, 0, 0),
            "itemDict": {},
            "itemSelected": 0,
            "perspectiveCumulateTime": 0,
        }
        checkGameDir()
        # read the drone data
        print(f"Loading drone:「{self.name}」.")
        # if there is no data before then create.
        if not os.path.exists(gameDir + self.name + ".pkl"):
            print(f"Data of drone:「{self.name}」 unexist.")
            print(f"Data of drone:「{self.name}」 created.")
            self.save()
        # if there is data before then read.
        else:
            self.load()
        # if self.data["arxivName"] == None:
        #     print("No previous arxiv")
        #     arxivname: str = input("Input the new arxivName:")
        #     self.data["arxivName"] = arxivname
        #     arxiv(arxivname)
        # print(self)

    def save(self):
        print(f"Start saving the data of drone:「{self.name}」.")
        with open(gameDir + self.name + ".pkl", "wb") as file:
            pickle.dump(self.data, file)
        print(f"Data of drone:「{self.name}」 saved.")

    def load(self):
        print(f"Start loading the data of drone:「{self.name}」.")
        with open(gameDir + self.name + ".pkl", "rb") as file:
            self.data = pickle.load(file)
        print(f"Data of drone:「{self.name}」 loaded.")

    def __del__(self):
        self.save()

    def giveYtem(self, ident, num: int = 1):
        for i in range(30):
            if i in self.data["itemDict"]:
                if self.data["itemDict"][i].ident == ident:
                    self.data["itemDict"][i].num += num
                    self.itemChanged = True
                    self.save()
                    return
        for i in range(30):
            if i not in self.data["itemDict"] or self.data["itemDict"] == None:
                self.data["itemDict"][i] = ytem(ident, None, "tile031", num)
                break
        # print(self.data["itemDict"])
        self.itemChanged = True
        self.save()

    def onRightClick(self, key: tyle):
        print("PRINT_drone_RIGHTclick")
        if self.data["itemSelected"] in self.data["itemDict"]:
            self.data["itemDict"][self.data["itemSelected"]].onRightClick(key)
            key.blobRes.autoTileGen()
            self.itemChanged = True
        # if self.ident == "dirt":
        #     self.map.data["tileMap"][
        #         f"loc_({self.position[0]},{self.position[1]},{1})"
        #     ] = tyle(
        #         name=f"earth_at_loc_({self.position[0]},{self.position[1]},{1})",
        #         position=(self.position[0], self.position[1], 1),
        #         ident="seed",
        #         blobResid=self,
        #         tiletype="tile031",
        #     )
        #     self.changed = True
        # if self.ident == "grass":
        #     self.ident = "dirt"
        #     self.tiletype = "tile012"
        #     self.changed = True
        #     self.age = 0

    def onRightDrag(self, key: tyle):
        print("PRINT_drone_RIGHTclick")
        if self.data["itemSelected"] in self.data["itemDict"]:
            self.data["itemDict"][self.data["itemSelected"]].onRightDrag(key)
            self.itemChanged = True


class blob(entiti):  # the space blob
    def __init__(self, name: str, size: tuple[int, int] = (20, 30), **karg) -> None:
        super().__init__(**karg)
        self.name: str = name
        self.size: tuple[int, int] = size  # the space blob-tours size
        self.data: dict[str] = {
            "tileMap": {},  # the actuall tilemap data of the 20*30
            "blobTime": 0,
        }
        # read the tileMap data
        checkGameDir()
        # load the blob
        print(f"Loading tileMap:「{self.name}」.")
        # if there is no data before then create.
        if not os.path.exists(gameDirblob + self.name + ".pkl"):
            print(f"Data of blob:「{self.name}」 unexists.")
            self.simpleGenerateWithTree()
            print(f"Data of blob:「{self.name}」 created.")
            self.save()
        # if there is data before then read.
        else:
            self.load()

    def save(self):
        print(f"Start saving the data of blob:「{self.name}」.")
        with open(gameDirblob + self.name + ".pkl", "wb") as file:
            pickle.dump(self.data, file)
        print(f"Data of blob:「{self.name}」 saved.")

    def load(self):
        print(f"Start loading the data of blob:「{self.name}」.")
        with open(gameDirblob + self.name + ".pkl", "rb") as file:
            self.data = pickle.load(file)
        print(f"Data of blob:「{self.name}」 loaded.")

    def __del__(self):
        self.save()

    def simpleGenerate(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.data["tileMap"][f"loc_({i},{j},{0})"] = tyle(
                    name=f"earth_at_loc_({i},{j},{0})",
                    position=(i, j, 0),
                    ident="grass",
                    blobResid=self,
                )
                rd = random.randint(0, 5)
                self.data["tileMap"][f"loc_({i},{j},{0})"].tiletype = f"tile00{rd}"

    def simpleGenerateWithTree(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.data["tileMap"][f"loc_({i},{j},{0})"] = tyle(
                    name=f"earth_at_loc_({i},{j},{0})",
                    position=(i, j, 0),
                    ident="grass",
                    blobResid=self,
                )
                rd = random.randint(0, 5)
                self.data["tileMap"][f"loc_({i},{j},{0})"].tiletype = f"tile00{rd}"
                if rd == 3:
                    self.data["tileMap"][f"loc_({i},{j},{2})"] = tyle(
                        name=f"earth_at_loc_({i},{j},{2})",
                        position=(i, j, 2),
                        ident="tree",
                        blobResid=self,
                    )
                    self.data["tileMap"][f"loc_({i},{j},{2})"].tiletype = f"tree{1}"

    def checkloc(self, k: str, ident: str) -> bool:
        if k in self.data["tileMap"]:
            if self.data["tileMap"][k].ident == ident:
                return True
            return False
        return False

    @staticmethod
    def caltiletype(t, tr, r, br, b, bl, l, tl: bool) -> bool:
        if not (t and l):
            tl = False
        if not (t and r):
            tr = False
        if not (b and l):
            bl = False
        if not (b and r):
            br = False

        tot: int = 0
        if t:
            tot += 1 << 0
        if tr:
            tot += 1 << 1
        if r:
            tot += 1 << 2
        if br:
            tot += 1 << 3
        if b:
            tot += 1 << 4
        if bl:
            tot += 1 << 5
        if l:
            tot += 1 << 6
        if tl:
            tot += 1 << 7
        return tot

    def autoTileGen(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.data["tileMap"][f"loc_({i},{j},{0})"].ident == "dirt":
                    rd = self.caltiletype(
                        self.checkloc(f"loc_({i},{j+1},{0})", "dirt"),
                        self.checkloc(f"loc_({i+1},{j+1},{0})", "dirt"),
                        self.checkloc(f"loc_({i+1},{j},{0})", "dirt"),
                        self.checkloc(f"loc_({i+1},{j-1},{0})", "dirt"),
                        self.checkloc(f"loc_({i},{j-1},{0})", "dirt"),
                        self.checkloc(f"loc_({i-1},{j-1},{0})", "dirt"),
                        self.checkloc(f"loc_({i-1},{j},{0})", "dirt"),
                        self.checkloc(f"loc_({i-1},{j+1},{0})", "dirt"),
                    )
                    if (
                        self.data["tileMap"][f"loc_({i},{j},{0})"].tiletype
                        != f"dirtOnGrass{rd:08b}"
                    ):
                        self.data["tileMap"][f"loc_({i},{j},{0})"].changed = True
                    self.data["tileMap"][
                        f"loc_({i},{j},{0})"
                    ].tiletype = f"dirtOnGrass{rd:08b}"
                    print("PRINT_TILEAUTO", f"dirtOnGrass{rd:08b}")

    def sync(self, time):
        while self.data["blobTime"] < time:
            self.incrementSync()

    def incrementSync(self):
        for v in self.data["tileMap"].values():
            v.age += 1
            v.update()
        self.data["blobTime"] += 1


class arxiv(entiti):
    def __init__(self, name: str = "defaultArxivName", **karg) -> None:
        super().__init__(**karg)
        self.name: str = name
        self.data: dict = {"currentBlob": "mainLandAnich", "blobs": {}, "time": 0}
        checkGameDir()
        # read the arxiv data
        print(f"Loading arxiv:「{self.name}」.")
        # if there is no data before then create.
        if not os.path.exists(gameDir + self.name + ".pkl"):
            print(f"Data of arxiv:「{self.name}」 unexists.")
            self.data["blobs"][self.data["currentBlob"]] = blob(
                name=self.data["currentBlob"]
            )
            print(f"Data of arxiv:「{self.name}」 created.")
            self.save()
        # if there is data before then read.
        else:
            self.load()
        print(self)

    def save(self):
        print(f"Start saving the data of arxiv:「{self.name}」.")
        with open(gameDir + self.name + ".pkl", "wb") as file:
            pickle.dump(self.data, file)
        print(f"Data of arxiv:「{self.name}」 saved.")

    def load(self):
        print(f"Start loading the data of arxiv:「{self.name}」.")
        with open(gameDir + self.name + ".pkl", "rb") as file:
            self.data = pickle.load(file)
        print(f"Data of arxiv:「{self.name}」 loaded.")

    def __del__(self):
        self.save()


if __name__ == "__main__":
    while True:
        cmd = input("input:")
        if cmd == "quit":
            break
        if cmd.startswith("goto_tyle"):
            lis = cmd.split("_")
            print(lis, lis[-1], [int(it) for it in lis[-1][1:-1].split(",")])
        if cmd.startswith("create_blob"):
            lis = cmd.split("_")
            print(lis, lis[-1], lis[-2], [int(it) for it in lis[-1][1:-1].split(",")])
            name = cmd.split("_")[-2]
            blobb = blob(name=name, size=[int(it) for it in lis[-1][1:-1].split(",")])
            del blobb
        if cmd.startswith("create_arxiv"):
            name = cmd.split("_")[-1]
            arxi = arxiv(name)
            del arxi
        if cmd.startswith("create_drone"):
            name = cmd.split("_")[-1]
            drone = dron(name)
            del drone
        if cmd.startswith("check_drone"):
            name = cmd.split("_")[-1]
            print(dron(name))
        if cmd.startswith("load_map"):
            name = cmd.split("_")[-1]
            itemmap = ytemMap(name)
            del itemmap
        if cmd.startswith("give_ytem"):  # give_ytem_seed_to_ddd
            name = cmd.split("_")[-1]
            ident = cmd.split("_")[-3]
            drone = dron(name)
            print(name, ident)
            drone.giveYtem(ident)
            drone.save()
            del drone
