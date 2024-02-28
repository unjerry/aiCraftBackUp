import pygame as pg
import pygame.mixer as mixer

pg.init()
mixer.init()
mainScreen = pg.display.set_mode((400, 400))
mainClock = pg.time.Clock()

soundDict = {}
for i in range(-13, 13):
    soundDict[i] = mixer.Sound(f"sine{i}.wav")
s0 = mixer.Sound("sine0.wav")


S = set()
isRunning = 1
while isRunning:
    for event in pg.event.get():
        print(event)
        if event.type == pg.QUIT:
            pg.quit()
            isRunning = 0

    keys = pg.key.get_pressed()
    if keys[pg.K_a]:
        if -12 not in S:
            S.add(-12)
            soundDict[-12].play()
    if keys[pg.K_s]:
        if -10 not in S:
            S.add(-10)
            soundDict[-10].play()
    if keys[pg.K_d]:
        if -8 not in S:
            S.add(-8)
            soundDict[-8].play()
    if keys[pg.K_f]:
        if -7 not in S:
            S.add(-7)
            soundDict[-7].play()
    if keys[pg.K_SPACE]:
        if -5 not in S:
            S.add(-5)
            soundDict[-5].play()
    if keys[pg.K_z]:
        if -3 not in S:
            S.add(-3)
            soundDict[-3].play()

    if keys[pg.K_v]:
        if -1 not in S:
            S.add(-1)
            soundDict[-1].play()
    if keys[pg.K_b]:
        if 0 not in S:
            S.add(0)
            soundDict[0].play()
    if keys[pg.K_g]:
        if 1 not in S:
            S.add(1)
            soundDict[1].play()
    if keys[pg.K_h]:
        if 2 not in S:
            S.add(2)
            soundDict[2].play()
    if keys[pg.K_y]:
        if 3 not in S:
            S.add(3)
            soundDict[3].play()
    if keys[pg.K_j]:
        if 4 not in S:
            S.add(4)
            soundDict[4].play()
    if keys[pg.K_k]:
        if 5 not in S:
            S.add(5)
            soundDict[5].play()
    if keys[pg.K_l]:
        if 7 not in S:
            S.add(7)
            soundDict[7].play()
    if keys[pg.K_SEMICOLON]:
        if 9 not in S:
            S.add(9)
            soundDict[9].play()
    if keys[pg.K_QUOTE]:
        if 11 not in S:
            S.add(11)
            soundDict[11].play()
    if keys[pg.K_RETURN]:
        if 12 not in S:
            S.add(12)
            soundDict[12].play()

    if not keys[pg.K_a]:
        if -12 in S:
            S.remove(-12)
            soundDict[-12].stop()
    if not keys[pg.K_s]:
        if -10 in S:
            S.remove(-10)
            soundDict[-10].stop()
    if not keys[pg.K_d]:
        if -8 in S:
            S.remove(-8)
            soundDict[-8].stop()
    if not keys[pg.K_f]:
        if -7 in S:
            S.remove(-7)
            soundDict[-7].stop()
    if not keys[pg.K_SPACE]:
        if -5 in S:
            S.remove(-5)
            soundDict[-5].stop()
    if not keys[pg.K_z]:
        if -3 in S:
            S.remove(-3)
            soundDict[-3].stop()

    if not keys[pg.K_v]:
        if -1 in S:
            S.remove(-1)
            soundDict[-1].stop()
    if not keys[pg.K_b]:
        if 0 in S:
            S.remove(0)
            soundDict[0].stop()
    if not keys[pg.K_g]:
        if 1 in S:
            S.remove(1)
            soundDict[1].stop()
    if not keys[pg.K_h]:
        if 2 in S:
            S.remove(2)
            soundDict[2].stop()
    if not keys[pg.K_y]:
        if 3 in S:
            S.remove(3)
            soundDict[3].stop()
    if not keys[pg.K_j]:
        if 4 in S:
            S.remove(4)
            soundDict[4].stop()
    if not keys[pg.K_k]:
        if 5 in S:
            S.remove(5)
            soundDict[5].stop()
    if not keys[pg.K_l]:
        if 7 in S:
            S.remove(7)
            soundDict[7].stop()
    if not keys[pg.K_SEMICOLON]:
        if 9 in S:
            S.remove(9)
            soundDict[9].stop()
    if not keys[pg.K_QUOTE]:
        if 11 in S:
            S.remove(11)
            soundDict[11].stop()
    if not keys[pg.K_RETURN]:
        if 12 in S:
            S.remove(12)
            soundDict[12].stop()

    print(S, len(S))
    for i in S:
        soundDict[i].set_volume(1 / len(S))
    pg.display.flip()
    mainClock.tick(10)
