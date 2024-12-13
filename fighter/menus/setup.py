import pygame
import os
from ..constants import const as c
from ..controllers.game import GAME
from ..entities.entities import Character, Beast
from ..entities.classes import Caster, Retaliator, Quick
from ..entities.ai import (
    target_next_active,
    target_weakest,
    target_weak_to_will,
    target_strongest,
)


def setup_teams():
    GAME.reset()
    # Set up entities
    from .stable import units

    def load_unit(unit, player, team_pos):
        if player:
            x_align = c.BORDER + c.PLAYER_COLUMN
        else:
            x_align = c.BORDER + c.ENEMY_COLUMN
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
            (x_align, c.TOP_PADDING + team_pos * 110),
            ai=ai,
        )

    for i, unit in enumerate(units):
        GAME.player_set.append(load_unit(unit, True, i))
        unit = {
            "name": f"Enemy {unit['name']}",
            "file": unit["file"],
        }
        GAME.enemy_set.append(load_unit(unit, False, i))

    image = pygame.image.load(os.path.join("assets", "beast.png"))
    ai = target_next_active
    kronk = Beast(  # Kronk is a special 'Beast' entity
        "Kronk",
        image,
        (c.BORDER + c.ENEMY_COLUMN, c.TOP_PADDING + 40),
        ai=ai,
    )
    print(kronk)
    # GAME.enemy_set.append(kronk)
