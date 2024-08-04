import renderEntiti
import entiti
import pyglet


class ytemListBatch(pyglet.graphics.Batch):
    def __init__(self, assets: renderEntiti.assetsManager, player: entiti.plaier):
        super().__init__()
        self.assets: renderEntiti.assetsManager = assets
        self.player: entiti.plaier = player
        self.sprite: dict[int, pyglet.sprite.Sprite] = {}


if __name__ == "__main__":
    mainAssets = renderEntiti.assetsManager(
        "mainAssets", folder="artAssets/mainAssets/"
    )
    config = pyglet.gl.Config(double_buffer=True)
    window = pyglet.window.Window(resizable=True, config=config)
    window.set_vsync(False)

    tylemap: entiti.tyleMap = entiti.tyleMap("tylemap")
    plaier = entiti.plaier("plaier")

    batchDict: dict[int, pyglet.graphics.Batch] = {}
    uiBatchDict: dict[int, pyglet.graphics.Batch] = {}
    spriteDictDict: dict[int, dict[str, pyglet.sprite.Sprite]] = {}
    weidgeBatch = pyglet.graphics.Batch()

    fpsSet: bool = True
    fpsDisplay: pyglet.window.FPSDisplay = pyglet.window.FPSDisplay(
        window=window,
        color=(255, 255, 255, 128),
    )

    anchor_p: pyglet.math.Vec2 = pyglet.math.Vec2(0, 0)
    anchor_v: pyglet.math.Vec2 = pyglet.math.Vec2(0, 0)
    anchor_v_mul = 1
    scl = 16
    keyV: int = 0

    def commandBarOnCommit(cmd: str):
        global tylemap
        global anchor_p
        print("The coammand you enter is:", cmd)
        if cmd == "quit":
            window.dispatch_event("on_close")
            tylemap.save("./mapData")
            plaier.save("./playerData")
        if cmd.startswith("sM_"):  # selectMap
            anchor_p = pyglet.math.Vec2(0, 0)
            name = cmd.split("_")[-1]
            print("NAMELOADWORLD", name)
            tylemap.name = name
            tylemap = tylemap.load("./mapData/")
            # print("GRID", tylemap.gridMap)
            spriteDictDict[0] = {}
            batchDict[0] = pyglet.graphics.Batch()
            spriteDictDict[0] = {}
            for key, itt in tylemap.gridMap.items():
                key: str
                itt: entiti.tyleBlock
                sprite = pyglet.sprite.Sprite(
                    getattr(mainAssets, itt.type),
                    group=pyglet.graphics.Group(0),
                    batch=batchDict[0],
                )
                sprite.gridLoc = (int(key.split(";")[0]), int(key.split(";")[1]))
                # sprite.visible = False
                spriteDictDict[0][key] = sprite
                # print("NINDIC",spriteDictDict[0])
            # print("DICT", batchDict, spriteDictDict)
        if cmd.startswith("cM_"):  # createMap
            name = cmd.split("_")[-1]
            print("NAMEcreateWORLD", name)
            tylemap.name = name
            tylemap.randomGeneration(10, (0, 0), 10)
            tylemap.save("./mapData/")
        if cmd.startswith("cP_"):  # createPlayer
            name = cmd.split("_")[-1]
            print("NAMEcreatePlayer", name)
            plaier.name = name
            plaier.save("./playerData/")
        if cmd.startswith("sP_"):  # selectPlayer
            name = cmd.split("_")[-1]
            print("NAMEselectPlayer", name)
            plaier.name = name
            plaier.load("./playerData/")
            batchDict[1] = pyglet.graphics.Batch()
            spriteDictDict[1] = {}
            spriteDictDict[1]["player"] = pyglet.sprite.Sprite(
                getattr(mainAssets, plaier.apperence),
                group=pyglet.graphics.Group(0),
                batch=batchDict[1],
            )
            spriteDictDict[1]["player"].gridLoc = (0, 0)
            uiBatchDict[10] = ytemListBatch(mainAssets, plaier)
        commandBar.value = ""  # clear the bar after enter

    commandBar: pyglet.gui.TextEntry = pyglet.gui.TextEntry(
        "", 0 + 5, 50 + 5, 200, batch=weidgeBatch
    )
    commandBar.set_handler("on_commit", commandBarOnCommit)
    window.push_handlers(commandBar)

    @window.event
    def on_close():
        print("PRINT_blobWindow_on_close")
        tylemap.save("./mapData/")
        plaier.save("./playerData/")

    @window.event
    def on_draw():
        pyglet.gl.glClearColor(0.35, 0.4, 0.65, 0.5)
        window.clear()
        for i in sorted(batchDict):
            batchDict[i].draw()
        for i in sorted(uiBatchDict):
            uiBatchDict[i].draw()
        weidgeBatch.draw()
        if fpsSet:
            fpsDisplay.draw()

    def buttonUpdate(dt):
        pass

    def update(dt):
        global anchor_p
        global keyV
        anchor_v.x = 0
        anchor_v.y = 0
        if (keyV & 1) != 0:
            anchor_v.x += -5
        if (keyV & 2) != 0:
            anchor_v.x += 5
        if (keyV & 4) != 0:
            anchor_v.y += -5
        if (keyV & 8) != 0:
            anchor_v.y += 5
        anchor_p += anchor_v * dt * anchor_v_mul
        if 1 in spriteDictDict:
            if "player" in spriteDictDict[1]:
                spriteDictDict[1]["player"].gridLoc = tuple(anchor_p)
        for i in sorted(spriteDictDict):
            for sprite in spriteDictDict[i].values():
                sprite: pyglet.sprite.Sprite
                dif_frac: pyglet.math.Vec2 = (
                    pyglet.math.Vec2(*sprite.gridLoc) - anchor_p
                )
                sprite.position = (
                    (dif_frac * scl)[0] + window.width / 2,
                    (dif_frac * scl)[1] + window.height / 2,
                    0,
                )
                sprite.scale = scl / 16

    @window.event
    def on_key_press(symbol, modifiers):
        global anchor_v_mul
        global keyV
        if symbol == pyglet.window.key.A:
            keyV = keyV | 1
        if symbol == pyglet.window.key.D:
            keyV = keyV | 2
        if symbol == pyglet.window.key.S:
            keyV = keyV | 4
        if symbol == pyglet.window.key.W:
            keyV = keyV | 8
        if (
            symbol == pyglet.window.key.LSHIFT
            or symbol == pyglet.window.key.RSHIFT
            or symbol == pyglet.window.key.SPACE
        ):
            anchor_v_mul *= 2
        print("ON_KEY_PRESS.window", symbol, modifiers, pyglet.window.key.A, keyV)

    @window.event
    def on_key_release(symbol, modifiers):
        global anchor_v_mul
        global keyV
        if symbol == pyglet.window.key.A:
            keyV = keyV & (15 - 1)
        if symbol == pyglet.window.key.D:
            keyV = keyV & (15 - 2)
        if symbol == pyglet.window.key.S:
            keyV = keyV & (15 - 4)
        if symbol == pyglet.window.key.W:
            keyV = keyV & (15 - 8)
        if (
            symbol == pyglet.window.key.LSHIFT
            or symbol == pyglet.window.key.RSHIFT
            or symbol == pyglet.window.key.SPACE
        ):
            anchor_v_mul /= 2
        print("ON_KEY_RELEASE.window", symbol, modifiers, pyglet.window.key.A, keyV)

    @window.event
    def on_mouse_scroll(x, y, scroll_x, scroll_y):
        print("PRINT_onMouse_scroll", x, y, scroll_x, scroll_y)
        global scl
        scl *= 1.1 ** (scroll_y)
        if scl < 8:
            scl = 8
        if scl > 100:
            scl = 100
        # if self.pldrone.drone.data["itemSelected"] < 0:
        #     self.pldrone.drone.data["itemSelected"] = 0

    pyglet.clock.schedule_interval(update, 1 / 60)
    pyglet.app.run(0)
