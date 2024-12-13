import pygame
from ..controllers.screen_writer import write_headline
from ..constants import color


class Button:
    def __init__(self, text, position, size):
        self.text = text
        self.position = position
        self.size = size
        self.rect = pygame.Rect(position, size)

    def draw(self, screen):
        pygame.draw.rect(screen, color.GREY, self.rect)
        write_headline(screen, self.text, self.position)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def is_hovered(self, event):
        if self.rect.collidepoint(event.pos):
            return True
        return False


class Buttons:
    def __init__(self):
        self.buttons = []

    def add_button(self, text, position, size):
        self.buttons.append(Button(text, position, size))

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def is_clicked(self, event):
        for button in self.buttons:
            if button.is_clicked(event):
                return button.text
        return None

    def is_hovered(self, event):
        for button in self.buttons:
            if button.is_hovered(event):
                return button.text
        return None
