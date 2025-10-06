"""Asteroid entities for space hazards and resources"""
import pygame
import random
import math
from game.constants import *

class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(15, 35)
        self.speed = random.randint(20, 60)
        self.angle = random.uniform(0, 2 * math.pi)
        self.rotation = 0
        self.rotation_speed = random.uniform(-2, 2)
        
        # Asteroid properties
        self.mineral_type = random.choice(['Iron', 'Nickel', 'Platinum', 'Water Ice'])
        self.value = self.radius * 10
        self.scanned = False
        
        # Movement
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
    
    def update(self, dt):
        """Update asteroid position and rotation"""
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.rotation += self.rotation_speed * dt
        
        # Wrap around screen
        if self.x < -self.radius:
            self.x = SCREEN_WIDTH + self.radius
        elif self.x > SCREEN_WIDTH + self.radius:
            self.x = -self.radius
            
        if self.y < -self.radius:
            self.y = SCREEN_HEIGHT + self.radius
        elif self.y > SCREEN_HEIGHT + self.radius:
            self.y = -self.radius
    
    def render(self, screen):
        """Render the asteroid"""
        # Draw asteroid body
        color = (100, 80, 60) if not self.scanned else (120, 100, 80)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        
        # Draw surface details
        for i in range(3):
            offset_x = math.cos(self.rotation + i * 2) * (self.radius * 0.3)
            offset_y = math.sin(self.rotation + i * 2) * (self.radius * 0.3)
            detail_x = self.x + offset_x
            detail_y = self.y + offset_y
            pygame.draw.circle(screen, (80, 60, 40), (int(detail_x), int(detail_y)), 3)
        
        # Draw scan indicator if scanned
        if self.scanned:
            pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), self.radius + 5, 2)
            
            # Show mineral type
            font = pygame.font.Font(None, 20)
            text = font.render(self.mineral_type, True, WHITE)
            text_rect = text.get_rect(center=(self.x, self.y - self.radius - 15))
            screen.blit(text, text_rect)
    
    def scan(self):
        """Scan asteroid for resources"""
        if not self.scanned:
            self.scanned = True
            return {
                'mineral': self.mineral_type,
                'value': self.value,
                'size': 'Large' if self.radius > 25 else 'Small'
            }
        return None