from entities import Character
from random import choice
from hud import HUD


class Caster(Character):
    def __init__(
        self,
        name,
        sprite,
        position,
        resilience,
        action_dice,
        speed,
        def_p=0,
        def_a=0,
        def_w=0,
        p_bst=0,
        a_bst=0,
        w_bst=0,
        ai=None,
    ):
        super().__init__(
            name,
            sprite,
            position,
            resilience,
            action_dice,
            speed,
            def_p,
            def_a,
            def_w,
            p_bst,
            a_bst,
            w_bst,
        )
        if ai:
            self.ai = ai

    def basic_attack(self, target):
        attack_type = "W"
        if target:
            attack = {"P": self.p_bst, "A": self.a_bst, "W": self.w_bst}
            for _ in range(self.action_dice):
                t = choice(["P", "A", "W"])
                attack[t] += 1
            damage = attack[attack_type]
            HUD.log_message(
                f"{self.name} attacks {target.name} with {attack}! "
                f"Attack type: {attack_type}."
            )
            HUD.log_message(f"    {self} deals {attack[attack_type]} damage! ")
            target.hit(damage, attack_type, self)
            if target.resilience <= 0:
                self.target = None
        else:
            HUD.log_message(f"{self.name} has no target!")


class Retaliator(Character):
    def __init__(
        self,
        name,
        sprite,
        position,
        resilience,
        action_dice,
        speed,
        def_p=0,
        def_a=0,
        def_w=0,
        p_bst=0,
        a_bst=0,
        w_bst=0,
        ai=None,
    ):
        super().__init__(
            name,
            sprite,
            position,
            resilience,
            action_dice,
            speed,
            def_p,
            def_a,
            def_w,
            p_bst,
            a_bst,
            w_bst,
        )
        if ai:
            self.ai = ai

    def hit(self, damage, attack_type, attacker):
        damage = self.defend(damage, attack_type)
        if not damage:
            HUD.log_message(f"    {self.name} takes 0 damage!")
        else:
            self.take_damage(damage)
        if self.resilience > 0 and attacker.turnmeter > self.turnmeter:
            HUD.log_message(f"{self} retaliates against {attacker}!")
            self.basic_attack(attacker)
