# https://www.youtube.com/watch?v=eJDIsFJN4OQ&t=494s

import pygame as pg
import moderngl as mgl
import sys
from model import Triangle
from camera import Camera


class graphicsEngine:
    def __init__(self, win_size=(1600 / 2, 900 / 2)) -> None:
        # init pygame modules
        pg.init()
        # window size
        self.WIN_SIZE = win_size
        # set opengl attr
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 4)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 6)
        pg.display.gl_set_attribute(
            pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE
        )
        # create opengl context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        # detect and use existing opengl context
        self.ctx = mgl.create_context(require=460)
        # create an object to track time
        self.clock = pg.time.Clock()
        # camera
        self.camera = Camera(self)
        self.time = 0
        # scene
        self.scene = Triangle(self)

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                self.scene.destroy()
                pg.quit()
                sys.exit()

    def render(self):
        # clear framebuffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        # render
        self.scene.render()
        # swap buffer
        pg.display.flip()

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.render()
            self.clock.tick(60)


if __name__ == "__main__":
    app = graphicsEngine()
    app.run()