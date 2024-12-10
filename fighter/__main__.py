import pygame
import os
from .constants import const as c
from .constants import color
from .controllers.game import (
    GAME,
    CLOCK,
)
from .controllers.screen_writer import write_headline
from .entities.entities import Character, Beast
from .entities.classes import Caster, Retaliator, Quick
from .controllers.hud import HUD
from .entities.ai import (
    target_next_active,
    target_weakest,
    target_weak_to_will,
    target_strongest,
)


def main():
    setup_teams()
    # Create a surface and populate it
    screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
    screen.fill(color.BLACK)
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
        pygame.display.flip()

        CLOCK.tick(c.FPS)


def setup_teams():
    # Set up entities
    from .stable import units

    def load_unit(unit, player, team_pos):
        if player:
            x_align = c.BORDER + c.PLAYER_COLUMN
        else:
            x_align = c.BORDER + c.ENEMY_COLUMN
        image = pygame.image.load(
            os.path.join("assets", unit["file"])
        )
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
            (x_align, c.TOP_PADDING + team_pos * 110),
            unit["resilience"],
            unit["action_dice"],
            unit["speed"],
            p_boost=unit.get("p_bst", 100),
            p_defense=unit.get("def_p", 100),
            w_boost=unit.get("w_bst", 100),
            w_defense=unit.get("def_w", 100),
            a_boost=unit.get("a_bst", 100),
            a_defense=unit.get("def_a", 100),
            ai=ai,
        )

    for i, unit in enumerate(units):
        GAME.player_set.append(load_unit(unit, True, i))
        # unit['name'] = f"Enemy {unit['name']}"
        # GAME.enemy_set.append(load_unit(unit, False, i))

    image = pygame.image.load(
        os.path.join("assets", "beast.png")
    )
    ai = target_next_active
    kronk = Beast(  # Kronk is a special 'Beast' entity
        "Kronk",
        image,
        (c.BORDER + c.ENEMY_COLUMN, c.TOP_PADDING + 40),
        70,
        60,
        90,
        ai=ai,
        p_boost=150,
        p_defense=170,
        a_defense=130,
        w_defense=110,
    )
    print(kronk)
    GAME.enemy_set.append(kronk)


if __name__ == "__main__":
    main()
