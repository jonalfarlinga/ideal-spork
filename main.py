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
        for entity in entities:
            entity.draw(screen)
        HUD.draw(screen)
        pygame.display.flip()

        CLOCK.tick(FPS)


def setup_test():
    # Set up entities
    image = pygame.image.load(os.path.join("assets", "blue.png"))
    image = pygame.transform.scale_by(image, 0.6)
    image = pygame.transform.flip(image, True, False)
    image.set_colorkey(VIOLETGREY)
    player = Character("Blue", image, (75, 40), 4, 5, 160)

    image = pygame.image.load(os.path.join("assets", "red.png"))
    image = pygame.transform.scale_by(image, 0.6)
    image.set_colorkey(VIOLETGREY)
    red = Character("Red", image, (75, 150), 5, 5, 95, p_bst=1)

    image = pygame.image.load(os.path.join("assets", "green.png"))
    image = pygame.transform.scale_by(image, 0.6)
    image.set_colorkey(VIOLETGREY)
    green = Character("Green", image, (75, 260), 6, 5, 80, p_bst=1, def_p=1)

    image = pygame.image.load(os.path.join("assets", "white.png"))
    image = pygame.transform.scale_by(image, 0.6)
    image.set_colorkey(VIOLETGREY)
    white = Character("White", image, (75, 370), 5, 5, 75, w_bst=1)

    image = pygame.image.load(os.path.join("assets", "beast.png"))
    image.set_colorkey(VIOLETGREY)
    kronk = Beast("Kronk", image, (350, 80), 10, 6, 85, ai=target_next_active, p_bst=2, def_p=2)

    GAME.player_set = [player, red, green, white]
    GAME.enemy_set = [kronk]


if __name__ == "__main__":
    main()
