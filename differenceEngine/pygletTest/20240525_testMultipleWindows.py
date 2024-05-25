import pyglet
margin=10
# 创建第一个窗口
window1 = pyglet.window.Window(width=400, height=300, caption="Window 1")

# 创建第二个窗口
window2 = pyglet.window.Window(width=400, height=300, caption="Window 2")

window1.switch_to()
batch = pyglet.graphics.Batch()
pressed_img = pyglet.resource.image("artAssets/greenPress.png")
depressed_img = pyglet.resource.image("artAssets/greenRelease.png")
pressed_img.height = 40
pressed_img.width = 40
depressed_img.height = 40
depressed_img.width = 40
# print(pressed_img.height)
pushbutton = pyglet.gui.PushButton(
    x=100 + margin,
    y=0 + margin,
    pressed=pressed_img,
    depressed=depressed_img,
    batch=batch,
)
window1.push_handlers(pushbutton)

# 定义窗口1的事件处理
@window1.event
def on_draw():
    window1.clear()
    # pyglet.graphics.draw(
    #     4, pyglet.gl.GL_QUADS, ("v2i", [0, 0, 100, 0, 100, 100, 0, 100])
    # )g
    batch.draw()


# 定义窗口2的事件处理
@window2.event
def on_draw():
    window2.clear()
    # pyglet.graphics.draw(
    #     4, pyglet.gl.GL_QUADS, ("v2i", [100, 100, 200, 100, 200, 200, 100, 200])
    # )


# 启动事件循环
pyglet.app.run()
