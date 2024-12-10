from .entities import Character
from .attacks import basic_attack, basic_magic_attack, basic_precise_attack
from ..controllers.hud import HUD


class Caster(Character):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions = [
            {
                "name": "Basic Magic Attack",
                "cooldown": 0,
                "action": basic_magic_attack,
            }
        ]
        self.cooldowns = {
            "Basic Magic Attack": 0,
        }


class Retaliator(Character):
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
        super().__init__(*args, **kwargs)
        self.actions = [
            {
                "name": "Basic Precise Attack",
                "cooldown": 0,
                "action": basic_precise_attack,
            }
        ]
        self.cooldowns = {
            "Basic Precise Attack": 0,
        }
