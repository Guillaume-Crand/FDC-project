import pygame

from src.utils.button import Button

class Menu():
    FONT = pygame.font.Font("font/Pixelcastle-Regular.otf", 45)
    buttons = []

    def __init__(self, screen: pygame.Surface):
        self.width, self.height = screen.get_size()
        self.bg_img = pygame.image.load("img/moutains.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (self.width, self.height))

        self.title = self.FONT.render("Fromages du Chaos", True, "red", "lightgray")
        self.title_rect = self.title.get_rect()
        self.title_rect.center = (self.width // 2, self.height // 8)

        self.init_buttons()

    def init_buttons(self):
        solo_button = Button((self.width // 4, self.height // 8 * 2), 20, 20, "Solo")
        self.buttons.append(solo_button)

        multi_button = Button((self.width // 4, (self.height // 8) * 6), 20, 20, "Multi")
        self.buttons.append(multi_button)

        credit_button = Button(((self.width // 4) * 3, self.height // 8 * 2), 20, 20, "Credit")
        self.buttons.append(credit_button)

        settings_button = Button(((self.width // 4) * 3, self.height // 8 * 2), 20, 20, "Option")
        self.buttons.append(settings_button)

        quit_button = Button(((self.width // 4) * 3, self.height // 8 * 2), 20, 20, "Solo")
        self.buttons.append(quit_button)

    def blit(self, screen: pygame.Surface):
        screen.blit(self.bg_img, (0, 0))
        screen.blit(self.title, self.title_rect)
        """for (b in self.buttons)
            screen.blit(b)"""
