# main game start programm file
import pyglet.event
import renderStuff
import pyglet
from entiti import ytem

if __name__ == "__main__":
    droneName: str = "ddd"
    # input(
    #     "input the character name to chose chara:"
    # )  # chose the drone to use
    renderStuff.PlayerDroneRender(droneName)  # start the rundering
    pyglet.app.run(0)
