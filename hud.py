import pygame


class Logbox:
    def __init__(self, hud):
        self.screen = hud
        self.font = pygame.font.SysFont("arialblack", 12)
        self.content = []

    def draw(self, index=0):
        self.screen.fill((50, 50, 50))
        if len(self.content) < 11:
            index = 0
        start = max(0, len(self.content) - 10 - index)
        end = min(len(self.content) - index, len(self.content))
        for i, line in enumerate(self.content[start:end]):
            text = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text, (5, 5 + i * 12))

    def add_message(self, message):
        self.content.append(message)

    def clear(self):
        self.content = []


class HUDBox:
    def __init__(self):
        self.logbox_screen = pygame.Surface((600, 140))
        self.logbox = Logbox(self.logbox_screen)
        self.order_screen = pygame.Surface((100, 400))
        self.orderbox = Logbox(self.order_screen)
        self.count = 0
        self.index = 0

    def draw(self, screen):
        self.logbox.draw(self.index)
        self.orderbox.draw(len(self.orderbox.content))
        screen.blit(self.logbox_screen, (50, 450))
        screen.blit(self.order_screen, (675, 100))

    def log_message(self, message):
        self.count += 1
        if self.index:
            self.index += 1
        self.logbox.add_message(f"{self.count}: {message}")

    def set_order(self, entities):
        messages = []
        for entity in entities:
            messages.append(f"{entity.turnmeter}: {entity.name}")
        self.clear_order()
        for message in messages:
            self.orderbox.add_message(message)

    def clear_log(self):
        self.logbox.clear()

    def scroll_log(self, up):
        if up:
            self.index = max(self.index - 1, 0)
            self.index = min(self.index, self.count)
        else:
            self.index = min(self.index + 1, self.count - 10)

    def clear_order(self):
        self.orderbox.clear()


HUD = HUDBox()
