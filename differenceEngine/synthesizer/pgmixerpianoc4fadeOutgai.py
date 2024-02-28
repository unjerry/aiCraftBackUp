import pygame as pg
import pygame.mixer as mixer
import numpy as np

pg.init()
mixer.init()
mainScreen = pg.display.set_mode((400, 400))
mainClock = pg.time.Clock()

soundDict = {}
for i in range(-24, 24):
    soundDict[i] = mixer.Sound(f"sine{i}.wav")
s0 = mixer.Sound("sine0.wav")


S = set()
isRunning = 1
while isRunning:
    for event in pg.event.get():
        # print(event)
        if event.type == pg.QUIT:
            isRunning = 0
        if event.type == pg.KEYDOWN:
            print("down")
            # print(pg.key.name(event.key))
            if event.key == pg.K_q:
                S.add(-24)
                soundDict[-24].play()
            if event.key == pg.K_w:
                S.add(-22)
                soundDict[-22].play()
            if event.key == pg.K_e:
                S.add(-20)
                soundDict[-20].play()
            if event.key == pg.K_r:
                S.add(-19)
                soundDict[-19].play()
            if event.key == pg.K_t:
                S.add(-17)
                soundDict[-17].play()
            if event.key == pg.K_y:
                S.add(-15)
                soundDict[-15].play()
            if event.key == pg.K_u:
                S.add(-13)
                soundDict[-13].play()
            if event.key == pg.K_LSHIFT:
                S.add(-12)
                soundDict[-12].play()
            if event.key == pg.K_z:
                S.add(-10)
                soundDict[-10].play()
            if event.key == pg.K_x:
                S.add(-8)
                soundDict[-8].play()
            if event.key == pg.K_c:
                S.add(-7)
                soundDict[-7].play()
            if event.key == pg.K_v:
                S.add(-5)
                soundDict[-5].play()
            if event.key == pg.K_b:
                S.add(-3)
                soundDict[-3].play()
            if event.key == pg.K_n:
                S.add(-1)
                soundDict[-1].play()

            if event.key == pg.K_m:
                S.add(0)
                soundDict[0].play()
            if event.key == pg.K_COMMA:
                S.add(2)
                soundDict[2].play()
            if event.key == pg.K_PERIOD:
                S.add(4)
                soundDict[4].play()
            if event.key == pg.K_SLASH:
                S.add(5)
                soundDict[5].play()
            if event.key == pg.K_RSHIFT:
                S.add(7)
                soundDict[7].play()
            if event.key == pg.K_LEFT:
                S.add(9)
                soundDict[9].play()
            if event.key == pg.K_DOWN:
                S.add(11)
                soundDict[11].play()
            if event.key == pg.K_RIGHT:
                S.add(12)
                soundDict[12].play()
            if event.key == pg.K_i:
                S.add(14)
                soundDict[14].play()
            if event.key == pg.K_o:
                S.add(16)
                soundDict[16].play()
            if event.key == pg.K_p:
                S.add(17)
                soundDict[17].play()
            if event.key == pg.K_LEFTBRACKET:
                S.add(19)
                soundDict[19].play()
            if event.key == pg.K_RIGHTBRACKET:
                S.add(21)
                soundDict[21].play()
            if event.key == pg.K_BACKSLASH:
                S.add(23)
                soundDict[23].play()

        if event.type == pg.KEYUP:
            print("up")
            if event.key == pg.K_q:
                S.remove(-24)
                soundDict[-24].fadeout(100)
            if event.key == pg.K_w:
                S.remove(-22)
                soundDict[-22].fadeout(100)
            if event.key == pg.K_e:
                S.remove(-20)
                soundDict[-20].fadeout(100)
            if event.key == pg.K_r:
                S.remove(-19)
                soundDict[-19].fadeout(100)
            if event.key == pg.K_t:
                S.remove(-17)
                soundDict[-17].fadeout(100)
            if event.key == pg.K_y:
                S.remove(-15)
                soundDict[-15].fadeout(100)
            if event.key == pg.K_u:
                S.remove(-13)
                soundDict[-13].fadeout(100)
            if event.key == pg.K_LSHIFT:
                S.remove(-12)
                soundDict[-12].fadeout(100)
            if event.key == pg.K_z:
                S.remove(-10)
                soundDict[-10].fadeout(100)
            if event.key == pg.K_x:
                S.remove(-8)
                soundDict[-8].fadeout(100)
            if event.key == pg.K_c:
                S.remove(-7)
                soundDict[-7].fadeout(100)
            if event.key == pg.K_v:
                S.remove(-5)
                soundDict[-5].fadeout(100)
            if event.key == pg.K_b:
                S.remove(-3)
                soundDict[-3].fadeout(100)
            if event.key == pg.K_n:
                S.remove(-1)
                soundDict[-1].fadeout(100)

            if event.key == pg.K_m:
                S.remove(0)
                soundDict[0].fadeout(100)
            if event.key == pg.K_COMMA:
                S.remove(2)
                soundDict[2].fadeout(100)
            if event.key == pg.K_PERIOD:
                S.remove(4)
                soundDict[4].fadeout(100)
            if event.key == pg.K_SLASH:
                S.remove(5)
                soundDict[5].fadeout(100)
            if event.key == pg.K_RSHIFT:
                S.remove(7)
                soundDict[7].fadeout(100)
            if event.key == pg.K_LEFT:
                S.remove(9)
                soundDict[9].fadeout(100)
            if event.key == pg.K_DOWN:
                S.remove(11)
                soundDict[11].fadeout(100)
            if event.key == pg.K_RIGHT:
                S.remove(12)
                soundDict[12].fadeout(100)
            if event.key == pg.K_i:
                S.remove(14)
                soundDict[14].fadeout(100)
            if event.key == pg.K_o:
                S.remove(16)
                soundDict[16].fadeout(100)
            if event.key == pg.K_p:
                S.remove(17)
                soundDict[17].fadeout(100)
            if event.key == pg.K_LEFTBRACKET:
                S.remove(19)
                soundDict[19].fadeout(100)
            if event.key == pg.K_RIGHTBRACKET:
                S.remove(21)
                soundDict[21].fadeout(100)
            if event.key == pg.K_BACKSLASH:
                S.remove(23)
                soundDict[23].fadeout(100)
    print(S, len(S))
    for i in S:
        soundDict[i].set_volume(1 / np.log(len(S) + 2))
    pg.display.flip()
    mainClock.tick(240)

pg.quit()
