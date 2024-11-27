import pygame
import os
from game import (  # pygame_init() and constants setup in game.py
    CLOCK,
    FPS,
    VIOLETGREY,
    BLACK,
    GAME,
)
from screen_writer import write_headline
from entities import Character, Beast
from hud import HUD
from ai import target_next_active


def main():
    setup_test()

    # Create a surface and populate it
    screen = pygame.display.set_mode((800, 600))
    screen.fill(BLACK)
    write_headline(screen, "Game", (300, 100))
    for entity in GAME.player_set:
        entity.draw(screen)
    for entity in GAME.enemy_set:
        entity.draw(screen)
    HUD.draw(screen)
    pygame.display.flip()
    waiting_input = False

    # Main loop
    while True:
        waiting_input, entities = GAME.tick()
        HUD.set_order(entities)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if waiting_input and event.key == pygame.K_SPACE:
                    for entity in entities:
                        if entity.turnmeter >= 1000:
                            entity.take_turn(GAME)
                            break
                    waiting_input = False
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    HUD.scroll_log(up=True)
                else:
                    HUD.scroll_log(up=False)

        # Draw entities
        screen.fill(BLACK)
        for entity in GAME.player_set:
            entity.draw(screen)
        for entity in GAME.enemy_set:
            entity.draw(screen)
        HUD.draw(screen)
        pygame.display.flip()

        CLOCK.tick(FPS)


def setup_test():
    # Set up entities
    image = pygame.image.load(os.path.join("assets", "blue.png"))
    image = pygame.transform.scale(image, (60, 60))
    image = pygame.transform.flip(image, True, False)
    image.set_colorkey(VIOLETGREY)
    player = Character("Player", image, (100, 160), 5, 5, 110)
    image = pygame.image.load(os.path.join("assets", "red.png"))
    image = pygame.transform.scale(image, (60, 60))
    image.set_colorkey(VIOLETGREY)
    pygame.transform.scale(image, (60, 60))
    enemy = Character("Enemy", image, (100, 40), 5, 5, 100)

    image = pygame.image.load(os.path.join("assets", "mech.png"))
    image.set_colorkey(VIOLETGREY)
    mech = Beast("Mech", image, (250, 80), 6, 5, 85, ai=target_next_active)

    GAME.player_set = [player, enemy]
    GAME.enemy_set = [mech]


if __name__ == "__main__":
    main()
