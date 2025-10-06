"""Satellite entities for communication and observation missions"""
import pygame
import math
from game.constants import *

class Satellite:
    def __init__(self, x, y, satellite_type="communication"):
        self.x = x
        self.y = y
        self.type = satellite_type
        self.radius = 20
        self.orbit_radius = 60
        self.orbit_angle = 0
        self.orbit_speed = 1.5
        self.active = True
        self.data_collected = 0
        
        # Satellite types and their functions
        self.satellite_data = {
            'communication': {
                'name': 'CommSat-1',
                'function': 'Enables communication between Earth and spacecraft',
                'color': CYAN,
                'data_type': 'Communication Signals'
            },
            'weather': {
                'name': 'WeatherSat-2',
                'function': 'Monitors Earth\'s weather patterns and climate',
                'color': BLUE,
                'data_type': 'Weather Data'
            },
            'navigation': {
                'name': 'NavSat-GPS',
                'function': 'Provides precise positioning for spacecraft navigation',
                'color': GREEN,
                'data_type': 'Navigation Data'
            },
            'scientific': {
                'name': 'SciSat-Hubble',
                'function': 'Observes distant galaxies and cosmic phenomena',
                'color': PURPLE,
                'data_type': 'Astronomical Data'
            }
        }
        
        self.info = self.satellite_data.get(satellite_type, self.satellite_data['communication'])
    
    def update(self, dt):
        """Update satellite orbital position"""
        if self.active:
            self.orbit_angle += self.orbit_speed * dt
            # Collect data over time
            self.data_collected += dt * 10
    
    def get_orbital_position(self, center_x, center_y):
        """Calculate current orbital position around a center point"""
        orbit_x = center_x + math.cos(self.orbit_angle) * self.orbit_radius
        orbit_y = center_y + math.sin(self.orbit_angle) * self.orbit_radius
        return orbit_x, orbit_y
    
    def render(self, screen, center_x=None, center_y=None):
        """Render the satellite"""
        if center_x is not None and center_y is not None:
            # Orbiting satellite
            self.x, self.y = self.get_orbital_position(center_x, center_y)
            
            # Draw orbit path
            pygame.draw.circle(screen, (100, 100, 100), (int(center_x), int(center_y)), self.orbit_radius, 1)
        
        # Draw satellite body
        color = self.info['color'] if self.active else (100, 100, 100)
        pygame.draw.rect(screen, color, (int(self.x - 8), int(self.y - 6), 16, 12))
        pygame.draw.rect(screen, WHITE, (int(self.x - 8), int(self.y - 6), 16, 12), 2)
        
        # Draw solar panels
        pygame.draw.rect(screen, BLUE, (int(self.x - 12), int(self.y - 3), 6, 6))
        pygame.draw.rect(screen, BLUE, (int(self.x + 6), int(self.y - 3), 6, 6))
        
        # Draw communication dish/antenna
        if self.type == 'communication':
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y - 10)), 4, 1)
        elif self.type == 'scientific':
            # Telescope
            pygame.draw.line(screen, WHITE, (self.x, self.y - 8), (self.x, self.y - 15), 2)
        
        # Status indicator
        status_color = GREEN if self.active else RED
        pygame.draw.circle(screen, status_color, (int(self.x + 10), int(self.y - 8)), 3)
    
    def interact(self):
        """Interact with satellite to collect data"""
        if self.active and self.data_collected > 0:
            collected = min(self.data_collected, 100)
            self.data_collected = max(0, self.data_collected - collected)
            return {
                'name': self.info['name'],
                'data_type': self.info['data_type'],
                'amount': collected,
                'function': self.info['function']
            }
        return None