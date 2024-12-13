import pygame
from ..constants import color
from ..constants import const as c
from .buttons import Buttons
from .setup import setup_teams


def game_menu(screen):
    while True:
        rect = pygame.Rect((280, 300), (200, 60))
        rect = pygame.draw.rect(screen, color.GREY, rect)
        menu_buttons = Buttons()
        menu_buttons.add_button("Start Game", (310, 320), (160, 40))
        menu_buttons.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                selection = menu_buttons.is_clicked(event)
                match selection:
                    case "Start Game":
                        setup_teams()
                        return c.RUN_GAME


def win_menu(screen):
    while True:
        rect = pygame.Rect((280, 300), (200, 60))
        rect = pygame.draw.rect(screen, color.GREY, rect)
        menu_buttons = Buttons()
        menu_buttons.add_button("Play Again!", (310, 320), (160, 40))
        menu_buttons.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            selection = menu_buttons.is_clicked(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                match selection:
                    case "Play Again!":
                        return


def team_menu(screen):
    pass
