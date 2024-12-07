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
from characters import Caster, Retaliator, Quick
from hud import HUD
from ai import (
    target_next_active,
    target_weakest,
    target_weak_to_will,
    target_strongest,
    # target_basic,
    # target_random,
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
            if event.type == pygame.KEYDOWN and waiting_input:
                waiting_input = False
                match event.key:
                    case pygame.K_1:
                        if turn_order[0].turnmeter >= 1000:
                            turn_order[0].take_turn(1)
                            break
                    case pygame.K_2:
                        if turn_order[0].turnmeter >= 1000:
                            turn_order[0].take_turn(2)
                            break
                    case pygame.K_3:
                        if turn_order[0].turnmeter >= 1000:
                            turn_order[0].take_turn(3)
                            break
                    case pygame.K_4:
                        if turn_order[0].turnmeter >= 1000:
                            turn_order[0].take_turn(4)
                            break
                    case _:
                        waiting_input = True

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
    from stable import units

    def load_unit(unit, player, team_pos):
        if player:
            x_align = 75
        else:
            x_align = 350
        image = pygame.image.load(os.path.join("assets", unit["file"]))
        image = pygame.transform.scale_by(image, 0.6)
        if not player:
            image = pygame.transform.flip(image, True, False)
        c_type = Character
        ai = target_next_active
        match unit["name"].split(" ")[-1]:
            case "White":
                c_type = Caster
                ai = target_weak_to_will
            case "Green":
                c_type = Retaliator
                ai = target_strongest
            case "Blue":
                c_type = Quick
                ai = target_weakest
        return c_type(
            unit["name"],
            image,
            (x_align, 40 + team_pos * 110),
            unit["resilience"],
            unit["action_dice"],
            unit["speed"],
            p_bst=unit.get("p_bst", 0),
            def_p=unit.get("def_p", 0),
            w_bst=unit.get("w_bst", 0),
            def_w=unit.get("def_w", 0),
            a_bst=unit.get("a_bst", 0),
            def_a=unit.get("def_a", 0),
            ai=ai,
        )

    for i, unit in enumerate(units):
        GAME.player_set.append(
            load_unit(unit, True, i)
        )

    for i, unit in enumerate(units):
        unit['name'] = f"Enemy {unit['name']}"
        GAME.enemy_set.append(
            load_unit(unit, False, i)
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
