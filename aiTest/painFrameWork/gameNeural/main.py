# tech from the project .\gameDemo
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import sys
import pygame as pg


class monoBooking:
    def __init__(self, win_size=(1600 / 1.5, 900 / 1.5)) -> None:
        # init pygame modules
        pg.init()
        # make SDL window
        self.window = pg.display.set_mode(win_size, pg.RESIZABLE)
        # set icon
        pg.display.set_icon(pg.image.load("icon.png").convert())
        # create an object to track time
        self.clock = pg.time.Clock()
        self.time = 0
        self.dtime = 0

    def get_time(self):
        self.time = pg.time.get_ticks()
        self.dtime = self.clock.get_time()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                pg.quit()
                sys.exit()

    def render(self):
        # clear framebuffer
        self.window.fill(color=(0.08 * 255, 0.16 * 255, 255 * 0.18))
        pg.display.flip()

    def run(self):
        while True:
            self.get_time()
            self.timeString = f"fps:{self.clock.get_fps():3.0f}|dt:{self.dtime:2d}ms|tottime:{self.time/1000:.0f}s"
            pg.display.set_caption(self.timeString)
            self.check_events()
            self.render()
            self.clock.tick(120)


if __name__ == "__main__":
    app = monoBooking()
    app.run()
