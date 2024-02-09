import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("lll")
clock = pygame.time.Clock()

test_surface = pygame.Surface((100, 200))
test_surface.fill("red")

x, y = (100, 200)


while True:
    for event in pygame.event.get():
        print(event, event.type, pygame.KEYUP)
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.dict["key"] == pygame.K_UP:
                y += -10
            if event.dict["key"] == pygame.K_RIGHT:
                x += 10
    screen.blit(test_surface, (x, y))
    pygame.image.save(pygame.display.get_surface(), "./rrl.png")
    pygame.display.set_caption(f"{clock.get_fps():.0f}")
    pygame.display.update()
    clock.tick(60)
