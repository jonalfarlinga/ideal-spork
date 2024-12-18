import pygame
import os
from ..constants import const as c


class Game:
    '''
    player_set: list of player entities
    enemy_set: list of enemy entities
    turn_order: list of entities in order of their turnmeter

    game_over(): check if the game is over
    get_team(entity): return the team of the entity
    get_entities(): return all entities
    get_turn_order(): return the turn order of the entities
    tick(): tick the game
    get_target(entity): return the target of the entity
    reset(): reset the game
    '''
    player_set = []
    enemy_set = []
    turn_order = []

    def game_over(self):
        player_lost = True
        enemy_lost = True
        for entity in self.player_set:
            if entity.resilience > 0:
                player_lost = False
                break
        for entity in self.enemy_set:
            if entity.resilience > 0:
                enemy_lost = False
                break
        return player_lost or enemy_lost

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

    def reset(self):
        self.player_set = []
        self.enemy_set = []
        self.turn_order = []


pygame.init()

CLOCK = pygame.time.Clock()
GAME = Game()

# Set up logo
path = os.path.join("assets", "blue.png")
logo = pygame.image.load(path)
pygame.display.set_icon(logo)
pygame.display.set_caption("Game")
