import pygame
from ..constants import const as c


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
    '''
    logbox: An object that tracks and displays game logs
    logbox_screen: the surface for the logbox
    orderbox: An object that tracks and displays the turn order
    order_screen: the surface for the orderbox
    action_box: An object that displays actions available to the current entity
    action_screen: the surface for the actionbox
    count: the number of messages in the logbox
    index: the index of the most recent message displayed

    draw(): draws the HUD to the screen
    log_message(message): adds a message to the logbox
    clear_log(): clears the logbox
    scroll_log(up): scrolls the logbox up or down
    set_order(entities): sets the orderbox to the entities
    clear_order(): clears the orderbox
    '''
    def __init__(self):
        self.logbox_screen = pygame.Surface((550, 140))
        self.logbox = Logbox(self.logbox_screen)
        self.order_screen = pygame.Surface((200, 150))
        self.orderbox = Logbox(self.order_screen)
        self.action_screen = pygame.Surface((200, 250))
        self.action_box = Logbox(self.action_screen)
        self.count = 0
        # index is the count back from most recent message to last displayed
        self.index = 0

    def draw(self, screen):
        self.logbox.draw(self.index)
        self.orderbox.draw(0)
        self.action_box.draw(0)
        screen.blit(self.logbox_screen, (
            c.BORDER + 50, c.SCREEN_HEIGHT - c.BORDER - 150))
        screen.blit(self.order_screen, (
            c.SCREEN_WIDTH - c.BORDER - 225, c.BORDER + 10))
        screen.blit(self.action_screen, (
            c.SCREEN_WIDTH - c.BORDER - 225, c.BORDER + 180))

    def log_message(self, message):
        self.count += 1
        if self.index:
            self.index += 1
        self.logbox.add_message(f"{self.count}: {message}")

    def clear_log(self):
        self.logbox.clear()

    def scroll_log(self, up):
        if up:
            self.index = min(self.index + 1, self.count - 10)
        else:
            self.index = max(self.index - 1, 0)
            self.index = min(self.index, self.count)

    def set_order(self, entities):
        messages = []
        for entity in entities:
            messages.append(f"{entity.turnmeter}: {entity.name}")
        self.clear_order()
        for message in messages:
            self.orderbox.add_message(message)

    def clear_order(self):
        self.orderbox.clear()

    def set_actions(self, entity):
        self.clear_actions()
        for i, action in enumerate(entity.actions):
            self.action_box.add_message(
                f"{i+1}: {action.name} - CD: "
                f"{action.cur_cd}/{action.cooldown}"
            )

    def clear_actions(self):
        self.action_box.clear()


HUD = HUDBox()
