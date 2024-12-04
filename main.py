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
from ai import (
    target_next_active,
    target_basic,
    target_weakest,
    target_random,
    target_strongest,
)


def main():
    setup_teams()

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
        waiting_input, turn_order = GAME.tick()
        HUD.set_order(turn_order)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if waiting_input and event.key == pygame.K_SPACE:
                    for entity in turn_order:
                        if entity.turnmeter >= 1000:
                            entity.take_turn()
                            break
                    waiting_input = False
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    HUD.scroll_log(up=True)
                else:
                    HUD.scroll_log(up=False)

        # Draw entities
        screen.fill(BLACK)
        turn_order[0].draw(screen, your_turn=waiting_input)
        if waiting_input:
            HUD.set_actions(turn_order[0])
        for entity in turn_order[1:]:
            entity.draw(screen)
        HUD.draw(screen)
        pygame.display.flip()

        CLOCK.tick(FPS)


def setup_teams():
    # Set up entities
    from characters import units

    for i, unit in enumerate(units):
        image = pygame.image.load(os.path.join("assets", unit["file"]))
        image = pygame.transform.scale_by(image, 0.6)
        # image.set_colorkey(VIOLETGREY)
        GAME.player_set.append(
            Character(
                unit["name"],
                image,
                (75, 40 + i * 110),
                unit["resilience"],
                unit["action_dice"],
                unit["speed"],
                p_bst=unit["p_bst"],
                def_p=unit["def_p"],
                ai=choice([target_next_active, target_basic, target_weakest]),
            )
        )

    for i, unit in enumerate(units):
        image = pygame.image.load(os.path.join("assets", unit["file"]))
        image = pygame.transform.scale_by(image, 0.6)
        # image.set_colorkey(VIOLETGREY)
        ai = choice(
            [
                target_next_active,
                target_basic,
                target_weakest,
                target_strongest,
                target_random,
            ]
        )
        GAME.enemy_set.append(
            Character(
                "enemy" + unit["name"],
                image,
                (350, 40 + i * 110),
                unit["resilience"],
                unit["action_dice"],
                unit["speed"],
                p_bst=unit["p_bst"],
                def_p=unit["def_p"],
                ai=ai,
            )
        )

    image = pygame.image.load(os.path.join("assets", "beast.png"))
    image.set_colorkey(VIOLETGREY)
    ai = target_next_active
    kronk = Beast(  # Kronk is a special entity
        "Kronk", image, (350, 80), 10, 6, 85, ai=ai, p_bst=2, def_p=2
    )
    print(kronk)


if __name__ == "__main__":
    main()
