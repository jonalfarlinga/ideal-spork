import pygame

# Set up fonts
HEADER = pygame.font.Font("freesansbold.ttf", 20)
TEXT = pygame.font.Font("freesansbold.ttf", 12)
CAPTION = pygame.font.Font("freesansbold.ttf", 8)


def write_headline(screen, content, position):
    headline = HEADER.render(content, True, (255, 255, 255))
    screen.blit(headline, position)


def write_text(screen, content, position):
    text = TEXT.render(content, True, (255, 255, 255))
    screen.blit(text, position)


def write_caption(screen, content, position):
    caption = CAPTION.render(content, True, (255, 255, 255))
    screen.blit(caption, position)
