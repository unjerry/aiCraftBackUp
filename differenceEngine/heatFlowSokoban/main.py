import pygame as pg
from utilities import loadImages
from scene import scene
from menue import menue
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
        self.renderType = -1
        self.menue = menue(self)
        self.deltaTime = 0

    def checkEvents(self):
        for event in pg.event.get():
            # print(event)
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                self.isRunning = 0
            if event.type == pg.MOUSEBUTTONDOWN:
                self.menue.update()
            self.scene.checkEvents(event)
            if self.scene.isPass:
                print("scene passed")
                self.renderType = -1
                self.scene.isPass = 0

    def render(self):
        self.mainScreen.fill(color=(100, 120, 132))
        if self.renderType == 0:
            self.scene.render(self.mainScreen)
        if self.renderType == -1:
            self.menue.render(self.mainScreen)
        if self.renderType == 3:
            ff = pg.Surface((100, 100))
            ff.fill((100, 1, 1))
            self.mainScreen.blit(ff, (0, 0))
        pg.display.set_caption(f"fps:{self.mainClock.get_fps():.0f}")
        pg.display.flip()

    def update(self):
        self.checkEvents()
        self.scene.update()
        self.scene.textureIndex = (self.scene.textureIndex + 1) % 2
        pass

    def run(self):
        while self.isRunning:
            self.update()
            self.render()
            self.deltaTime = self.mainClock.tick() / 1000
            print(self.deltaTime)
        pg.quit()


if __name__ == "__main__":
    mainApp = mainGame()
    mainApp.run()
