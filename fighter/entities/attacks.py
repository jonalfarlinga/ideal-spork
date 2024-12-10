from random import choice
from ..controllers.hud import HUD
from ..controllers.game import GAME


def roll_attack_dice(attacker):
    attack_roll = {
        "P": 0,
        "A": 0,
        "W": 0,
    }
    for _ in range(attacker.action_dice):
        t = choice(["P", "A", "W"])
        attack_roll[t] += 1
    for t in attack_roll.keys():
        attack_roll[t] = attack_roll[t] * attacker.get_boost(t)
    return attack_roll


def basic_attack(attacker, target):
    attack_type = "P"
    if target:
        attack_roll = roll_attack_dice(attacker)
        damage = attack_roll[attack_type]
        HUD.log_message(
            f"{attacker} attacks {target} with {attack_roll}! "
            f"Attack type: {attack_type}."
        )
        HUD.log_message(
            f"    {attacker} deals {attack_roll[attack_type]} damage! "
        )
        target.hit(damage, attack_type, attacker)
        if target.resilience <= 0:
            attacker.target = None
    else:
        HUD.log_message(f"{attacker} has no target!")


def basic_magic_attack(attacker, target):
    attack_type = "W"
    if target:
        attack_roll = roll_attack_dice(attacker)
        damage = attack_roll[attack_type]
        HUD.log_message(
            f"{attacker.name} attacks {target.name} with {attack_roll}! "
            f"Attack type: {attack_type}."
        )
        HUD.log_message(
            f"    {attacker} deals {attack_roll[attack_type]} damage! "
        )
        target.hit(damage, attack_type, attacker)
        if target.resilience <= 0:
            attacker.target = None
    else:
        HUD.log_message(f"{attacker.name} has no target!")


def basic_precise_attack(attacker, target):
    attack_type = "A"
    if target:
        attack_roll = roll_attack_dice(attacker)
        damage = attack_roll[attack_type]
        HUD.log_message(
            f"{attacker.name} attacks {target.name} with {attack_roll}! "
            f"Attack type: {attack_type}."
        )
        HUD.log_message(
            f"    {attacker} deals {attack_roll[attack_type]} damage! "
        )
        target.hit(damage, attack_type, attacker)
        if target.resilience <= 0:
            attacker.target = None
    else:
        HUD.log_message(f"{attacker.name} has no target!")


def basic_wave_attack(attacker, target):
    if target is None:
        HUD.log_message(f"{attacker.name} has no target!")
        return
    target_team = GAME.get_team(target)
    for entity in target_team:
        if entity.resilience > 0:
            basic_attack(attacker, entity)
