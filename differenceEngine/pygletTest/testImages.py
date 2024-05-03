import pyglet
from pyglet.window import key
from pyglet.window import mouse

music = pyglet.resource.media(
    "artAssets/HOYO-MiX《Da Capo》[FLAC-MP3-320K] - 音乐磁场.mp3"
)
music.play()
imagex = pyglet.image.load("artAssets/Designer.png")
imagey = pyglet.image.load("artAssets/Designer2.png")

batchh=pyglet.graphics.Batch()
window = pyglet.window.Window(caption="sdfsdf")
image = pyglet.image.load("artAssets/Designer3.png")
sprite = pyglet.sprite.Sprite(img=image)
sprite.width = window.size[0]
sprite.height = window.size[1]
sprite.opacity = 0.3 * 255
bt=pyglet.gui.PushButton(10,100,pressed=imagex,depressed=imagey,batch=batchh)
window.push_handlers(bt)
@bt.event
def on_press():
    print("sdfsdfddddddddddddd")

event_logger = pyglet.window.event.WindowEventLogger()
# window.push_handlers(event_logger)
# event_logger = pyglet.sprite.event.SpriteEventLogger()
# sprite.push_handlers(event_logger)


@sprite.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        print("sdfsfsdfsdfsdf", x, y)


# @window.event
# def on_mouse_press(x, y, button, modifiers):
#     if button == mouse.LEFT:
#         print("The left mouse button was pressed.", x, y)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.A:
        print('The "A" key was pressed.')
    elif symbol == key.LEFT:
        print("The left arrow key was pressed.")
    elif symbol == key.ENTER:
        print("The enter key was pressed.")


@window.event
def on_draw():
    window.clear()
    batchh.draw()
    

def update(dt):
    pass
pyglet.clock.schedule_interval(update, 1 / 60.0)
pyglet.app.run()
