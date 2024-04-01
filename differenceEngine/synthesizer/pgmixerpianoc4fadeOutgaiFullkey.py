import pygame as pg
import pygame.mixer as mixer
import numpy as np

pg.init()
mixer.init()
mainScreen = pg.display.set_mode((400, 400))
mainClock = pg.time.Clock()

kk=1

soundDict = {}
for i in range(-36, 36):
    soundDict[i] = mixer.Sound(f"piano_c4/{i}.wav")
s0 = mixer.Sound("sine0.wav")

SHIFT = 12
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
            if event.key == pg.K_TAB:
                S.add(-27 + SHIFT)
                soundDict[-27 + SHIFT].play()
            if event.key == pg.K_q:
                S.add(-25 + SHIFT)
                soundDict[-25 + SHIFT].play()
            if event.key == pg.K_w:
                S.add(-24 + SHIFT)
                soundDict[-24 + SHIFT].play()
            if event.key == pg.K_e:
                S.add(-22 + SHIFT)
                soundDict[-22 + SHIFT].play()
            if event.key == pg.K_r:
                S.add(-20 + SHIFT)
                soundDict[-20 + SHIFT].play()
            if event.key == pg.K_t:
                S.add(-19 + SHIFT)
                soundDict[-19 + SHIFT].play()
            if event.key == pg.K_y:
                S.add(-17 + SHIFT)
                soundDict[-17 + SHIFT].play()
            if event.key == pg.K_u:
                S.add(-15 + SHIFT)
                soundDict[-15 + SHIFT].play()
            if event.key == pg.K_i:
                S.add(-13 + SHIFT)
                soundDict[-13 + SHIFT].play()
            if event.key == pg.K_o:
                S.add(-12 + SHIFT)
                soundDict[-12 + SHIFT].play()
            if event.key == pg.K_p:
                S.add(-10 + SHIFT)
                soundDict[-10 + SHIFT].play()
            if event.key == pg.K_LEFTBRACKET:
                S.add(-8 + SHIFT)
                soundDict[-8 + SHIFT].play()
            if event.key == pg.K_RIGHTBRACKET:
                S.add(-7 + SHIFT)
                soundDict[-7 + SHIFT].play()
            if event.key == pg.K_BACKSLASH:
                S.add(-5 + SHIFT)
                soundDict[-5 + SHIFT].play()
            
            if event.key == pg.K_DELETE:
                S.add(-3 + SHIFT)
                soundDict[-3 + SHIFT].play()
            if event.key == pg.K_END:
                S.add(-1 + SHIFT)
                soundDict[-1 + SHIFT].play()
            if event.key == pg.K_PAGEDOWN:
                S.add(0 + SHIFT)
                soundDict[0 + SHIFT].play()
            if event.key == pg.K_KP_7:
                S.add(2 + SHIFT)
                soundDict[2 + SHIFT].play()
            if event.key == pg.K_KP_8:
                S.add(4 + SHIFT)
                soundDict[4 + SHIFT].play()
            if event.key == pg.K_KP_9:
                S.add(5 + SHIFT)
                soundDict[5 + SHIFT].play()
            if event.key == pg.K_KP_PLUS:
                S.add(7 + SHIFT)
                soundDict[7 + SHIFT].play()

            if event.key == pg.K_LSHIFT:
                S.add(-12 + SHIFT)
                soundDict[-12 + SHIFT].play()
            if event.key == pg.K_z:
                S.add(-10 + SHIFT)
                soundDict[-10 + SHIFT].play()
            if event.key == pg.K_x:
                S.add(-8 + SHIFT)
                soundDict[-8 + SHIFT].play()
            if event.key == pg.K_c:
                S.add(-7 + SHIFT)
                soundDict[-7 + SHIFT].play()
            if event.key == pg.K_v:
                S.add(-5 + SHIFT)
                soundDict[-5 + SHIFT].play()
            if event.key == pg.K_b:
                S.add(-3 + SHIFT)
                soundDict[-3 + SHIFT].play()
            if event.key == pg.K_n:
                S.add(-1 + SHIFT)
                soundDict[-1 + SHIFT].play()

            if event.key == pg.K_m:
                S.add(0 + SHIFT)
                soundDict[0 + SHIFT].play()
            if event.key == pg.K_COMMA:
                S.add(2 + SHIFT)
                soundDict[2 + SHIFT].play()
            if event.key == pg.K_PERIOD:
                S.add(4 + SHIFT)
                soundDict[4 + SHIFT].play()
            if event.key == pg.K_SLASH:
                S.add(5 + SHIFT)
                soundDict[5 + SHIFT].play()



            if event.key == pg.K_RSHIFT:
                S.add(7 + SHIFT)
                soundDict[7 + SHIFT].play()
            if event.key == pg.K_LEFT:
                S.add(9 + SHIFT)
                soundDict[9 + SHIFT].play()
            if event.key == pg.K_DOWN:
                S.add(11 + SHIFT)
                soundDict[11 + SHIFT].play()
            if event.key == pg.K_RIGHT:
                S.add(12 + SHIFT)
                soundDict[12 + SHIFT].play()
            # if event.key == pg.K_i:
            #     S.add(14)
            #     soundDict[14+SHIFT].play()
            # if event.key == pg.K_o:
            #     S.add(16)
            #     soundDict[16+SHIFT].play()
            # if event.key == pg.K_p:
            #     S.add(17)
            #     soundDict[17+SHIFT].play()
            # if event.key == pg.K_LEFTBRACKET:
            #     S.add(19)
            #     soundDict[19+SHIFT].play()
            # if event.key == pg.K_RIGHTBRACKET:
            #     S.add(21)
            #     soundDict[21+SHIFT].play()
            # if event.key == pg.K_BACKSLASH:
            #     S.add(23)
            #     soundDict[23+SHIFT].play()

        if event.type == pg.KEYUP:
            print("up")
            if event.key == pg.K_TAB:
                S.remove(-27 + SHIFT)
                soundDict[-27 + SHIFT].fadeout(100)
            if event.key == pg.K_q:
                S.remove(-25 + SHIFT)
                soundDict[-25 + SHIFT].fadeout(100)
            if event.key == pg.K_w:
                S.remove(-24 + SHIFT)
                soundDict[-24 + SHIFT].fadeout(100)
            if event.key == pg.K_e:
                S.remove(-22 + SHIFT)
                soundDict[-22 + SHIFT].fadeout(100)
            if event.key == pg.K_r:
                S.remove(-20 + SHIFT)
                soundDict[-20 + SHIFT].fadeout(100)
            if event.key == pg.K_t:
                S.remove(-19 + SHIFT)
                soundDict[-19 + SHIFT].fadeout(100)
            if event.key == pg.K_y:
                S.remove(-17 + SHIFT)
                soundDict[-17 + SHIFT].fadeout(100)
            if event.key == pg.K_u:
                S.remove(-15 + SHIFT)
                soundDict[-15 + SHIFT].fadeout(100)
            if event.key == pg.K_i:
                S.remove(-13 + SHIFT)
                soundDict[-13 + SHIFT].fadeout(100)
            if event.key == pg.K_o:
                S.remove(-12 + SHIFT)
                soundDict[-12 + SHIFT].fadeout(100)
            if event.key == pg.K_p:
                S.remove(-10 + SHIFT)
                soundDict[-10 + SHIFT].fadeout(100)
            if event.key == pg.K_LEFTBRACKET:
                S.remove(-8 + SHIFT)
                soundDict[-8 + SHIFT].fadeout(100)
            if event.key == pg.K_RIGHTBRACKET:
                S.remove(-7 + SHIFT)
                soundDict[-7 + SHIFT].fadeout(100)
            if event.key == pg.K_BACKSLASH:
                S.remove(-5 + SHIFT)
                soundDict[-5 + SHIFT].fadeout(100)


            if event.key == pg.K_DELETE:
                S.remove(-3 + SHIFT)
                soundDict[-3 + SHIFT].fadeout(100)
            if event.key == pg.K_END:
                S.remove(-1 + SHIFT)
                soundDict[-1 + SHIFT].fadeout(100)
            if event.key == pg.K_PAGEDOWN:
                S.remove(0 + SHIFT)
                soundDict[0 + SHIFT].fadeout(100)
            if event.key == pg.K_KP_7:
                S.remove(2 + SHIFT)
                soundDict[2 + SHIFT].fadeout(100)
            if event.key == pg.K_KP_8:
                S.remove(4 + SHIFT)
                soundDict[4 + SHIFT].fadeout(100)
            if event.key == pg.K_KP_9:
                S.remove(5 + SHIFT)
                soundDict[5 + SHIFT].fadeout(100)
            if event.key == pg.K_KP_PLUS:
                S.remove(7 + SHIFT)
                soundDict[7 + SHIFT].fadeout(100)


            if event.key == pg.K_LSHIFT:
                S.remove(-12 + SHIFT)
                soundDict[-12 + SHIFT].fadeout(100)
            if event.key == pg.K_z:
                S.remove(-10 + SHIFT)
                soundDict[-10 + SHIFT].fadeout(100)
            if event.key == pg.K_x:
                S.remove(-8 + SHIFT)
                soundDict[-8 + SHIFT].fadeout(100)
            if event.key == pg.K_c:
                S.remove(-7 + SHIFT)
                soundDict[-7 + SHIFT].fadeout(100)
            if event.key == pg.K_v:
                S.remove(-5 + SHIFT)
                soundDict[-5 + SHIFT].fadeout(100)
            if event.key == pg.K_b:
                S.remove(-3 + SHIFT)
                soundDict[-3 + SHIFT].fadeout(100)
            if event.key == pg.K_n:
                S.remove(-1 + SHIFT)
                soundDict[-1 + SHIFT].fadeout(100)

            if event.key == pg.K_m:
                S.remove(0 + SHIFT)
                soundDict[0 + SHIFT].fadeout(100)
            if event.key == pg.K_COMMA:
                S.remove(2 + SHIFT)
                soundDict[2 + SHIFT].fadeout(100)
            if event.key == pg.K_PERIOD:
                S.remove(4 + SHIFT)
                soundDict[4 + SHIFT].fadeout(100)
            if event.key == pg.K_SLASH:
                S.remove(5 + SHIFT)
                soundDict[5 + SHIFT].fadeout(100)
            if event.key == pg.K_RSHIFT:
                S.remove(7 + SHIFT)
                soundDict[7 + SHIFT].fadeout(100)
            if event.key == pg.K_LEFT:
                S.remove(9 + SHIFT)
                soundDict[9 + SHIFT].fadeout(100)
            if event.key == pg.K_DOWN:
                S.remove(11 + SHIFT)
                soundDict[11 + SHIFT].fadeout(100)
            if event.key == pg.K_RIGHT:
                S.remove(12 + SHIFT)
                soundDict[12 + SHIFT].fadeout(100)
            # if event.key == pg.K_i:
            #     S.remove(14)
            #     soundDict[14+SHIFT].fadeout(100)
            # if event.key == pg.K_o:
            #     S.remove(16)
            #     soundDict[16+SHIFT].fadeout(100)
            # if event.key == pg.K_p:
            #     S.remove(17)
            #     soundDict[17+SHIFT].fadeout(100)
            # if event.key == pg.K_LEFTBRACKET:
            #     S.remove(19)
            #     soundDict[19+SHIFT].fadeout(100)
            # if event.key == pg.K_RIGHTBRACKET:
            #     S.remove(21)
            #     soundDict[21+SHIFT].fadeout(100)
            # if event.key == pg.K_BACKSLASH:
            #     S.remove(23)
            #     soundDict[23+SHIFT].fadeout(100)
    print(S, len(S))
    for i in S:
        soundDict[i].set_volume(kk / np.log(len(S) + 2))
    pg.display.flip()
    mainClock.tick(240)

pg.quit()
