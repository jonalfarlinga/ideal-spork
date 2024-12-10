import pygame
import os


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
            return True, entities
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

FPS = 30
CLOCK = pygame.time.Clock()
GAME = Game()

# Set up colors
VIOLETGREY = (28, 36, 59)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GOLD = (255, 215, 0)

# Set up logo
path = os.path.join("assets", "blue.png")
logo = pygame.image.load(path)
pygame.display.set_icon(logo)
pygame.display.set_caption("Game")

# Set up Constants
ACTION_1 = 0
ACTION_2 = 1
ACTION_3 = 2
ACTION_4 = 3
