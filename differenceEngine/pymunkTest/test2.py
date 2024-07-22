import pyglet
import pymunk
import time
from pymunk.pyglet_util import DrawOptions

m_length = 16
window = pyglet.window.Window(1280, 720, "pymunkTest")
options = DrawOptions()

space = pymunk.Space()
space.gravity = (0, -9.8 * m_length)

body = pymunk.Body(1, 1666)
body.position = (10 * m_length, 10 * m_length)
poly = pymunk.Poly.create_box(body, size=(50, 50))

space.add(body, poly)


@window.event
def on_draw():
    window.clear()
    space.debug_draw(options)


def update(dt):
    space.step(1 / 60)


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / 60)
    pyglet.app.run()
