import pygame


class Background(pygame.sprite.Sprite):
    FONT = pygame.font.Font("font/Pixelcastle-Regular.otf", 90)

    def __init__(self, screen: pygame.Surface):
        super(Background, self).__init__()

        width, height = screen.get_size()

        self.bg_img = pygame.image.load("img/moutains.png")
        self.bg_img = pygame.transform.scale(self.bg_img, (width, height))

        self.text = self.FONT.render("Press p to leave the game", True, "red")
        self.textRect = self.text.get_rect()
        self.textRect.center = (width // 2, height // 2)

    def blit(self, screen: pygame.Surface):
        screen.blit(self.bg_img, (0, 0))
        screen.blit(self.text, self.textRect)
