import ai
import pygame
from screen_writer import write_text, write_headline
from random import choice, randint
from hud import HUD


class Character:
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
        ai=ai.target_basic,
    ):
        self.name = name
        self.resilience = resilience
        self.action_dice = action_dice
        self.speed = speed
        self.def_p = def_p
        self.def_a = def_a
        self.def_w = def_w
        self.p_bst = p_bst
        self.a_bst = a_bst
        self.w_bst = w_bst
        self.ai = ai
        self.sprite = sprite
        self.x, self.y = position
        self.turnmeter = 0

    def __str__(self):
        return self.name

    def draw(self, screen):
        image = self.sprite
        if self.resilience <= 0:
            image = pygame.transform.grayscale(image)
        screen.blit(image, (self.x, self.y))
        write_headline(screen, self.name, (self.x + 25, self.y - 25))
        write_text(
            screen,
            f"Resilience: {self.resilience}",
            (self.x + self.sprite.get_width() + 10, self.y + 5),
        )
        write_text(
            screen,
            f"Power: {self.p_bst} Defense: {self.def_p}",
            (self.x + self.sprite.get_width() + 10, self.y + 20),
        )
        write_text(
            screen,
            f"Accuracy: {self.a_bst} Defense: {self.def_a}",
            (self.x + self.sprite.get_width() + 10, self.y + 35),
        )
        write_text(
            screen,
            f"Will: {self.w_bst} Defense: {self.def_w}",
            (self.x + self.sprite.get_width() + 10, self.y + 50),
        )

    # Handle turns and turn order
    def tick_turnmeter(self):
        if self.resilience > 0:
            self.turnmeter += self.speed
            return self.turnmeter

    def take_turn(self, game):
        self.turnmeter = 0
        if self.resilience > 0:
            return self.basic_attack(game.get_target(self))

    # handle attacks
    def basic_attack(self, target):
        attack_type = "P"
        if target:
            attack = {"P": self.p_bst, "A": self.a_bst, "W": self.w_bst}
            for _ in range(self.action_dice):
                t = choice(["P", "A", "W"])
                attack[t] += 1
            damage = attack[attack_type]
            HUD.log_message(
                f"{self} attacks {target} with {attack}! "
                f"Attack type: {attack_type}."
            )
            HUD.log_message(f"    {self} deals {attack[attack_type]} damage! ")
            target.hit(damage, attack_type)
            if target.resilience <= 0:
                self.target = None
        else:
            HUD.log_message(f"{self} has no target!")

    # recieve damage
    def defend(self, damage, type):
        defense = (
            self.def_p if type == "P"
            else self.def_a if type == "A"
            else self.def_w
        )
        return max(damage - defense, 0)

    def hit(self, damage, attack_type):
        damage = self.defend(damage, attack_type)
        if not damage:
            HUD.log_message(f"    {self.name} takes 0 damage!")
        else:
            self.take_damage(damage)

    def take_damage(self, damage):
        HUD.log_message(f"    {self.name} takes {damage} damage!")
        self.resilience -= damage

        if self.resilience <= 0:
            self.turnmeter = 0
            HUD.log_message(f"{self.name} is defeated!")


class Beast(Character):
    def __init__(
        self,
        name,
        sprite,
        position,
        resilience=6,
        action_dice=6,
        speed=6,
        def_p=2,
        def_a=2,
        def_w=2,
        p_bst=1,
        a_bst=1,
        w_bst=1,
        ai=ai.target_basic,
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
            ai,
        )

    def take_damage(self, damage):
        for _ in range(damage):
            target = randint(1, 6)
            match target:
                case 1:
                    self.def_w = max(self.def_w - 1, 0)
                    HUD.log_message(f"    {self.name} loses 1 W defense!")
                case 2:
                    self.a_bst = max(self.w_bst - 1, 0)
                    self.resilience -= 1
                    HUD.log_message(
                        f"    {self.name} loses 1 W boost" " and 1 Resilience!"
                    )
                case 3:
                    self.def_a = max(self.def_a - 1, 0)
                    HUD.log_message(f"    {self.name} loses 1 A defense!")
                case 4:
                    self.p_bst = max(self.p_bst - 1, 0)
                    self.resilience -= 1
                    HUD.log_message(
                        f"    {self.name} loses 1 A boost" " and 1 Resilience!"
                    )
                case 5:
                    self.def_p = max(self.def_p - 1, 0)
                    HUD.log_message(f"    {self.name} loses 1 P defense!")
                case 6:
                    self.p_bst = max(self.p_bst - 1, 0)
                    self.resilience -= 1
                    HUD.log_message(
                        f"    {self.name} loses 1 P boost" " and 1 Resilience!"
                    )
        if self.resilience <= 0:
            self.turnmeter = 0
            HUD.log_message(f"{self.name} is defeated!")