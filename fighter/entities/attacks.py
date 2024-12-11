from random import choice
from ..controllers.hud import HUD
from ..controllers.game import GAME


# Every attack function takes two arguments: attacker and target.
# The attacker is the entity that is performing the action.
# The target is selected by the user.
def roll_attack_dice(attacker):
    attack_roll = {
        "P": 0,
        "A": 0,
        "W": 0,
    }
    for _ in range(attacker.action_dice):
        t = choice(["P", "A", "W"])
        attack_roll[t] += 1
    return attack_roll


def basic_attack(attacker, target):
    attack_type = "P"
    if target:
        attack_roll = roll_attack_dice(attacker)
        HUD.log_message(
            f"{attacker} attacks {target} with {attack_roll}! "
            f"Attack type: {attack_type}."
        )
        damage = attack_roll[attack_type] * attacker.get_boost(attack_type)
        HUD.log_message(f"    {attacker} deals {damage} damage! ")
        target.hit(damage, attack_type, attacker)
        if target.resilience <= 0:
            attacker.target = None
    else:
        HUD.log_message(f"{attacker} has no target!")


def basic_magic_attack(attacker, target):
    attack_type = "W"
    if target:
        attack_roll = roll_attack_dice(attacker)
        HUD.log_message(
            f"{attacker.name} attacks {target.name} with {attack_roll}! "
            f"Attack type: {attack_type}."
        )
        damage = attack_roll[attack_type] * attacker.get_boost(attack_type)
        HUD.log_message(f"    {attacker} deals {damage} damage! ")
        target.hit(damage, attack_type, attacker)
        if target.resilience <= 0:
            attacker.target = None
    else:
        HUD.log_message(f"{attacker.name} has no target!")


def basic_precise_attack(attacker, target):
    attack_type = "A"
    if target:
        attack_roll = roll_attack_dice(attacker)
        HUD.log_message(
            f"{attacker.name} attacks {target.name} with {attack_roll}! "
            f"Attack type: {attack_type}."
        )
        damage = attack_roll[attack_type] * attacker.get_boost(attack_type)
        HUD.log_message(f"    {attacker} deals {damage} damage! ")
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


def riposte_attack(attacker, target):
    if target is None:
        HUD.log_message(f"{attacker.name} has no target!")
        return
    attack_type = "A"
    attack_roll = roll_attack_dice(attacker)
    HUD.log_message(
        f"{attacker.name} attacks {target.name} with {attack_roll}! "
        f"Attack type: {attack_type}."
    )
    attacker.shield = max(attack_roll["W"] // 2, attacker.shield)
    HUD.log_message(f"    {attacker.name} gains {attacker.shield} shield!")
    damage = attack_roll[attack_type] * attacker.get_boost(attack_type)
    HUD.log_message(f"    {attacker} deals {damage} damage! ")
    target.hit(damage, attack_type, attacker)
    if target.resilience <= 0:
        attacker.target = None


def regenerate(attacker, _):
    attack_type = "W"
    attack_roll = roll_attack_dice(attacker)
    HUD.log_message(
        f"{attacker.name} heals self with {attack_roll}! "
        f"Roll type: {attack_type}."
    )
    heal = attack_roll[attack_type] * attacker.get_boost(attack_type) // 200
    heal = min(heal, attacker.max_resilience - attacker.resilience)
    HUD.log_message(f"    {attacker} heals {heal} health! ")
    attacker.resilience += heal


def fireball_attack(attacker, target):
    group = GAME.get_team(target)
    for entity in group:
        attack_type = "W"
        attack_roll = roll_attack_dice(attacker)
        HUD.log_message(
            f"{attacker.name} attacks {entity.name} with {attack_roll}! "
            f"Attack type: {attack_type}."
        )
        damage = (
            attack_roll[attack_type] * attacker.get_boost(attack_type) // 2
        )
        HUD.log_message(f"    {attacker} deals {damage} damage! ")
        entity.hit(damage, attack_type, attacker)
        if entity.resilience <= 0:
            attacker.target = None
