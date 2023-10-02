import pygame

pygame.init()


class Windows:
    FONT = pygame.font.Font("font/Pixelcastle-Regular.otf", 90)

    def __init__(self, screen):
        screen.fill((255, 255, 255))

        width, height = screen.get_size()
        bg_img = pygame.image.load("img/moutains.png")
        bg_img = pygame.transform.scale(bg_img, (width, height))
        screen.blit(bg_img, (0, 0))

        text = self.FONT.render("Press p to leave the game", True, "red")
        textRect = text.get_rect()
        textRect.center = (width // 2, height // 2)
        screen.blit(text, textRect)

        pygame.display.flip()


if __name__ == "__main__":
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.toggle_fullscreen()

    Windows(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    running = False

    pygame.quit()
