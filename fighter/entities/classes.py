from ..controllers.hud import HUD
from .entities import Character
from .actions import Action
from .attacks import (
    basic_attack,
    basic_magic_attack,
    basic_precise_attack,
    riposte_attack,
    regenerate,
    fireball_attack,
)


class Caster(Character):
    def __init__(self, *args, **kwargs):
        kwargs.update({
            'resilience': 50,
            'speed': 75,
            'action_dice': 50,
            'w_boost': 140,
            'w_defense': 130,
        })
        super().__init__(*args, **kwargs)
        self.actions = [
            Action("Basic Magic Attack", 0, basic_magic_attack),
            Action("Fireball", 3, fireball_attack),
        ]


class Retaliator(Character):
    def __init__(self, *args, **kwargs):
        kwargs.update({
            'resilience': 60,
            'speed': 70,
            'action_dice': 50,
            'p_defense': 130,
            'a_defense': 130,
            'w_defense': 130,
        })
        super().__init__(*args, **kwargs)
        self.actions = [
            Action("Basic Attack", 0, basic_attack),
            Action("Regenerate", 3, regenerate),
        ]

    def hit(self, damage, attack_type, attacker):
        damage = self.defend_against(damage, attack_type)
        if not damage:
            HUD.log_message(f"    {self.name} takes 0 damage!")
        else:
            self.take_damage(damage)
        if self.resilience > 0 and not self.active:
            HUD.log_message(f"{self} retaliates against {attacker}!")
            basic_attack(self, attacker)


class Quick(Character):
    def __init__(self, *args, **kwargs):
        kwargs.update({
            'resilience': 40,
            'speed': 150,
            'action_dice': 50,
            'p_defense': 90,
            'w_defense': 115,
        })
        super().__init__(*args, **kwargs)
        self.actions = [
            Action("Basic Precise Attack", 0, basic_precise_attack),
            Action("Riposte Attack", 2, riposte_attack),
        ]
