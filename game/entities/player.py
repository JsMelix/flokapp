"""Player spacecraft entity"""
import pygame
import math
from game.constants import *

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 200
        self.radius = 15
        self.angle = 0
        self.thrust = False
        
        # Movement keys
        self.keys = {
            'up': False,
            'down': False, 
            'left': False,
            'right': False
        }
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.keys['up'] = True
            elif event.key == pygame.K_s:
                self.keys['down'] = True
            elif event.key == pygame.K_a:
                self.keys['left'] = True
            elif event.key == pygame.K_d:
                self.keys['right'] = True
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.keys['up'] = False
            elif event.key == pygame.K_s:
                self.keys['down'] = False
            elif event.key == pygame.K_a:
                self.keys['left'] = False
            elif event.key == pygame.K_d:
                self.keys['right'] = False
    
    def update(self, dt):
        """Update player position and state"""
        # Handle movement
        dx = 0
        dy = 0
        
        if self.keys['left']:
            dx -= self.speed * dt
        if self.keys['right']:
            dx += self.speed * dt
        if self.keys['up']:
            dy -= self.speed * dt
        if self.keys['down']:
            dy += self.speed * dt
        
        # Update position with screen wrapping
        self.x = (self.x + dx) % SCREEN_WIDTH
        self.y = (self.y + dy) % SCREEN_HEIGHT
        
        # Update angle for rotation effect
        if dx != 0 or dy != 0:
            self.angle = math.atan2(dy, dx)
            self.thrust = True
        else:
            self.thrust = False
    
    def check_collision(self, other):
        """Check collision with another entity"""
        distance = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        return distance < (self.radius + other.radius)
    
    def render(self, screen):
        """Render the player spacecraft"""
        # Draw spacecraft body
        pygame.draw.circle(screen, CYAN, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius, 2)
        
        # Draw direction indicator
        end_x = self.x + math.cos(self.angle) * (self.radius + 10)
        end_y = self.y + math.sin(self.angle) * (self.radius + 10)
        pygame.draw.line(screen, YELLOW, (self.x, self.y), (end_x, end_y), 3)
        
        # Draw thrust effect
        if self.thrust:
            thrust_x = self.x - math.cos(self.angle) * (self.radius + 5)
            thrust_y = self.y - math.sin(self.angle) * (self.radius + 5)
            pygame.draw.circle(screen, RED, (int(thrust_x), int(thrust_y)), 5)