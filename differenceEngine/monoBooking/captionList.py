import json
from orac import orac


class captionList:
    def __init__(self, world, dataSource) -> None:
        self.world = world
        with open(dataSource, "r") as file:
            self.dict = json.load(file)
        print(self.dict)
        self.list = self.dict["textList"]
        for texs in self.list:
            print(texs)
        self.cuuren = 0
        self.renderList = []

    def update(self):
        if self.cuuren < len(self.list):
            if self.list[self.cuuren]["startTime"] < (self.world.time / 1000):
                self.renderList.append(
                    (
                        self.cuuren,
                        orac(
                            self.world.window,
                            "assets/fonts/COUR.TTF",
                            25,
                            self.list[self.cuuren]["content"],
                            (0, 50 * len(self.renderList)),
                        ),
                    )
                )
                self.cuuren += 1
        for i, it in enumerate(self.renderList):
            print(i, it, self.list[it[0]]["startTime"] + self.list[it[0]]["lastTime"])
            if (self.list[it[0]]["startTime"] + self.list[it[0]]["lastTime"]) < (
                self.world.time / 1000
            ):
                self.renderList.pop(i)
        for i, it in enumerate(self.renderList):
            it[1].pos = (0, 50 * i)

    def render(self):
        for it in self.renderList:
            it[1].render()
