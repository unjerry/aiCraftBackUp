import renderEntiti
import entiti
import pyglet
import math


class ytemListBatch(pyglet.graphics.Batch):
    def __init__(self, assets: renderEntiti.assetsManager, player: entiti.plaier):
        super().__init__()
        self.assets: renderEntiti.assetsManager = assets
        self.pos: pyglet.math.Vec2 = pyglet.math.Vec2(0, 0)
        self.player: entiti.plaier = player
        self.sprite: dict[int, pyglet.sprite.Sprite] = {}
        self.lables = {}
        self.skale: float = 1
        for k, v in self.player.itemDict.items():
            k: int
            v: dict[str, str]
            self.sprite[k] = pyglet.sprite.Sprite(
                getattr(mainAssets, v["ident"]),
                k * self.skale * 16,
                0,
                batch=self,
                group=pyglet.graphics.Group(0),
            )
            self.lables[k] = pyglet.text.Label(
                f"{v['num']}",
                font_name="courier new",
                font_size=3,
                x=30 + k * self.skale * 16,
                y=10,
                z=12,
                anchor_x="center",
                anchor_y="center",
                batch=self,
                group=pyglet.graphics.Group(1),
            )

    def update(self, dt):
        for k, sp in self.sprite.items():
            sp.scale = self.skale
            sp.position = tuple(
                pyglet.math.Vec3(
                    self.pos.x + k * self.skale * 16,
                    self.pos.y + 0,
                    0,
                )
            )
        for k, sp in self.lables.items():
            sp: pyglet.text.Label
            sp.font_size = 3 * self.skale
            sp.position = tuple(
                pyglet.math.Vec3(
                    self.pos.x + (k + 0.9) * self.skale * 16,
                    self.pos.y + 10,
                    12,
                )
            )


