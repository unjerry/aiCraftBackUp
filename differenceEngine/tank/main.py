import pyglet
import numpy as np


class phyBall(pyglet.shapes.Circle):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.v = np.array([10, 10],dtype=np.float64)
        self.p = np.array([self.x, self.y],dtype=np.float64)

    def update(self, dt):
        print(self.x, self.y, self.p, self.v)
        self.p += self.v * dt
        self.x = self.p[0]
        self.y = self.p[1]


class wind(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pyglet.clock.schedule_interval(self.update, 1 / 1000)

    def on_draw(self):
        window.clear()
        label.draw()
        circ.draw()
        fps_display.draw()

    def update(self, dt):
        circ.update(dt)


window = wind(caption="HelloWorld")
fps_display = pyglet.window.FPSDisplay(window=window)

label = pyglet.text.Label(
    "Hello, world",
    font_name="Times New Roman",
    font_size=36,
    x=window.width // 2,
    y=window.height // 2,
    anchor_x="center",
    anchor_y="center",
)

circ = phyBall(100, 200, 10)

pyglet.app.run(0)
