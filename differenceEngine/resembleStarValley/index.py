# main game start programm file
import pyglet.event
import renderStuff
import pyglet

if __name__ == "__main__":
    droneName: str = input("chose chara:")  # chose the drone to use
    renderStuff.PlayerDroneRender(droneName)  # start the rundering
    pyglet.app.run(0)
