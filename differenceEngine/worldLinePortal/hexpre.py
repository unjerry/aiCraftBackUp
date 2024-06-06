import pyglet
import numpy as np


class Hexagon(pyglet.shapes.Polygon):
    def __init__(self, x, y, radius=100, batch=None, group=None):
        self.radius = radius
        self.coordinates = [
            (
                x + self.radius * np.cos(0 * np.pi / 3),
                y + self.radius * np.sin(0 * np.pi / 3),
            ),
            (
                x + self.radius * np.cos(1 * np.pi / 3),
                y + self.radius * np.sin(1 * np.pi / 3),
            ),
            (
                x + self.radius * np.cos(2 * np.pi / 3),
                y + self.radius * np.sin(2 * np.pi / 3),
            ),
            (
                x + self.radius * np.cos(3 * np.pi / 3),
                y + self.radius * np.sin(3 * np.pi / 3),
            ),
            (
                x + self.radius * np.cos(4 * np.pi / 3),
                y + self.radius * np.sin(4 * np.pi / 3),
            ),
            (
                x + self.radius * np.cos(5 * np.pi / 3),
                y + self.radius * np.sin(5 * np.pi / 3),
            ),
        ]
        self.hexColor = (
            int(np.random.uniform(0.5, 1) * 255),
            int(np.random.uniform(0.5, 1) * 255),
            int(np.random.uniform(0.5, 1) * 255),
            int(np.random.uniform(0.5, 1) * 255),
        )
        super().__init__(
            *self.coordinates, color=self.hexColor, batch=batch, group=group
        )


class MenuWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.matHexCoord: pyglet.math.Mat3 = pyglet.math.Mat3(
            [
                3.0 / 2.0,
                np.sqrt(3.0) / 2.0,
                0.0,
                0.0,
                np.sqrt(3.0),
                0.0,
                0.0,
                0.0,
                1.0,
            ]
        )
        self.batch: pyglet.graphics.Batch = pyglet.graphics.Batch()
        self.fpsDisplay: pyglet.window.FPSDisplay = pyglet.window.FPSDisplay(
            window=self
        )
        self.position: dict[str, pyglet.math.Vec3] = {}
        self.renderList: dict[str, Hexagon] = {}
        self.stepLength: float = 5.0
        self.anchor: pyglet.math.Vec3 = pyglet.math.Vec3(10, 15, 0)
        self.anchorVelocity: pyglet.math.Vec3 = pyglet.math.Vec3(0, 0, 0)
        for i in range(20):
            for j in range(20):
                self.position[f"({i},{j})"] = (
                    self.matHexCoord @ (pyglet.math.Vec3(i, j, 0))
                ) * self.stepLength + self.anchor
                if (
                    self.position[f"({i},{j})"].x < 0
                    or self.position[f"({i},{j})"].x > self.width
                ):
                    continue
                if (
                    self.position[f"({i},{j})"].y < 0
                    or self.position[f"({i},{j})"].y > self.height
                ):
                    continue
                self.renderList[f"({i},{j})"] = Hexagon(
                    self.position[f"({i},{j})"].x,
                    self.position[f"({i},{j})"].y,
                    radius=self.stepLength,
                    batch=self.batch,
                )
        print(len(self.renderList))
        pyglet.clock.schedule_interval(self.update, 1 / 200)

    def update(self, dt):
        self.anchor += self.anchorVelocity
        # print(self.anchor)
        for i in range(20):
            for j in range(20):
                # pass
                self.renderList[f"({i},{j})"].x += self.anchorVelocity.x * dt
                self.renderList[f"({i},{j})"].y += self.anchorVelocity.y * dt
        # print(len(self.renderList))

    def on_draw(self) -> None:
        self.clear()
        self.batch.draw()
        self.fpsDisplay.draw()

    def on_key_press(self, symbol, modifiers):
        print(symbol, modifiers, pyglet.window.key.A)
        if symbol == pyglet.window.key.A:
            self.anchorVelocity.x = 100
        if symbol == pyglet.window.key.D:
            self.anchorVelocity.x = -100
        if symbol == pyglet.window.key.S:
            self.anchorVelocity.y = 100
        if symbol == pyglet.window.key.W:
            self.anchorVelocity.y = -100
        print(self.anchorVelocity)
        return super().on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        print(symbol, modifiers, pyglet.window.key.A)
        if symbol == pyglet.window.key.A:
            self.anchorVelocity.x = 0
        if symbol == pyglet.window.key.D:
            self.anchorVelocity.x = 0
        if symbol == pyglet.window.key.S:
            self.anchorVelocity.y = 0
        if symbol == pyglet.window.key.W:
            self.anchorVelocity.y = 0
        print(self.anchorVelocity)


# menuWindow: pyglet.window.Window = pyglet.window.Window(caption="worldLinePortal")
# menuWindow.set_location(x=100, y=100)
# fpsDisplay: pyglet.window.FPSDisplay = pyglet.window.FPSDisplay(window=menuWindow)
# menuWindowBatch: pyglet.graphics.Batch = pyglet.graphics.Batch()
# rectangle: pyglet.shapes.Rectangle = pyglet.shapes.Rectangle(
#     x=400, y=400, width=100, height=50, batch=menuWindowBatch
# )
# polygon: pyglet.shapes.Polygon = pyglet.shapes.Polygon(
#     *[(0, 0), (100, 100), (100, 200)], batch=menuWindowBatch
# )


# @menuWindow.event
# def on_draw():
#     menuWindow.clear()
#     menuWindowBatch.draw()
#     fpsDisplay.draw()
if __name__ == "__main__":
    menuWindow = MenuWindow(caption="Test")
    pyglet.app.run(0)
