from random import randint
import pygame
from .ai import target_basic
from .attacks import basic_attack, basic_wave_attack
from ..controllers.screen_writer import write_text, write_headline
from ..controllers.hud import HUD
from ..controllers.game import GAME
from ..constants import color


class Character:
    def __init__(
        self,
        name,
        sprite,
        position,
        resilience,
        action_dice,
        speed,
        p_defense=100,
        a_defense=100,
        w_defense=100,
        p_boost=100,
        a_boost=100,
        w_boost=100,
        ai=target_basic,
    ):
        self.name = name
        self.resilience = resilience
        self.max_resilience = resilience
        self.action_dice = action_dice
        self.speed = speed
        self.p_defense = p_defense
        self.a_defense = a_defense
        self.w_defense = w_defense
        self.p_boost = p_boost
        self.a_boost = a_boost
        self.w_boost = w_boost
        self.ai = ai
        self.sprite = sprite
        self.x, self.y = position
        self.turnmeter = 0
        self.actions = [
            {
                "name": "Basic Attack",
                "cooldown": 0,
                "action": basic_attack,
            }
        ]
        self.cooldowns = {
            "Basic Attack": 0,
        }
        self.active = False

    def __str__(self):
        return self.name

    def draw(self, screen, your_turn=False):
        border = color.GOLD if your_turn else color.GREY
        pygame.draw.rect(
            screen,
            border,
            pygame.Rect(
                self.x - 2,
                self.y - 2,
                self.sprite.get_width() + 4,
                self.sprite.get_height() + 4,
            ),
        )
        image = self.sprite
        if self.resilience <= 0:
            image = pygame.transform.grayscale(image)
        screen.blit(image, (self.x, self.y))

        res_bar = pygame.Rect(self.x - 20, self.y - 1, 7, 52)
        pygame.draw.rect(screen, color.GREY, res_bar)
        cur_res_bar = int(self.resilience / self.max_resilience * 50)
        res_bar = pygame.Rect(
            self.x - 19, self.y + 50 - cur_res_bar, 5, cur_res_bar
        )
        pygame.draw.rect(screen, color.RED, res_bar)

        self.draw_headlines(screen)
        self.draw_stats(screen)

    def draw_headlines(self, screen):
        write_headline(screen, self.name, (self.x + 25, self.y - 25))
        write_headline(
            screen,
            str(self.resilience),
            (self.x - 30, self.y + 52),
        )

    def draw_stats(self, screen):
        write_text(
            screen,
            f"Power: {self.p_boost} Defense: {self.p_defense}",
            (self.x + self.sprite.get_width() + 10, self.y + 20),
        )
        write_text(
            screen,
            f"Accuracy: {self.a_boost} Defense: {self.a_defense}",
            (self.x + self.sprite.get_width() + 10, self.y + 35),
        )
        write_text(
            screen,
            f"Will: {self.w_boost} Defense: {self.w_defense}",
            (self.x + self.sprite.get_width() + 10, self.y + 50),
        )

    # Handle turns and turn order
    def tick_turnmeter(self):
        if self.resilience > 0:
            self.turnmeter += self.speed
            return self.turnmeter

    def take_turn(self, action):
        self.active = True
        if self.resilience > 0:
            if action >= len(self.actions):
                self.active = False
                return
            selected_action = self.actions[action]["action"]
            selected_action(self, GAME.get_target(self))
        self.turnmeter = 0
        self.active = False

    # receive damage
    def defend_against(self, damage, type):
        defense = (
            self.p_defense
            if type == "P"
            else self.a_defense if type == "A" else self.w_defense
        )
        return int(damage / defense)

    # empty argument is for compatibility with other character types
    # expect the attacker's Character object
    def hit(self, damage, attack_type, _):
        damage = self.defend_against(damage, attack_type)
        if not damage:
            HUD.log_message(f"    {self.name} takes no damage!")
        else:
            self.take_damage(damage)

    def take_damage(self, damage):
        HUD.log_message(f"    {self.name} loses {damage} resilience!")
        self.resilience -= damage

        if self.resilience <= 0:
            self.turnmeter = 0
            HUD.log_message(f"{self.name} is defeated!")

    # getters and setters
    def get_boost(self, type):
        return (
            self.p_boost
            if type == "P"
            else self.a_boost if type == "A" else self.w_boost
        )


