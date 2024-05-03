import pygame as pg
import pygame.mixer as mixer
import numpy as np

pg.init()
mixer.init()
mainScreen = pg.display.set_mode((400, 400))
mainClock = pg.time.Clock()

kk = 1
ss="saw"
soundDict = {}
yanyin=100
for i in range(-36, 36):
    soundDict[i] = mixer.Sound(ss+f"{i}.wav")
s0 = mixer.Sound("sine0.wav")

SHIFT =12
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
                S.add(-36 + SHIFT)
                soundDict[-36 + SHIFT].play()
            if event.key == pg.K_1:
                S.add(-35 + SHIFT)
                soundDict[-35 + SHIFT].play()
            if event.key == pg.K_q:
                S.add(-34 + SHIFT)
                soundDict[-34 + SHIFT].play()
            if event.key == pg.K_2:
                S.add(-33 + SHIFT)
                soundDict[-33 + SHIFT].play()
            if event.key == pg.K_w:
                S.add(-32 + SHIFT)
                soundDict[-32 + SHIFT].play()
            if event.key == pg.K_e:
                S.add(-31 + SHIFT)
                soundDict[-31 + SHIFT].play()
            if event.key == pg.K_4:
                S.add(-30 + SHIFT)
                soundDict[-30 + SHIFT].play()
            if event.key == pg.K_r:
                S.add(-29 + SHIFT)
                soundDict[-29 + SHIFT].play()
            if event.key == pg.K_5:
                S.add(-28 + SHIFT)
                soundDict[-28 + SHIFT].play()
            if event.key == pg.K_t:
                S.add(-27 + SHIFT)
                soundDict[-27 + SHIFT].play()
            if event.key == pg.K_6:
                S.add(-26 + SHIFT)
                soundDict[-26 + SHIFT].play()
            if event.key == pg.K_y:
                S.add(-25 + SHIFT)
                soundDict[-25 + SHIFT].play()
            if event.key == pg.K_u:
                S.add(-24 + SHIFT)
                soundDict[-24 + SHIFT].play()
            if event.key == pg.K_8:
                S.add(-23 + SHIFT)
                soundDict[-23 + SHIFT].play()
            if event.key == pg.K_i:
                S.add(-22 + SHIFT)
                soundDict[-22 + SHIFT].play()
            if event.key == pg.K_9:
                S.add(-21 + SHIFT)
                soundDict[-21 + SHIFT].play()
            if event.key == pg.K_o:
                S.add(-20 + SHIFT)
                soundDict[-20 + SHIFT].play()
            if event.key == pg.K_p:
                S.add(-19 + SHIFT)
                soundDict[-19 + SHIFT].play()
            if event.key == pg.K_MINUS:
                S.add(-18 + SHIFT)
                soundDict[-18 + SHIFT].play()

            if event.key == pg.K_LSHIFT:
                S.add(-24 + SHIFT)
                soundDict[-24 + SHIFT].play()
            if event.key == pg.K_a:
                S.add(-23 + SHIFT)
                soundDict[-23 + SHIFT].play()
            if event.key == pg.K_z:
                S.add(-22 + SHIFT)
                soundDict[-22 + SHIFT].play()
            if event.key == pg.K_s:
                S.add(-21 + SHIFT)
                soundDict[-21 + SHIFT].play()
            if event.key == pg.K_x:
                S.add(-20 + SHIFT)
                soundDict[-20 + SHIFT].play()
            if event.key == pg.K_c:
                S.add(-19 + SHIFT)
                soundDict[-19 + SHIFT].play()
            if event.key == pg.K_f:
                S.add(-18 + SHIFT)
                soundDict[-18 + SHIFT].play()
            if event.key == pg.K_v:
                S.add(-17 + SHIFT)
                soundDict[-17 + SHIFT].play()
            if event.key == pg.K_g:
                S.add(-16 + SHIFT)
                soundDict[-16 + SHIFT].play()
            if event.key == pg.K_b:
                S.add(-15 + SHIFT)
                soundDict[-15 + SHIFT].play()
            if event.key == pg.K_h:
                S.add(-14 + SHIFT)
                soundDict[-14 + SHIFT].play()
            if event.key == pg.K_n:
                S.add(-13 + SHIFT)
                soundDict[-13 + SHIFT].play()
            if event.key == pg.K_m:
                S.add(-12 + SHIFT)
                soundDict[-12 + SHIFT].play()
            if event.key == pg.K_k:
                S.add(-11 + SHIFT)
                soundDict[-11 + SHIFT].play()
            if event.key == pg.K_COMMA:
                S.add(-10 + SHIFT)
                soundDict[-10 + SHIFT].play()
            if event.key == pg.K_l:
                S.add(-9 + SHIFT)
                soundDict[-9 + SHIFT].play()
            if event.key == pg.K_PERIOD:
                S.add(-8 + SHIFT)
                soundDict[-8 + SHIFT].play()
            if event.key == pg.K_SLASH:
                S.add(-7 + SHIFT)
                soundDict[-7 + SHIFT].play()
            if event.key == pg.K_QUOTE:
                S.add(-6 + SHIFT)
                soundDict[-6 + SHIFT].play()
            if event.key == pg.K_RSHIFT:
                S.add(-5 + SHIFT)
                soundDict[-5 + SHIFT].play()
            if event.key == pg.K_RETURN:
                S.add(-4 + SHIFT)
                soundDict[-4 + SHIFT].play()
            if event.key == pg.K_LEFT:
                S.add(-3 + SHIFT)
                soundDict[-3 + SHIFT].play()
            if event.key == pg.K_UP:
                S.add(-2 + SHIFT)
                soundDict[-2 + SHIFT].play()
            if event.key == pg.K_DOWN:
                S.add(-1 + SHIFT)
                soundDict[-1 + SHIFT].play()
            if event.key == pg.K_RIGHT:
                S.add(0 + SHIFT)
                soundDict[0 + SHIFT].play()
            if event.key == pg.K_KP_4:
                S.add(1 + SHIFT)
                soundDict[1 + SHIFT].play()
            if event.key == pg.K_KP_1:
                S.add(2 + SHIFT)
                soundDict[2 + SHIFT].play()
            if event.key == pg.K_KP_5:
                S.add(3 + SHIFT)
                soundDict[3 + SHIFT].play()
            if event.key == pg.K_KP_2:
                S.add(4 + SHIFT)
                soundDict[4 + SHIFT].play()
            if event.key == pg.K_KP_3:
                S.add(5 + SHIFT)
                soundDict[5 + SHIFT].play()
            if event.key == pg.K_KP_6:
                S.add(6 + SHIFT)
                soundDict[6 + SHIFT].play()
            if event.key == pg.K_KP_ENTER:
                S.add(7 + SHIFT)
                soundDict[7 + SHIFT].play()

            if event.key == pg.K_LEFTBRACKET:
                S.add(0 + SHIFT)
                soundDict[0 + SHIFT].play()
            if event.key == pg.K_EQUALS:
                S.add(1 + SHIFT)
                soundDict[1 + SHIFT].play()
            if event.key == pg.K_RIGHTBRACKET:
                S.add(2 + SHIFT)
                soundDict[2 + SHIFT].play()
            if event.key == pg.K_BACKSPACE:
                S.add(3 + SHIFT)
                soundDict[3 + SHIFT].play()
            if event.key == pg.K_BACKSLASH:
                S.add(4 + SHIFT)
                soundDict[4 + SHIFT].play()
            if event.key == pg.K_DELETE:
                S.add(5 + SHIFT)
                soundDict[5 + SHIFT].play()
            if event.key == pg.K_END:
                S.add(7 + SHIFT)
                soundDict[7 + SHIFT].play()
            if event.key == pg.K_PAGEDOWN:
                S.add(9 + SHIFT)
                soundDict[9 + SHIFT].play()
            if event.key == pg.K_KP_7:
                S.add(11 + SHIFT)
                soundDict[11 + SHIFT].play()
            if event.key == pg.K_KP_8:
                S.add(12 + SHIFT)
                soundDict[12 + SHIFT].play()
            if event.key == pg.K_KP_9:
                S.add(14 + SHIFT)
                soundDict[14 + SHIFT].play()
            if event.key == pg.K_KP_PLUS:
                S.add(16 + SHIFT)
                soundDict[16 + SHIFT].play()

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
                if (-36 + SHIFT) in S:
                    S.remove(-36 + SHIFT)
                soundDict[-36 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_1:
                if (-35 + SHIFT) in S:
                    S.remove(-35 + SHIFT)
                soundDict[-35 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_q:
                if (-34 + SHIFT) in S:
                    S.remove(-34 + SHIFT)
                soundDict[-34 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_2:
                if (-33 + SHIFT) in S:
                    S.remove(-33 + SHIFT)
                soundDict[-33 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_w:
                if (-32 + SHIFT) in S:
                    S.remove(-32 + SHIFT)
                soundDict[-32 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_e:
                if (-31 + SHIFT) in S:
                    S.remove(-31 + SHIFT)
                soundDict[-31 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_4:
                if (-30 + SHIFT) in S:
                    S.remove(-30 + SHIFT)
                soundDict[-30 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_r:
                if (-29 + SHIFT) in S:
                    S.remove(-29 + SHIFT)
                soundDict[-29 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_5:
                if (-28 + SHIFT) in S:
                    S.remove(-28 + SHIFT)
                soundDict[-28 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_t:
                if (-27 + SHIFT) in S:
                    S.remove(-27 + SHIFT)
                soundDict[-27 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_6:
                if (-26 + SHIFT) in S:
                    S.remove(-26 + SHIFT)
                soundDict[-26 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_y:
                if (-25 + SHIFT) in S:
                    S.remove(-25 + SHIFT)
                soundDict[-25 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_u:
                if (-24 + SHIFT) in S:
                    S.remove(-24 + SHIFT)
                soundDict[-24 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_8:
                if (-23 + SHIFT) in S:
                    S.remove(-23 + SHIFT)
                soundDict[-23 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_i:
                if (-22 + SHIFT) in S:
                    S.remove(-22 + SHIFT)
                soundDict[-22 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_9:
                if (-21 + SHIFT) in S:
                    S.remove(-21 + SHIFT)
                soundDict[-21 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_o:
                if (-20 + SHIFT) in S:
                    S.remove(-20 + SHIFT)
                soundDict[-20 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_p:
                if (-19 + SHIFT) in S:
                    S.remove(-19 + SHIFT)
                soundDict[-19 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_MINUS:
                if (-18 + SHIFT) in S:
                    S.remove(-18 + SHIFT)
                soundDict[-18 + SHIFT].fadeout(yanyin)

            if event.key == pg.K_LSHIFT:
                if (-24 + SHIFT) in S:
                    S.remove(-24 + SHIFT)
                soundDict[-24 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_a:
                if (-23 + SHIFT) in S:
                    S.remove(-23 + SHIFT)
                soundDict[-23 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_z:
                if (-22 + SHIFT) in S:
                    S.remove(-22 + SHIFT)
                soundDict[-22 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_s:
                if (-21 + SHIFT) in S:
                    S.remove(-21 + SHIFT)
                soundDict[-21 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_x:
                if (-20 + SHIFT) in S:
                    S.remove(-20 + SHIFT)
                soundDict[-20 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_c:
                if (-19 + SHIFT) in S:
                    S.remove(-19 + SHIFT)
                soundDict[-19 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_f:
                if (-18 + SHIFT) in S:
                    S.remove(-18 + SHIFT)
                soundDict[-18 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_v:
                if (-17 + SHIFT) in S:
                    S.remove(-17 + SHIFT)
                soundDict[-17 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_g:
                if (-16 + SHIFT) in S:
                    S.remove(-16 + SHIFT)
                soundDict[-16 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_b:
                if (-15 + SHIFT) in S:
                    S.remove(-15 + SHIFT)
                soundDict[-15 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_h:
                if (-14 + SHIFT) in S:
                    S.remove(-14 + SHIFT)
                soundDict[-14 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_n:
                if (-13 + SHIFT) in S:
                    S.remove(-13 + SHIFT)
                soundDict[-13 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_m:
                if (-12 + SHIFT) in S:
                    S.remove(-12 + SHIFT)
                soundDict[-12 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_k:
                if (-11 + SHIFT) in S:
                    S.remove(-11 + SHIFT)
                soundDict[-11 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_COMMA:
                if (-10 + SHIFT) in S:
                    S.remove(-10 + SHIFT)
                soundDict[-10 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_l:
                if (-9 + SHIFT) in S:
                    S.remove(-9 + SHIFT)
                soundDict[-9 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_PERIOD:
                if (-8 + SHIFT) in S:
                    S.remove(-8 + SHIFT)
                soundDict[-8 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_SLASH:
                if (-7 + SHIFT) in S:
                    S.remove(-7 + SHIFT)
                soundDict[-7 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_QUOTE:
                if (-6 + SHIFT) in S:
                    S.remove(-6 + SHIFT)
                soundDict[-6 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_RSHIFT:
                if (-5 + SHIFT) in S:
                    S.remove(-5 + SHIFT)
                soundDict[-5 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_RETURN:
                if (-4 + SHIFT) in S:
                    S.remove(-4 + SHIFT)
                soundDict[-4 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_LEFT:
                if (-3 + SHIFT) in S:
                    S.remove(-3 + SHIFT)
                soundDict[-3 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_UP:
                if (-2 + SHIFT) in S:
                    S.remove(-2 + SHIFT)
                soundDict[-2 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_DOWN:
                if (-1 + SHIFT) in S:
                    S.remove(-1 + SHIFT)
                soundDict[-1 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_RIGHT:
                if (0 + SHIFT) in S:
                    S.remove(0 + SHIFT)
                soundDict[0 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_KP_4:
                if (1 + SHIFT) in S:
                    S.remove(1 + SHIFT)
                soundDict[1 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_KP_1:
                if (2 + SHIFT) in S:
                    S.remove(2 + SHIFT)
                soundDict[2 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_KP_5:
                if (3 + SHIFT) in S:
                    S.remove(3 + SHIFT)
                soundDict[3 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_KP_2:
                if (4 + SHIFT) in S:
                    S.remove(4 + SHIFT)
                soundDict[4 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_KP_3:
                if (5 + SHIFT) in S:
                    S.remove(5 + SHIFT)
                soundDict[5 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_KP_6:
                if (6 + SHIFT) in S:
                    S.remove(6 + SHIFT)
                soundDict[6 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_KP_ENTER:
                if (7 + SHIFT) in S:
                    S.remove(7 + SHIFT)
                soundDict[7 + SHIFT].fadeout(yanyin)

            if event.key == pg.K_LEFTBRACKET:
                if (0 + SHIFT) in S:
                    S.remove(0 + SHIFT)
                soundDict[0 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_EQUALS:
                if (1 + SHIFT) in S:
                    S.remove(1 + SHIFT)
                soundDict[1 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_RIGHTBRACKET:
                if (2 + SHIFT) in S:
                    S.remove(2 + SHIFT)
                soundDict[2 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_BACKSPACE:
                if (3 + SHIFT) in S:
                    S.remove(3 + SHIFT)
                soundDict[3 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_BACKSLASH:
                if (4 + SHIFT) in S:
                    S.remove(4 + SHIFT)
                soundDict[4 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_DELETE:
                if (5 + SHIFT) in S:
                    S.remove(5 + SHIFT)
                soundDict[5 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_END:
                if (7 + SHIFT) in S:
                    S.remove(7 + SHIFT)
                soundDict[7 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_PAGEDOWN:
                if (9 + SHIFT) in S:
                    S.remove(9 + SHIFT)
                soundDict[9 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_KP_7:
                if (11 + SHIFT) in S:
                    S.remove(11 + SHIFT)
                soundDict[11 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_KP_8:
                if (12 + SHIFT) in S:
                    S.remove(12 + SHIFT)
                soundDict[12 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_KP_9:
                if (14 + SHIFT) in S:
                    S.remove(14 + SHIFT)
                soundDict[14 + SHIFT].fadeout(yanyin)
            if event.key == pg.K_KP_PLUS:
                if (16 + SHIFT) in S:
                    S.remove(16 + SHIFT)
                soundDict[16 + SHIFT].fadeout(yanyin)
            # if event.key == pg.K_i:
            # if in S:
            #                         # S.remove(14)
            #     soundDict[14+SHIFT].fadeout(yanyin)
            # if event.key == pg.K_o:
            # if in S:
            #                         # S.remove(16)
            #     soundDict[16+SHIFT].fadeout(yanyin)
            # if event.key == pg.K_p:
            # if in S:
            #                         # S.remove(17)
            #     soundDict[17+SHIFT].fadeout(yanyin)
            # if event.key == pg.K_LEFTBRACKET:
            # if in S:
            #                         # S.remove(19)
            #     soundDict[19+SHIFT].fadeout(yanyin)
            # if event.key == pg.K_RIGHTBRACKET:
            # if in S:
            #                         # S.remove(21)
            #     soundDict[21+SHIFT].fadeout(yanyin)
            # if event.key == pg.K_BACKSLASH:
            # if in S:
            #                         # S.remove(23)
            #     soundDict[23+SHIFT].fadeout(yanyin)
    print(S, len(S))
    for i in S:
        soundDict[i].set_volume(kk / np.log(len(S) + 2))
    pg.display.flip()
    mainClock.tick(240)

pg.quit()
