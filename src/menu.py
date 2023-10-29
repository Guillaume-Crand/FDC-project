import pygame

from src.utils.button import Button

class Menu():
    FONT = pygame.font.Font("font/Pixelcastle-Regular.otf", 45)
    buttons = []

    def __init(self, screen: pygame.Surface):

        width, height = screen.get_size()
        self.bg_img = pygame.image.load("img/moutains.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, (width, height))

        self.title_text = self.FONT.render("Fromages du Chaos")
        self.title_rect = self.text.get_rect()
        self.title_rect.center(width // 2, height // 8)

        self.init_buttons(self)

    def init_buttons(self):
        solo_button = Button()
        self.buttons.append(solo_button)
        self.buttons.append(multi_button)
        self.buttons.append(credit_button)
        self.buttons.append(settings_button)
        self.buttons.append(quit_button)

    def blit(self, screen: pygame.Surface):
        screen.blit(self.bg_img)
        screen.blit(self.textRect)
        """for (b in self.buttons)
            screen.blit(b)"""
