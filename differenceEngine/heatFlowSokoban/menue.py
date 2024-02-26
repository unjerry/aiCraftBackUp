import pygame as pg
from functools import partial


class menue:
    def __init__(self, game) -> None:
        self.game = game
        self.buttonList = [
            {
                "title": "exit",
                "font": pg.font.Font(size=20),
                "func": self.exitt,
                "pos": (0, 0),
                "size": (100, 100),
                "rect": None,
            },
            {
                "title": "level:0",
                "font": pg.font.Font(size=20),
                "func": partial(self.setNum, n=0),
                "pos": (110, 0),
                "size": (100, 100),
                "rect": None,
            },
        ]

    def exitt(self):
        self.game.isRunning = 0
        print("exitt")

    def setNum(self, n):
        print(f"{n}")
        self.game.renderType = n

    def update(self):
        for but in self.buttonList:
            # print(but["rect"])
            if but["rect"].collidepoint(pg.mouse.get_pos()):
                # print(but["func"])
                but["func"]()

    def render(self, surf):
        for but in self.buttonList:
            su = pg.Surface(but["size"])
            su.fill((255, 100, 200))
            rc = su.get_rect()
            rc.move_ip(but["pos"])
            but["rect"] = rc
            text = but["font"].render(but["title"], False, 20)
            surf.blit(su, but["pos"])
            surf.blit(text, but["pos"])