if __name__ == "__main__":
    mainAssets = renderEntiti.assetsManager(
        "mainAssets", folder="artAssets/mainAssets/"
    )
    config = pyglet.gl.Config(double_buffer=True)
    window = pyglet.window.Window(resizable=True, config=config)
    window.set_vsync(False)

    tylemap: entiti.tyleMap = entiti.tyleMap("tylemap")
    plaier = entiti.plaier("plaier")

    batchDict: dict[int, pyglet.graphics.Batch] = {0: pyglet.graphics.Batch()}
    uiBatchDict: dict[int, pyglet.graphics.Batch] = {}
    spriteDictDict: dict[int, dict[str, pyglet.sprite.Sprite]] = {0: {}}
    weidgeBatch = pyglet.graphics.Batch()

    fpsSet: bool = True
    fpsDisplay: pyglet.window.FPSDisplay = pyglet.window.FPSDisplay(
        window=window,
        color=(255, 255, 255, 128),
    )

    anchor_p: pyglet.math.Vec2 = pyglet.math.Vec2(0, 0)
    anchor_v: pyglet.math.Vec2 = pyglet.math.Vec2(0, 0)
    anchor_v_mul = 1
    scl = 16 * 1
    keyV: int = 0
    PressCtrl: bool = False

    def commandBarOnCommit(cmd: str):
        global tylemap
        global anchor_p
        print("The coammand you enter is:", cmd)
        if cmd == "quit":
            window.dispatch_event("on_close")
            tylemap.save("./mapData/")
            plaier.save("./playerData/")
        if cmd.startswith("sM_"):  # selectMap
            anchor_p = pyglet.math.Vec2(0, 0)
            name = cmd.split("_")[-1]
            print("NAMELOADWORLD", name)
            tylemap.name = name
            tylemap = tylemap.load("./mapData/")
            # print("GRID", tylemap.gridMap)
            spriteDictDict[0] = {}
            batchDict[0] = pyglet.graphics.Batch()
            loc = (
                math.floor(anchor_p.x),
                math.floor(anchor_p.y),
            )
            N = math.ceil(window.height / 2 / scl)
            M = math.ceil(window.width / 2 / scl)
            for i in range(-N, N + 1):
                for j in range(-M, M + 1):
                    key: str = (
                        f"{((loc[0])+j)%(tylemap.width)};{((loc[1])+i)%(tylemap.height)}"
                    )
                    # print("KEY", key, (loc[0] + j, loc[1] + i))
                    if key in tylemap.gridMap:
                        itt: entiti.tyleBlock = tylemap.gridMap[key]
                        sprite = pyglet.sprite.Sprite(
                            getattr(mainAssets, itt.type),
                            group=pyglet.graphics.Group(0),
                            batch=batchDict[0],
                        )
                        sprite.gridLoc = (loc[0] + j, loc[1] + i)
                        spriteDictDict[0][f"{loc[0]+j};{loc[1]+i}"] = sprite
                        dif_frac: pyglet.math.Vec2 = (
                            pyglet.math.Vec2(*sprite.gridLoc) - anchor_p
                        )
                        sprite.position = (
                            (dif_frac * scl)[0] + window.width / 2,
                            (dif_frac * scl)[1] + window.height / 2,
                            0,
                        )
                        sprite.scale = scl / 16
            # for key, itt in tylemap.gridMap.items():
            #     key: str
            #     itt: entiti.tyleBlock
            #     sprite = pyglet.sprite.Sprite(
            #         getattr(mainAssets, itt.type),
            #         group=pyglet.graphics.Group(0),
            #         batch=batchDict[0],
            #     )
            #     sprite.gridLoc = (int(key.split(";")[0]), int(key.split(";")[1]))
            #     # sprite.visible = False
            #     spriteDictDict[0][key] = sprite
            #     # print("NINDIC",spriteDictDict[0])
            # # print("DICT", batchDict, spriteDictDict)
        if cmd.startswith("cM_"):  # createMap
            name = cmd.split("_")[-1]
            print("NAMEcreateWORLD", name)
            tylemap.name = name
            tylemap.randomGeneration(10)
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
            uiBatchDict[10].skale = 4
            uiBatchDict[10].pos = pyglet.math.Vec2(210, 10)
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
        print("sfdsf", len(spriteDictDict[0]), anchor_p)

    @window.event
    def on_key_press(symbol, modifiers):
        global anchor_v_mul
        global keyV, PressCtrl
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
        if symbol == pyglet.window.key.LCTRL:
            # print("CONTROKey")
            PressCtrl = True
        print("ON_KEY_PRESS.window", symbol, modifiers, pyglet.window.key.A, keyV)

    @window.event
    def on_key_release(symbol, modifiers):
        global anchor_v_mul
        global keyV, PressCtrl
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
        if symbol == pyglet.window.key.LCTRL:
            # print("CONTROKey")
            PressCtrl = False
        print("ON_KEY_RELEASE.window", symbol, modifiers, pyglet.window.key.A, keyV)

    @window.event
    def on_mouse_scroll(x, y, scroll_x, scroll_y):
        print("PRINT_onMouse_scroll", x, y, scroll_x, scroll_y)
        global scl
        if PressCtrl:
            scl *= 1.1 ** (scroll_y)
        if scl < 32:
            scl = 32
        if scl > 64:
            scl = 64
        # if self.pldrone.drone.data["itemSelected"] < 0:
        #     self.pldrone.drone.data["itemSelected"] = 0

    def recycle(dt):
        spriteDictDict[0].clear()
        loc = (
            math.floor(anchor_p.x),
            math.floor(anchor_p.y),
        )
        N = math.ceil(window.height / 2 / scl)
        M = math.ceil(window.width / 2 / scl)
        for i in range(-N, N + 1):
            for j in range(-M, M + 1):
                key: str = (
                    f"{((loc[0])+j)%(tylemap.width)};{((loc[1])+i)%(tylemap.height)}"
                )
                # print("KEY", key, (loc[0] + j, loc[1] + i))
                if key in tylemap.gridMap:
                    itt: entiti.tyleBlock = tylemap.gridMap[key]
                    sprite = pyglet.sprite.Sprite(
                        getattr(mainAssets, itt.type),
                        group=pyglet.graphics.Group(0),
                        batch=batchDict[0],
                    )
                    sprite.gridLoc = (loc[0] + j, loc[1] + i)
                    spriteDictDict[0][f"{loc[0]+j};{loc[1]+i}"] = sprite
                    dif_frac: pyglet.math.Vec2 = (
                        pyglet.math.Vec2(*sprite.gridLoc) - anchor_p
                    )
                    sprite.position = (
                        (dif_frac * scl)[0] + window.width / 2,
                        (dif_frac * scl)[1] + window.height / 2,
                        0,
                    )
                    sprite.scale = scl / 16

    # pyglet.clock.schedule_interval(recycle, 2)
    pyglet.clock.schedule_interval(update, 1 / 60)
    pyglet.app.run(0)
