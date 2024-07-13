# main game start programm file
import pyglet.event
import renderStuff
import pyglet

if __name__ == "__main__":
    renderStuff.PlayerDroneRender("mainPlayerDrone")
    # # @firstBlob.event
    # # def on_key_press(symbol, modifiers):
    # #     if symbol == pyglet.window.key.D:
    # #         # print("sldkfj")
    # #         mainPlayerDrone.x += 1.0

    pyglet.app.run(0)
