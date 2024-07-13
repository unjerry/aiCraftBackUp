# basic entities in game
import pickle
import os
import random

gameDir: str = "gameData/"


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
    def __init__(self, **karg) -> None:
        super().__init__(**karg)


class dron(entiti):  # floating drone
    def __init__(self, name: str = "defaultDron", **karg) -> None:
        super().__init__(**karg)
        self.name: str = name
        # self.bagPack
        self.data: dict = {
            "worldBlobName": "mainLandAnich",
            "position": (0, 0, 0),
            "time": 0,
        }
        # read the drone data
        if not os.path.exists(gameDir):  # if there is no gameDir directory then create
            os.makedirs(gameDir)
            print(f"The directory {gameDir} has been created.")
        else:
            print(f"The directory {gameDir} already exists.")
            print(f"Loading drone.")
            if not os.path.exists(
                gameDir + self.name + ".pkl"
            ):  # if there is no data before then create.
                print(f"no data of drone name:{self.name}.")
                with open(gameDir + self.name + ".pkl", "wb") as file:
                    pickle.dump(self.data, file)
                print(f"data of blob name:{self.name} created.")
            else:  # if there is data before then read.
                with open(gameDir + self.name + ".pkl", "rb") as file:
                    self.data = pickle.load(file)
                print("game data loaded.")
        print(self.data)

    def save(self):
        with open(gameDir + self.name + ".pkl", "wb") as file:
            pickle.dump(self.data, file)
        print(f"data of drone name:{self.name} saved.")


class blob(entiti):  # the space blob
    def __init__(
        self, name: str = "defaultBlob", size: tuple[int, int] = (20, 30), **karg
    ) -> None:
        super().__init__(**karg)
        self.name: str = name
        self.size: tuple[int, int] = size  # the space blob-tours size
        self.data: dict[str] = {
            "tileMap": {},
            "gameTime": 0,
        }  # the actuall tilemap data of the 20*30
        # read the tileMap data
        if not os.path.exists(gameDir):  # if there is no gameDir directory then create
            os.makedirs(gameDir)
            print(f"The directory {gameDir} has been created.")
        else:
            print(f"The directory {gameDir} already exists.")
            print(f"Loading tileMap.")
            if not os.path.exists(
                gameDir + self.name + ".pkl"
            ):  # if there is no data before then create.
                print(f"no data of blob name:{self.name}.")
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
                with open(gameDir + self.name + ".pkl", "wb") as file:
                    pickle.dump(self.data, file)
                print(f"data of blob name:{self.name} created.")
            else:  # if there is data before then read.
                with open(gameDir + self.name + ".pkl", "rb") as file:
                    self.data = pickle.load(file)
                print("game data loaded.")

    def save(self):
        print(self.data["gameTime"])
        with open(gameDir + self.name + ".pkl", "wb") as file:
            pickle.dump(self.data, file)
        print(f"data of blob name:{self.name} saved.")


class arxiv(entiti):
    def __init__(self, name: str = "defaultArxivName", **karg) -> None:
        super().__init__(**karg)
        self.name: str = name
        self.data: dict = {"blobs": {}, "time": 0}
        # read the arxiv data
        if not os.path.exists(gameDir):  # if there is no gameDir directory then create
            os.makedirs(gameDir)
            print(f"The directory {gameDir} has been created.")
        else:
            print(f"The directory {gameDir} already exists.")
            print(f"Loading arxiv.")
            if not os.path.exists(
                gameDir + self.name + ".pkl"
            ):  # if there is no data before then create.
                print(f"no data of arxiv:「{self.name}」.")
                self.data["blobs"]["mainLandAnich"]=blob()
                with open(gameDir + self.name + ".pkl", "wb") as file:
                    pickle.dump(self.data, file)
                print(f"data of arxiv:「{self.name}」 created.")
            else:  # if there is data before then read.
                with open(gameDir + self.name + ".pkl", "rb") as file:
                    self.data = pickle.load(file)
                print("arxiv:「{self.name}」 data loaded.")

    def save(self):
        print(f"start saving the data of arxiv:{self.name}")
        with open(gameDir + self.name + ".pkl", "wb") as file:
            pickle.dump(self.data, file)
        print(f"data of arxiv:{self.name} saved.")


if __name__ == "__main__":
    # new_eni = entiti(name="sdlkfj")
    # new_til = tyle(name="earth", position=(10, 2), status="rest")
    # til_list = {}
    # for i in range(10):
    #     for j in range(20):
    #         til_list[f"({i},{j})"] = tyle(
    #             name="earth", position=(i, j), status="rest", possess="air"
    #         )
    # print(type(new_eni))
    # print(new_eni)
    # print(type(new_til))
    # print(new_til)
    # print(type(til_list))
    # print(til_list)
    # player_drone = dron(name="player", position=(10, 2))
    # setattr(player_drone, "position", (3, 2))
    # print(player_drone.position)
    while True:
        cmd = input("input:")
        if cmd == "quit":
            break
        if cmd.startswith("goto_tyle"):
            lis = cmd.split("_")
            print(lis, lis[-1], [int(it) for it in lis[-1][1:-1].split(",")])
        if cmd.startswith("create_blob"):
            name = cmd.split("_")[-1]
            newBlob = blob(name=name, size=(10, 20))
            print(name, newBlob)
