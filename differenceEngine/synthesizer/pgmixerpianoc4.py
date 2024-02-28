import pygame as pg
import pygame.mixer as mixer
import numpy as np

pg.init()
mixer.init()
mainScreen = pg.display.set_mode((400, 400))
mainClock = pg.time.Clock()

soundDict = {}
for i in range(-13, 13):
    soundDict[i] = mixer.Sound(f"piano_c4/{i}.wav")
s0 = mixer.Sound("sine0.wav")


S = set()
isRunning = 1
while isRunning:
    for event in pg.event.get():
        print(event)
        if event.type == pg.QUIT:
            pg.quit()
            isRunning = 0
        if event.type == pg.KEYDOWN:
            print("down")
            if event.key == pg.K_a:
                S.add(-12)
                soundDict[-12].play()
            if event.key == pg.K_s:
                S.add(-10)
                soundDict[-10].play()
            if event.key == pg.K_d:
                S.add(-8)
                soundDict[-8].play()
            if event.key == pg.K_f:
                S.add(-7)
                soundDict[-7].play()
            if event.key == pg.K_SPACE:
                S.add(-5)
                soundDict[-5].play()
            if event.key == pg.K_z:
                S.add(-3)
                soundDict[-3].play()

            if event.key == pg.K_v:
                S.add(-1)
                soundDict[-1].play()
            if event.key == pg.K_b:
                S.add(0)
                soundDict[0].play()
            if event.key == pg.K_g:
                S.add(1)
                soundDict[1].play()
            if event.key == pg.K_h:
                S.add(2)
                soundDict[2].play()
            if event.key == pg.K_y:
                S.add(3)
                soundDict[3].play()
            if event.key == pg.K_j:
                S.add(4)
                soundDict[4].play()
            if event.key == pg.K_k:
                S.add(5)
                soundDict[5].play()
            if event.key == pg.K_l:
                S.add(7)
                soundDict[7].play()
            if event.key == pg.K_SEMICOLON:
                S.add(9)
                soundDict[9].play()
            if event.key == pg.K_QUOTE:
                S.add(11)
                soundDict[11].play()
            if event.key == pg.K_RETURN:
                S.add(12)
                soundDict[12].play()
        if event.type == pg.KEYUP:
            print("up")
            if event.key == pg.K_a:
                S.remove(-12)
                soundDict[-12].stop()
            if event.key == pg.K_s:
                S.remove(-10)
                soundDict[-10].stop()
            if event.key == pg.K_d:
                S.remove(-8)
                soundDict[-8].stop()
            if event.key == pg.K_f:
                S.remove(-7)
                soundDict[-7].stop()
            if event.key == pg.K_SPACE:
                S.remove(-5)
                soundDict[-5].stop()
            if event.key == pg.K_z:
                S.remove(-3)
                soundDict[-3].stop()

            if event.key == pg.K_v:
                S.remove(-1)
                soundDict[-1].stop()
            if event.key == pg.K_b:
                S.remove(0)
                soundDict[0].stop()
            if event.key == pg.K_g:
                S.remove(1)
                soundDict[1].stop()
            if event.key == pg.K_h:
                S.remove(2)
                soundDict[2].stop()
            if event.key == pg.K_y:
                S.remove(3)
                soundDict[3].stop()
            if event.key == pg.K_j:
                S.remove(4)
                soundDict[4].stop()
            if event.key == pg.K_k:
                S.remove(5)
                soundDict[5].stop()
            if event.key == pg.K_l:
                S.remove(7)
                soundDict[7].stop()
            if event.key == pg.K_SEMICOLON:
                S.remove(9)
                soundDict[9].stop()
            if event.key == pg.K_QUOTE:
                S.remove(11)
                soundDict[11].stop()
            if event.key == pg.K_RETURN:
                S.remove(12)
                soundDict[12].stop()
    print(S, len(S))
    for i in S:
        soundDict[i].set_volume(1 / np.log(len(S) + 2))
    pg.display.flip()
    mainClock.tick(10)
