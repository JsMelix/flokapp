"""Base scene class for all game scenes"""
import pygame
from game.constants import *

class BaseScene:
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
    
    def on_enter(self):
        """Called when entering this scene"""
        pass
    
    def handle_event(self, event):
        """Handle pygame events"""
        pass
    
    def update(self, dt):
        """Update scene logic"""
        pass
    
    def render(self, screen):
        """Render scene to screen"""
        pass
    
    def draw_stars(self, screen):
        """Draw animated starfield background"""
        import random
        for _ in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            brightness = random.randint(100, 255)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(screen, color, (x, y), 1)