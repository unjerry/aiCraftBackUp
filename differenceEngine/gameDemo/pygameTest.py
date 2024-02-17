import pygame as pg
import moderngl as mgl
from util import load_image, load_images
from tilemap import tile_map


# 6hour
class physics_entity:
    def __init__(self, game, e_type, pos, size) -> None:
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {"up": False, "down": False, "right": False, "left": False}

    def rect(self):
        return pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {"up": False, "down": False, "right": False, "left": False}
        frame_movement = (
            movement[0] + self.velocity[0],
            movement[1] + self.velocity[1],
        )
        self.velocity[1] += 0.098 - 0.005 * self.velocity[1]
        print(self.velocity)
        self.pos[0] += frame_movement[0]
        entt_rect = self.rect()
        for rec in tilemap.physics_around(self.pos):
            if entt_rect.colliderect(rec):
                if frame_movement[0] > 0:
                    entt_rect.right = rec.left
                    self.collisions["right"] = True
                if frame_movement[0] < 0:
                    entt_rect.left = rec.right
                    self.collisions["left"] = True
                self.pos[0] = entt_rect.x
        self.pos[1] += frame_movement[1]
        entt_rect = self.rect()
        for rec in tilemap.physics_around(self.pos):
            if entt_rect.colliderect(rec):
                if frame_movement[1] > 0:
                    entt_rect.bottom = rec.top
                    self.collisions["down"] = True
                if frame_movement[1] < 0:
                    entt_rect.top = rec.bottom
                    self.collisions["up"] = True
                self.pos[1] = entt_rect.y
        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

    def render(self, surf):
        surf.blit(self.game.assets["player"], self.pos)


class Player(pg.sprite.Sprite):
    def __init__(self, x, y, ofst, ground):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("./images/compositionIcon.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.offset = ofst
        self.ground = ground
        self.rect.center = (
            x + ofst[0] * self.ground.get_size()[0],
            y + ofst[1] * self.ground.get_size()[1],
        )

    def update(self) -> None:
        self.keyboard_control()
        # print(self.rect.center)

    def draw(self):
        self.ground.blit(
            self.rect,
        )

    def keyboard_control(self):
        PLAYER_SPEED = 1.0
        key_state = pg.key.get_pressed()
        vel = PLAYER_SPEED  # * self.app.dtime
        if key_state[pg.K_w] | key_state[pg.K_UP]:
            self.rect.move_ip(0, -vel)
        if key_state[pg.K_s] | key_state[pg.K_DOWN]:
            self.rect.move_ip(0, vel)
        if key_state[pg.K_d] | key_state[pg.K_RIGHT]:
            self.rect.move_ip(vel, 0)
        if key_state[pg.K_a] | key_state[pg.K_LEFT]:
            self.rect.move_ip(-vel, 0)

        if self.rect.center[0] - self.offset[0] * self.ground.get_size()[0] < 0:
            self.rect.move_ip(self.ground.get_size()[0], 0)
        if (
            self.rect.center[0] - self.offset[0] * self.ground.get_size()[0]
            > self.ground.get_size()[0]
        ):
            self.rect.move_ip(-self.ground.get_size()[0], 0)
        if self.rect.center[1] - self.offset[1] * self.ground.get_size()[1] < 0:
            self.rect.move_ip(0, self.ground.get_size()[1])
        if (
            self.rect.center[1] - self.offset[1] * self.ground.get_size()[1]
            > self.ground.get_size()[1]
        ):
            self.rect.move_ip(0, -self.ground.get_size()[1])


class main_game:
    def __init__(self, win_size=(1600 / 1.5, 900 / 1.5)) -> None:
        # init pygame modules
        pg.init()
        # window size
        self.WIN_SIZE = win_size
        # set opengl attr
        self.screen = pg.display.set_mode(self.WIN_SIZE)
        self.clock = pg.time.Clock()
        self.is_running = 1
        self.ground = pg.image.load("./images/img4.png").convert()
        self.window = pg.Surface(self.ground.get_size())
        self.pls = pg.sprite.Group()
        self.pls.add(
            [
                [Player(50, 40, (i, j), self.ground) for i in range(0, 1)]
                for j in range(1)
            ]
        )
        self.movement = [False, False]

        self.assets = {"player": load_image("rrr.png"), "grass": load_images("grass")}

        self.tilmp = tile_map(self)
        self.player = physics_entity(self, "player", (50, 100), (16, 16))

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                self.is_running = 0
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.movement[0] = True
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.movement[1] = True
                if event.key == pg.K_UP or event.key == pg.K_SPACE:
                    self.player.velocity[1] += -3
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.movement[0] = False
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.movement[1] = False

    def render(self):
        # clear framebuffer
        self.screen.fill(color=(0.08 * 255, 0.16 * 255, 0.18 * 255))
        # render
        self.window.blit(self.ground, (0, 0))
        self.tilmp.render(self.window)
        self.pls.update()
        self.pls.draw(self.window)
        self.player.update(self.tilmp, (self.movement[1] - self.movement[0], 0))
        self.player.render(self.window)
        self.screen.blit(self.window, (10, 100))
        # swap buffer
        pg.display.flip()

    def run(self):
        while self.is_running:
            self.check_events()
            if not self.is_running:
                break
            self.render()
            self.clock.tick(60)


if __name__ == "__main__":
    app = main_game()
    app.run()
