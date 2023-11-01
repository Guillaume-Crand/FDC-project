import pygame

pygame.init()

from src.network.const import is_server
from src.sprite.background import Background
from src.sprite.player import Player

if __name__ == "__main__":
    screen = pygame.display.set_mode((600, 400))
    # pygame.display.toggle_fullscreen()

    width, height = screen.get_size()

    player = Player()
    background = Background(screen)
    to_display = [background, player]

    # server = Server(port=40910)
    # server.start()

    running = True
    while running:
        for event in pygame.event.get():
            print(event, event.type)
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                print(event.key)
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
                    # case pygame.K_o:
                    #     print("Key o")
                    #     server.add_messages("saucisse")
                    case pygame.K_f:
                        pygame.display.toggle_fullscreen()
                    case _:
                        pass

        for sprite in to_display:
            sprite.blit(screen)
        # pygame.display.update()
        pygame.display.flip()

    # server.continue_loop = False
    pygame.quit()

    print("Game closed")
