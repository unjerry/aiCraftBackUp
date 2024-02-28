import pygame as pg


pg.init()

mainScreen = pg.display.set_mode((400, 400))
mainClock = pg.time.Clock()


S = set()
isRunning = 1
while isRunning:
    print("start")
    for event in pg.event.get():
        print(event, event.type)
        if event.type == pg.QUIT:
            isRunning = 0
            pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_h:
                S.add(0)
    for i in S:
        print(i)
    pg.display.set_caption(f"fps:{mainClock.get_fps():.0f}")
    pg.display.flip()
    mainClock.tick(1)
