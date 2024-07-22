import pymunk
import time

m_length = 1

space = pymunk.Space()
space.gravity = (0, -9.8)

body = pymunk.Body(1, 1666)
body.position = (50, 0)

space.add(body)

t = 0
while True:
    space.step(1 / 50)
    print(body.position, t)
    t += space.current_time_step
    time.sleep(0.5)
