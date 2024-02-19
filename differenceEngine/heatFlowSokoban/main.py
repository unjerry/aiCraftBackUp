import pygame as pg
from utilities import loadImages
from scene import scene
import glcontext


class mainGame:
    def __init__(self, windowSize=[1600 / 1.5, 900 / 1.5]) -> None:
        pg.init()
        self.windowSize = windowSize
        self.mainScreen = pg.display.set_mode(self.windowSize)
        pg.display.set_icon(pg.image.load("./assets/images/icon.png").convert_alpha())
        self.mainClock = pg.time.Clock()
        self.isRunning = 1
        self.assets = {
            "player": loadImages("player"),
            "grass": loadImages("grass"),
            "box": loadImages("box"),
            "base": loadImages("base"),
            "heatBox": loadImages("heatBox"),
        }
        self.scene = scene(self)

    def checkEvents(self):
        for event in pg.event.get():
            # print(event)
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                self.isRunning = 0
            self.scene.checkEvents(event)
            if self.scene.isPass:
                print("scene passed")

    def render(self):
        self.mainScreen.fill(color=(0, 0, 0))
        self.scene.render(self.mainScreen)
        pg.display.set_caption(f"fps:{self.mainClock.get_fps():.0f}")
        pg.display.flip()

    def update(self):
        # self.scene.update()
        pass

    def run(self):
        while self.isRunning:
            self.checkEvents()
            self.update()
            self.render()
            self.mainClock.tick()
        pg.quit()


if __name__ == "__main__":
    mainApp = mainGame()
    mainApp.run()
