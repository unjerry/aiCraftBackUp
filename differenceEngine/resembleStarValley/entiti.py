# basic entities in game
import pickle
import os
import random
import json

gameDir: str = "gameData/"
gameDirblob: str = "gameData/blobs/"


def checkDir(dir: str):
    if not os.path.exists(dir):  # if there is no dir directory then create
        os.makedirs(dir)
        print(f"The directory {dir} has been created.")
    else:
        print(f"The directory {dir} already exists.")


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
    def __init__(self, **karg) -> None:
        super().__init__(**karg)


class ytem(entiti):  # unified scattering items
    def __init__(self, ident: int, **karg) -> None:
        super().__init__(**karg)
        self.ident: str = ident


class ytemMap(entiti):  # the id map with the id:int and the pixture name:str
    def __init__(self, name, **karg) -> None:
        super().__init__(**karg)
        self.name: str = name
        self.data: dict[str, str] = {}
        checkGameDir()
        # read the drone data
        print(f"Loading drone:{self.name}.")
        # if there is no data before then report an error.
        if not os.path.exists(gameDir + self.name + ".json"):
            print(f"Data of map:{self.name} unexist.")
        # if there is data before then read.
        else:
            self.load()
        print(self)

    def load(self):
        print(f"start loading the data of drone:「{self.name}」.")
        with open(gameDir + self.name + ".json", "rb") as file:
            self.data = json.load(file)
        print(f"Data of drone:「{self.name}」 loaded.")


class dron(entiti):  # floating drone
    def __init__(self, name: str = "defaultDron", **karg) -> None:
        super().__init__(**karg)
        self.name: str = name
        self.data: dict = {
            "worldBlobName": "mainLandAnich",
            "position": (0, 0, 0),
            "itemDict": {},
            "perspectiveCumulateTime": 0,
        }
        checkGameDir()
        # read the drone data
        print(f"Loading drone:{self.name}.")
        # if there is no data before then create.
        if not os.path.exists(gameDir + self.name + ".pkl"):
            print(f"Data of drone:{self.name} unexist.")
            print(f"Data of drone:{self.name} created.")
            self.save()
        # if there is data before then read.
        else:
            self.load()
        # if self.data["arxivName"] == None:
        #     print("No previous arxiv")
        #     arxivname: str = input("Input the new arxivName:")
        #     self.data["arxivName"] = arxivname
        #     arxiv(arxivname)
        print(self)

    def save(self):
        print(f"start saving the data of drone:「{self.name}」.")
        with open(gameDir + self.name + ".pkl", "wb") as file:
            pickle.dump(self.data, file)
        print(f"Data of drone:「{self.name}」 saved.")

    def load(self):
        print(f"start loading the data of drone:「{self.name}」.")
        with open(gameDir + self.name + ".pkl", "rb") as file:
            self.data = pickle.load(file)
        print(f"Data of drone:「{self.name}」 loaded.")

    def __del__(self):
        self.save()


class blob(entiti):  # the space blob
    def __init__(
        self, name: str = "defaultBlob", size: tuple[int, int] = (20, 30), **karg
    ) -> None:
        super().__init__(**karg)
        self.name: str = name
        self.size: tuple[int, int] = size  # the space blob-tours size
        self.data: dict[str] = {
            "tileMap": {},  # the actuall tilemap data of the 20*30
            "blobTime": 0,
        }
        # read the tileMap data
        checkGameDir()
        print(f"Loading tileMap.")
        # if there is no data before then create.
        if not os.path.exists(gameDirblob + self.name + ".pkl"):
            print(f"Data of blob:{self.name} unexists.")
            self.simpleGenerate()
            print(f"Data of blob:{self.name} created.")
            self.save()
        # if there is data before then read.
        else:
            self.load()

    def save(self):
        print(f"start saving the data of blob:「{self.name}」.")
        with open(gameDirblob + self.name + ".pkl", "wb") as file:
            pickle.dump(self.data, file)
        print(f"Data of blob:「{self.name}」 saved.")

    def load(self):
        print(f"start loading the data of blob:「{self.name}」.")
        with open(gameDirblob + self.name + ".pkl", "rb") as file:
            self.data = pickle.load(file)
        print(f"Data of blob:「{self.name}」 loaded.")

    def __del__(self):
        self.save()

    def simpleGenerate(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.data["tileMap"][f"loc_({i},{j})"] = tyle(
                    name=f"earth_at_loc_({i},{j})",
                    position=(i, j, 0),
                    status="rest",
                    possess="air",
                    tiletype="tile000",
                )
                rd = random.randint(0, 5)
                # if rd == 0:
                self.data["tileMap"][f"loc_({i},{j})"].tiletype = f"tile00{rd}"


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
        print(f"start saving the data of arxiv:「{self.name}」.")
        with open(gameDir + self.name + ".pkl", "wb") as file:
            pickle.dump(self.data, file)
        print(f"Data of arxiv:「{self.name}」 saved.")

    def load(self):
        print(f"start loading the data of arxiv:「{self.name}」.")
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
            blob(name=name, size=[int(it) for it in lis[-1][1:-1].split(",")])
        if cmd.startswith("create_arxiv"):
            name = cmd.split("_")[-1]
            arxiv(name)
        if cmd.startswith("create_drone"):
            name = cmd.split("_")[-1]
            dron(name)
        if cmd.startswith("load_map"):
            name = cmd.split("_")[-1]
            ytemMap(name)
