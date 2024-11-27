import pygame
import os
from random import choice
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
from ai import target_next_active, target_basic, target_weakest


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
    units = [
        {
            "name": "Blue",
            "file": "blue.png",
            "resilience": 4,
            "speed": 160,
            "action_dice": 5,
            "p_bst": 0,
            "def_p": 0,
            "w_bst": 0,
        },
        {
            "name": "Red",
            "file": "red.png",
            "resilience": 5,
            "speed": 95,
            "action_dice": 5,
            "p_bst": 1,
            "def_p": 0,
            "w_bst": 0,
        },
        {
            "name": "Green",
            "file": "green.png",
            "resilience": 6,
            "speed": 80,
            "action_dice": 5,
            "p_bst": 1,
            "def_p": 1,
            "w_bst": 0,
        },
        {
            "name": "White",
            "file": "white.png",
            "resilience": 5,
            "speed": 75,
            "action_dice": 5,
            "p_bst": 0,
            "def_p": 0,
            "w_bst": 1,
        },
    ]
    for i, unit in enumerate(units):
        image = pygame.image.load(os.path.join("assets", unit["file"]))
        image = pygame.transform.scale_by(image, 0.6)
        image.set_colorkey(VIOLETGREY)
        GAME.player_set.append(Character(
            unit["name"],
            image,
            (75, 40 + i * 110),
            unit["resilience"],
            unit["action_dice"],
            unit["speed"],
            p_bst=unit["p_bst"],
            def_p=unit["def_p"],
            ai=choice([target_next_active, target_basic, target_weakest]),
        ))

    for i, unit in enumerate(units):
        image = pygame.image.load(os.path.join("assets", unit["file"]))
        image = pygame.transform.scale_by(image, 0.6)
        image.set_colorkey(VIOLETGREY)
        GAME.enemy_set.append(Character(
            "enemy" + unit["name"],
            image,
            (350, 40 + i * 110),
            unit["resilience"],
            unit["action_dice"],
            unit["speed"],
            p_bst=unit["p_bst"],
            def_p=unit["def_p"],
            ai=choice([target_next_active, target_basic, target_weakest]),
        ))

    image = pygame.image.load(os.path.join("assets", "beast.png"))
    image.set_colorkey(VIOLETGREY)
    kronk = Beast(
        "Kronk", image, (350, 80), 10, 6, 85, ai=target_next_active, p_bst=2, def_p=2
    )
    print(kronk)


if __name__ == "__main__":
    main()
