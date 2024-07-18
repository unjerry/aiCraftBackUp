import pickle
import os
import array


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
            self: entiti = pickle.load(file)
        print(f"Data of {type(self)}:「{self.name}」 loaded.")


class vecti(entiti):
    def __init__(self, name: str, **karg) -> None:
        super().__init__(name, **karg)
        self.vec: array = array.array("d", [1.1, 2.2, 3.3])
        print("PRINT_ARRAYLength", len(self.vec))


if __name__ == "__main__":
    a = entiti("a")
    print(a)
    a.save("./hhh/")
    a.load("./hhh/")
    v = vecti("v")
    print(v)
    v.save("./")
