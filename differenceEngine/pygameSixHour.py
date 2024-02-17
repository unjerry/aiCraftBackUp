import pygame


class main_game:
    def __init__(self) -> None:
        pygame.init()

        pygame.display.set_caption("rapt")
        self.screen = pygame.display.set_mode((800, 600))

        self.clock = pygame.time.Clock()
        self.img = pygame.image.load("./images/img.png")

        self.is_running = 1


    def run(self):
        while self.is_running:

            self.screen.blit(self.img, pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.is_running = 0

            pygame.display.flip()
            delta_time = self.clock.tick(60)


game_instance = main_game()
game_instance.run()
