"""Planet entity for exploration"""
import pygame
import math
from game.constants import *

class Planet:
    def __init__(self, x, y, name, color):
        self.x = x
        self.y = y
        self.name = name
        self.color = color
        self.radius = 40
        self.visited = False
        self.animation_time = 0
        
        # Educational data (could be loaded from NASA APIs)
        self.facts = {
            'Earth': 'Our home planet, 71% covered by water',
            'Mars': 'The Red Planet, potential for human colonization',
            'Moon': 'Earth\'s natural satellite, first human landing 1969',
            'Jupiter': 'Largest planet, has over 80 moons'
        }
    
    def update(self, dt):
        """Update planet animation"""
        self.animation_time += dt
    
    def render(self, screen):
        """Render the planet"""
        # Pulsing effect for unvisited planets
        pulse = 1.0
        if not self.visited:
            pulse = 1.0 + 0.1 * math.sin(self.animation_time * 3)
        
        current_radius = int(self.radius * pulse)
        
        # Draw planet
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), current_radius)
        
        # Draw atmosphere glow
        glow_color = tuple(min(255, c + 50) for c in self.color)
        pygame.draw.circle(screen, glow_color, (int(self.x), int(self.y)), current_radius + 5, 2)
        
        # Draw name
        font = pygame.font.Font(None, 24)
        name_text = font.render(self.name, True, WHITE)
        name_rect = name_text.get_rect(center=(self.x, self.y - self.radius - 20))
        screen.blit(name_text, name_rect)
        
        # Draw visited indicator
        if self.visited:
            pygame.draw.circle(screen, GREEN, (int(self.x + self.radius - 10), int(self.y - self.radius + 10)), 5)
    
    def get_fact(self):
        """Get educational fact about this planet"""
        return self.facts.get(self.name, "An interesting celestial body to explore!")