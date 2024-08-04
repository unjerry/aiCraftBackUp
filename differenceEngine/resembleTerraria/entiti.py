import pickle
import os
import array
import random


class entiti(object):
    def __init__(self, name: str, **karg) -> None:
        # iterate the args to attributes
        self.name: str = name
        for k, v in karg.items():
            setattr(self, k, v)

    def __str__(self) -> str:
        # print the object id and the list of attributes
        ans = f"id={id(self)}:[\n"
        for attr in dir(self):
            if not (
                attr.startswith("__")
                or type(getattr(self, attr)) == type(self.__init__)
                or type(getattr(self, attr)) == type(self.checkDir)
            ):
                ans += f"{attr} {getattr(self,attr)} {type(getattr(self,attr))}\n"
        ans += "]"
        return ans

    @staticmethod
    def checkDir(dir: str):
        if not os.path.exists(dir):  # if there is no dir directory then create
            os.makedirs(dir)
            print(f"The directory 「{dir}」 has been created.")
        else:
            print(f"The directory 「{dir}」 already exists.")

    def save(self, dir: str):
        self.checkDir(dir)
        print(f"Start saving the data of {type(self)}:「{self.name}」.")
        with open(dir + self.name + ".pkl", "wb") as file:
            pickle.dump(self, file)
        print(f"Data of {type(self)}:「{self.name}」 saved.")

    def load(self, dir: str):
        print(f"Start loading the data of {type(self)}:「{self.name}」.")
        with open(dir + self.name + ".pkl", "rb") as file:
            rt: entiti = pickle.load(file)
        print(f"Data of {type(self)}:「{self.name}」 loaded.")
        return rt


class plaier(entiti):
    def __init__(self, name: str, **karg) -> None:
        super().__init__(name, **karg)
        self.apperence = "triDroneFast.gif"
        self.itemDict = {0: {"ident": "grass.png", "num": 4}}

    def giveYtem(self, ident, num: int = 1):
        for i in range(30):
            if i in self.itemDict:
                if self.itemDict[i]["ident"] == ident:
                    self.itemDict[i]["num"] += num
                    self.save()
                    return
        for i in range(30):
            if i not in self.itemDict or self.itemDict == None:
                self.itemDict[i] = {"ident": ident, "num": num}
                break
        # print(self.itemDict)


class vecti(entiti):
    def __init__(self, name: str, **karg) -> None:
        super().__init__(name, **karg)
        self.vec: array = array.array("d", [1.1, 2.2, 3.3])
        print("PRINT_ARRAYLength", len(self.vec))


class tyleMap(entiti):
    def __init__(self, name: str, **karg) -> None:
        super().__init__(name, **karg)
        self.gridMap = {}
        self.width = 100
        self.height = 100
        # self.randomGeneration(10, (0, 0), 20)

    def randomGeneration(self, num: int):
        for _ in range(num):
            x, y = (0, 0)
            while f"{x};{y}" in self.gridMap:
                x, y = (
                    random.randint(0, self.width - 1),
                    random.randint(0, self.height - 1),
                )
            self.gridMap[f"{x};{y}"] = tyleBlock(
                f"block_{x};{y}", "dirtOnGrass00000000.png", "air"
            )
        for i in range(0, self.width):
            for j in range(0, self.height):
                if f"{i};{j}" not in self.gridMap:
                    self.gridMap[f"{i};{j}"] = tyleBlock(
                        f"block_{i};{j}",
                        "grass.png",
                        None,
                    )


class tyleBlock(entiti):
    def __init__(self, name: str, type: str, possess: str, **karg) -> None:
        super().__init__(name, **karg)
        self.type: str = type
        self.possess: str = possess


if __name__ == "__main__":
    a = entiti("a")
    print(a)
    a.save("./hhh/")
    a.load("./hhh/")
    v = vecti("v")
    print(v)
    v.save("./")
    mp = tyleMap("tylemap")
    # mp.randomGeneration(10, (0, 0), 10)
    mp.name = "hxt"
    # mp.save("./testMap/")
    # print(mp)
    mp = mp.load("./testMap/")
    print(mp)
    # mp.name = "hxx"
    # mp.load("./mapData/")
    # print(mp)
