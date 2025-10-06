"""Space station for collaboration missions"""
import pygame
import math
from game.constants import *

class SpaceStation:
    def __init__(self, x, y, name="ISS"):
        self.x = x
        self.y = y
        self.name = name
        self.radius = 50
        self.rotation = 0
        self.docked = False
        self.crew_members = [
            "Commander Sarah Chen (USA)",
            "Flight Engineer Yuki Tanaka (Japan)", 
            "Mission Specialist Alex Petrov (Russia)",
            "Research Scientist Maria Santos (ESA)"
        ]
        self.experiments = [
            "Protein Crystal Growth",
            "Plant Growth in Microgravity",
            "Materials Science Research",
            "Earth Observation Study"
        ]
        
    def update(self, dt):
        """Update station rotation"""
        self.rotation += dt * 0.5  # Slow rotation
    
    def render(self, screen):
        """Render the space station"""
        # Main hub
        pygame.draw.circle(screen, (150, 150, 150), (int(self.x), int(self.y)), 25)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 25, 2)
        
        # Solar panels (rotating)
        panel_length = 40
        for angle_offset in [0, math.pi/2, math.pi, 3*math.pi/2]:
            angle = self.rotation + angle_offset
            start_x = self.x + math.cos(angle) * 30
            start_y = self.y + math.sin(angle) * 30
            end_x = self.x + math.cos(angle) * (30 + panel_length)
            end_y = self.y + math.sin(angle) * (30 + panel_length)
            
            # Solar panel
            pygame.draw.line(screen, BLUE, (start_x, start_y), (end_x, end_y), 8)
            pygame.draw.line(screen, CYAN, (start_x, start_y), (end_x, end_y), 4)
        
        # Station name
        font = pygame.font.Font(None, 24)
        name_text = font.render(self.name, True, WHITE)
        name_rect = name_text.get_rect(center=(self.x, self.y - 70))
        screen.blit(name_text, name_rect)
        
        # Docking indicator
        if self.docked:
            pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y - 35)), 5)
    
    def dock(self):
        """Dock with the space station"""
        self.docked = True
        return {
            'crew': self.crew_members,
            'experiments': self.experiments,
            'message': f"Successfully docked with {self.name}!"
        }
    
    def undock(self):
        """Undock from the space station"""
        self.docked = False