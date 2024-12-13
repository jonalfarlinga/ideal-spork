import pygame
from .constants import const as c
from .constants import color
from .controllers.game import (
    GAME,
    CLOCK,
)
from .controllers.screen_writer import write_headline
from .controllers.hud import HUD
from .menus.menu import game_menu, win_menu


def main():
    # Create a surface and populate it
    screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
    screen.fill(color.BLACK)
    for entity in GAME.player_set:
        entity.draw(screen)
    for entity in GAME.enemy_set:
        entity.draw(screen)
    HUD.draw(screen)
    pygame.display.flip()

    while True:
        selection = game_menu(screen)
        match selection:
            case c.RUN_GAME:
                run_game(screen)
        selection = None


def run_game(screen):
    waiting_input = False
    # Main loop
    while True:
        waiting_input, turn_order = GAME.tick()
        HUD.set_order(turn_order)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and waiting_input:
                waiting_input = False
                match event.key:
                    case pygame.K_1:
                        if turn_order[0].turnmeter >= 1000:
                            turn_order[0].take_turn(c.ACTION_1)
                            break
                    case pygame.K_2:
                        if turn_order[0].turnmeter >= 1000:
                            turn_order[0].take_turn(c.ACTION_2)
                            break
                    case pygame.K_3:
                        if turn_order[0].turnmeter >= 1000:
                            turn_order[0].take_turn(c.ACTION_3)
                            break
                    case pygame.K_4:
                        if turn_order[0].turnmeter >= 1000:
                            turn_order[0].take_turn(c.ACTION_4)
                            break
                    case _:
                        waiting_input = True

            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    HUD.scroll_log(up=True)
                else:
                    HUD.scroll_log(up=False)

        # Draw entities
        screen.fill(color.BLACK)
        write_headline(screen, "Fight!", (300, 20))
        turn_order[0].draw(screen, your_turn=waiting_input)
        if waiting_input:
            HUD.set_actions(turn_order[0])
        for entity in turn_order[1:]:
            entity.draw(screen)
        HUD.draw(screen)
        if GAME.game_over():
            win_menu(screen)
            break
        pygame.display.flip()

        CLOCK.tick(c.FPS)


if __name__ == "__main__":
    main()
