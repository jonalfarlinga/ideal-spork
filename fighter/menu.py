import pygame
from .controllers.screen_writer import write_headline
from .constants import color
from .constants import const as c


def game_menu(screen):
    while True:
        rect = pygame.Rect((280, 300), (200, 60))
        rect = pygame.draw.rect(screen, color.GREY, rect)
        write_headline(screen, "Fighter!", (300, 320))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return c.RUN_GAME


def win_menu(screen):
    while True:
        rect = pygame.Rect((280, 300), (200, 60))
        rect = pygame.draw.rect(screen, color.GREY, rect)
        write_headline(screen, "Game Over!", (300, 320))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
