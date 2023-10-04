import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.SIZE = 200
        self.STEP = 50
        self.COLOR = pygame.Color((0, 255, 0))

        self.surf = pygame.Surface((self.SIZE, self.SIZE))
        self.surf.fill(self.COLOR)
        self.rect = self.surf.get_rect()

    def blit(self, screen: pygame.Surface):
        screen.blit(self.surf, self.rect)

    def move(self, x: int, y: int):
        self.rect.move_ip(x * self.STEP, y * self.STEP)
