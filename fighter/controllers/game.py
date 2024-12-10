import pygame
import os
from ..constants import const as c


class Game:
    player_set = []
    enemy_set = []
    turn_order = []

    def get_team(self, entity):
        if entity in self.player_set:
            return self.player_set
        else:
            return self.enemy_set

    def get_entities(self):
        return self.player_set + self.enemy_set

    def get_turn_order(self):
        if not self.turn_order:
            self.turn_order = self.get_entities()
        self.turn_order.sort(key=lambda entity: entity.turnmeter, reverse=True)
        return self.turn_order

    def tick(self):
        entities = self.get_turn_order()
        if not entities or len(entities) == 0:
            return False
        if entities[0].turnmeter >= 1000:
            if entities[0] in self.player_set:
                return True, entities
            else:
                entities[0].take_turn(c.ACTION_1)
        else:
            for entity in entities:
                entity.tick_turnmeter()
            return False, entities

    def get_target(self, entity):
        if entity in self.player_set:
            return entity.ai(self.enemy_set)
        else:
            return entity.ai(self.player_set)


pygame.init()

CLOCK = pygame.time.Clock()
GAME = Game()

# Set up logo
path = os.path.join("assets", "blue.png")
logo = pygame.image.load(path)
pygame.display.set_icon(logo)
pygame.display.set_caption("Game")
