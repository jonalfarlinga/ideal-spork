import pygame
import os


class Game:
    player_set = []
    enemy_set = []

    def get_entities(self):
        return self.player_set + self.enemy_set

    def tick(self):
        entities = self.get_entities()
        entities.sort(key=lambda entity: entity.turnmeter, reverse=True)
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

# Set up logo
path = os.path.join("assets", "blue.png")
logo = pygame.image.load(path)
logo.set_colorkey(VIOLETGREY)
pygame.display.set_icon(logo)
pygame.display.set_caption("Game")
