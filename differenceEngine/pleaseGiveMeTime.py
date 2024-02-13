import pygame

# from pygame.sprite import _Group

pygame.init()
main_screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
main_clock = pygame.time.Clock()
font_courier_new = pygame.font.Font("./fonts/COURE.FON")

main_icon = pygame.image.load("./images/compositionIcon.png")
greet_text = pygame.transform.scale_by(
    font_courier_new.render(
        "Just give me time, and leave the else to me.", False, "purple"
    ),
    3,
)
grave_text = font_courier_new.render("But you don't.", False, "purple")
print(greet_text.get_size())
print(grave_text.get_size())
pygame.display.set_icon(main_icon)


is_running = 1
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = 0
    main_screen.blit(greet_text, (0, 0))
    main_screen.blit(grave_text, (0, greet_text.get_size()[1]))
    pygame.display.flip()
    pygame.display.set_caption(f"fps:{main_clock.get_fps():.0f}")
    main_clock.tick(60)
