"""Game constants for Flokapp"""

# Screen dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors (retro space theme)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 200)
GREEN = (0, 200, 100)
RED = (200, 50, 50)
YELLOW = (255, 255, 0)
PURPLE = (150, 0, 200)
CYAN = (0, 255, 255)

# Space colors
SPACE_BLUE = (10, 20, 40)
STAR_WHITE = (240, 240, 255)
PLANET_COLORS = {
    'earth': (100, 150, 255),
    'mars': (200, 100, 50),
    'moon': (200, 200, 200),
    'jupiter': (255, 200, 100)
}

# Game states
MENU = 'menu'
PLAYING = 'playing'
MISSION_SELECT = 'mission_select'
PAUSE = 'pause'
GAME_OVER = 'game_over'

# Mission types
EXPLORATION = 'exploration'
RESEARCH = 'research'
COLLABORATION = 'collaboration'
PROBLEM_SOLVING = 'problem_solving'