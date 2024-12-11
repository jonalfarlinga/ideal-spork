# Set up Constants
class Const:
    # Action positions
    ACTION_1 = 0
    ACTION_2 = 1
    ACTION_3 = 2
    ACTION_4 = 3
    # Target positions
    TARGET_1 = 0
    TARGET_2 = 1
    TARGET_3 = 2
    TARGET_4 = 3
    # Character highlights
    ACTIVE = (255, 215, 0)
    INACTIVE = (128, 128, 128)
    TARGET = (255, 0, 0)

    # Game commands
    RUN_GAME = 0

    # App constants
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 800
    BORDER = 50
    PLAYER_COLUMN = 25
    ENEMY_COLUMN = 325
    TOP_PADDING = 90
    FPS = 30


# Set up colors
class Color:
    WHITE = (255, 255, 255)
    VIOLETGREY = (28, 36, 59)
    BLACK = (0, 0, 0)
    GREY = (128, 128, 128)
    RED = (255, 0, 0)
    GOLD = (255, 215, 0)


const = Const()
color = Color()
