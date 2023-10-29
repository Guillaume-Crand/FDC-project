import pygame

pygame.init()

from src.menu import Menu
from src.sprite.background import Background
from src.sprite.player import Player


if __name__ == "__main__":
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.toggle_fullscreen()

    width, height = screen.get_size()

    menu = Menu(screen)
    menu.blit(screen)

    player = Player()
    background = Background(screen)
    to_display = [background, player]
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_p:
                        running = False
                    case pygame.K_UP:
                        player.move(0, -1)
                    case pygame.K_DOWN:
                        player.move(0, 1)
                    case pygame.K_LEFT:
                        player.move(-1, 0)
                    case pygame.K_RIGHT:
                        player.move(1, 0)
                    case _:
                        pass
        menu.blit(screen)
        #for sprite in to_display:
            #sprite.blit(screen)
        # pygame.display.update()
        pygame.display.flip()

    pygame.quit()
