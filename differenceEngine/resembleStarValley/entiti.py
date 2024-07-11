# basic entities in game
import pickle
import os

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
    def __init__(self, **karg) -> None:
        super().__init__(**karg)


class blob(entiti):  # the space blob
    def __init__(
        self, name: str = "defaultBlob", size: tuple[int, int] = (20, 30), **karg
    ) -> None:
        super().__init__(**karg)
        self.name: str = name
        self.size: tuple[int, int] = size  # the space blob-tours size
        self.tileMap: dict[str, tyle] = {}  # the actuall tilemap data of the 20*30
        # create the game storage folder
        if not os.path.exists(gameDir):
            os.makedirs(gameDir)
            print(f"The directory {gameDir} has been created.")
        else:
            print(f"The directory {gameDir} already exists.")
            print(f"Loading tileMap.")
            if not os.path.exists(gameDir + self.name + ".pkl"):
                # wirte into pkl file
                with open(gameDir + self.name + ".pkl", "wb") as file:
                    pickle.dump(self.tileMap, file)
                print("game data created.")
            else:
                # read pkl
                with open(gameDir + self.name + ".pkl", "rb") as file:
                    self.tileMap = pickle.load(file)
                print("game data loaded.")


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
            print(name)
