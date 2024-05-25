print("hello world")


class Camera:
    def __init__(self, deg) -> None:
        self.degree: float = deg


class Player:
    def __init__(self, camera: Camera) -> None:
        self.camera: Camera = camera


# def change(a: int):
#     a += 1
# cmm = 0
# print(cmm)
# change(cmm)
# print(cmm)

cam = Camera(0.5)
pl1 = Player(cam)
print(cam.degree)
print(pl1.camera.degree)
pl1.camera.degree = 1
print(cam.degree)
print(pl1.camera.degree)