class Beast(Character):
    def __init__(
        self,
        name,
        sprite,
        position,
        resilience=60,
        action_dice=60,
        speed=90,
        p_defense=120,
        a_defense=120,
        w_defense=120,
        p_boost=110,
        a_boost=110,
        w_boost=110,
        ai=target_basic,
    ):
        super().__init__(
            name,
            sprite,
            position,
            resilience,
            action_dice,
            speed,
            p_defense,
            a_defense,
            w_defense,
            p_boost,
            a_boost,
            w_boost,
            ai,
        )
        self.actions = [
            {
                "name": "Basic Wave Attack",
                "cooldown": 0,
                "action": basic_wave_attack,
            }
        ]
        self.cooldowns = {
            "Basic Wave Attack": 0,
        }

    def draw_stats(self, screen):
        write_text(
            screen,
            f"Power: {self.p_boost} Defense: {self.p_defense}",
            (self.x + 10, self.y + self.sprite.get_height() + 20),
        )
        write_text(
            screen,
            f"Accuracy: {self.a_boost} Defense: {self.a_defense}",
            (self.x + 10, self.y + self.sprite.get_height() + 35),
        )
        write_text(
            screen,
            f"Will: {self.w_boost} Defense: {self.w_defense}",
            (self.x + 10, self.y + self.sprite.get_height() + 50),
        )

    def take_damage(self, damage):
        sys_damage = {
            "resilience": 0,
            "p_boost": 0,
            "p_defense": 0,
            "a_boost": 0,
            "a_defense": 0,
            "w_boost": 0,
            "w_defense": 0,
        }
        for _ in range(damage):
            target = randint(1, 6)
            match target:
                case 1:
                    sys_damage["w_defense"] = min(
                        sys_damage["w_defense"] + 1, self.w_defense - 1
                    )
                case 2:
                    sys_damage["w_boost"] = min(
                        sys_damage["w_boost"] + 1, self.w_boost - 1
                    )
                    sys_damage["resilience"] += 1
                case 3:
                    sys_damage["a_defense"] = min(
                        sys_damage["a_defense"] + 1, self.a_defense - 1
                    )
                case 4:
                    sys_damage["a_boost"] = min(
                        sys_damage["a_boost"] + 1, self.a_boost - 1
                    )
                    sys_damage["resilience"] += 1
                case 5:
                    sys_damage["p_defense"] = min(
                        sys_damage["p_defense"] + 1, self.p_defense - 1
                    )
                case 6:
                    sys_damage["p_boost"] = min(
                        sys_damage["p_boost"] + 1, self.p_boost - 1
                    )
                    sys_damage["resilience"] += 1
        HUD.log_message(
            f"    {self.name} loses {sys_damage['resilience']} resilience!"
        )
        HUD.log_message(
            f"    {self.name} Systems damage- "
            f"P+: {sys_damage['p_boost']} PD: {sys_damage['p_defense']} "
            f"A+: {sys_damage['a_boost']} AD: {sys_damage['a_defense']} "
            f"W+: {sys_damage['w_boost']} AD: {sys_damage['w_defense']} "
        )
        self.resilience -= sys_damage["resilience"]
        self.p_boost -= sys_damage["p_boost"]
        self.p_defense -= sys_damage["p_defense"]
        self.a_boost -= sys_damage["a_boost"]
        self.a_defense -= sys_damage["a_defense"]
        self.w_boost -= sys_damage["w_boost"]
        self.w_defense -= sys_damage["w_defense"]
        if self.resilience <= 0:
            self.turnmeter = 0
            HUD.log_message(f"{self.name} is defeated!")
