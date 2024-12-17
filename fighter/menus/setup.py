import pygame
import os
from ..constants import const as c
from ..controllers.game import GAME
from ..entities.classes import CLASSES
from ..entities.ai import (
    target_next_active,
    TARGETING_AI,
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
        h = 70 / image.get_height()
        image = pygame.transform.scale_by(image, h)
        if not player:
            image = pygame.transform.flip(image, True, False)
        c_type = unit["class"]
        ai = unit["ai"]
        return CLASSES[c_type](
            unit["name"],
            image,
            (x_align, c.TOP_PADDING + team_pos * 110),
            ai=TARGETING_AI[ai],
        )

    for i, unit in enumerate(units):
        GAME.player_set.append(load_unit(unit, True, i))
        unit["name"] = f"Enemy {unit['name']}"
        GAME.enemy_set.append(load_unit(unit, False, i))

    image = pygame.image.load(os.path.join("assets", "beast.png"))
    ai = target_next_active
    kronk = CLASSES['Beast'](  # Kronk is a special 'Beast' entity
        "Kronk",
        image,
        (c.BORDER + c.ENEMY_COLUMN, c.TOP_PADDING + 40),
        ai=ai,
    )
    print(kronk)
    # GAME.enemy_set.append(kronk)
