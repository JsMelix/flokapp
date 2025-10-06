"""Rocket launch simulation for mission deployment"""
import pygame
import math
from game.constants import *

class Rocket:
    def __init__(self, x, y, mission_type="exploration"):
        self.x = x
        self.y = y
        self.start_y = y
        self.width = 20
        self.height = 60
        self.velocity_y = 0
        self.acceleration = -200  # Upward acceleration
        self.fuel = 100
        self.fuel_consumption = 15  # Fuel per second
        self.launched = False
        self.mission_type = mission_type
        self.stage = 1  # Rocket stages (1, 2, 3)
        self.max_stages = 3
        
        # Mission destinations
        self.destinations = {
            'exploration': {'name': 'Mars', 'distance': 225000000, 'color': PLANET_COLORS['mars']},
            'research': {'name': 'Deep Space', 'distance': 1000000000, 'color': PURPLE},
            'collaboration': {'name': 'ISS', 'distance': 400, 'color': CYAN},
            'problem_solving': {'name': 'Asteroid Belt', 'distance': 550000000, 'color': (150, 150, 150)}
        }
        
        self.destination = self.destinations.get(mission_type, self.destinations['exploration'])
        self.distance_traveled = 0
        
        # Visual effects
        self.thrust_particles = []
        self.stage_separation_time = 0
    
    def launch(self):
        """Launch the rocket"""
        if not self.launched and self.fuel > 0:
            self.launched = True
    
    def update(self, dt):
        """Update rocket physics and flight"""
        if self.launched and self.fuel > 0:
            # Apply thrust
            self.velocity_y += self.acceleration * dt
            self.y += self.velocity_y * dt
            
            # Consume fuel
            self.fuel -= self.fuel_consumption * dt
            self.fuel = max(0, self.fuel)
            
            # Calculate distance traveled (simplified)
            if self.velocity_y < 0:  # Moving upward
                self.distance_traveled += abs(self.velocity_y) * dt * 1000  # Scale for visualization
            
            # Stage separation
            if self.fuel <= 66 and self.stage == 1:
                self.stage = 2
                self.stage_separation_time = 1.0  # Visual effect duration
            elif self.fuel <= 33 and self.stage == 2:
                self.stage = 3
                self.stage_separation_time = 1.0
            
            # Update stage separation effect
            if self.stage_separation_time > 0:
                self.stage_separation_time -= dt
            
            # Create thrust particles
            if len(self.thrust_particles) < 20:
                particle = {
                    'x': self.x + random.randint(-5, 5),
                    'y': self.y + self.height // 2,
                    'velocity_y': random.randint(50, 150),
                    'life': random.uniform(0.5, 1.5),
                    'color': random.choice([RED, YELLOW, (255, 100, 0)])
                }
                self.thrust_particles.append(particle)
            
            # Update particles
            for particle in self.thrust_particles[:]:
                particle['y'] += particle['velocity_y'] * dt
                particle['life'] -= dt
                if particle['life'] <= 0:
                    self.thrust_particles.remove(particle)
        
        # Apply gravity when fuel runs out
        elif self.launched:
            self.velocity_y += 100 * dt  # Gravity
            self.y += self.velocity_y * dt
    
    def render(self, screen):
        """Render the rocket and effects"""
        import random
        
        # Draw thrust particles
        for particle in self.thrust_particles:
            alpha = int(255 * (particle['life'] / 1.5))
            color = (*particle['color'], alpha)
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 3)
        
        # Draw rocket body based on current stage
        rocket_height = self.height - (self.max_stages - self.stage) * 15
        
        # Main body
        rocket_rect = pygame.Rect(self.x - self.width//2, self.y - rocket_height//2, 
                                self.width, rocket_height)
        pygame.draw.rect(screen, WHITE, rocket_rect)
        pygame.draw.rect(screen, (200, 200, 200), rocket_rect, 2)
        
        # Nose cone
        nose_points = [
            (self.x, self.y - rocket_height//2 - 10),
            (self.x - self.width//2, self.y - rocket_height//2),
            (self.x + self.width//2, self.y - rocket_height//2)
        ]
        pygame.draw.polygon(screen, RED, nose_points)
        
        # Fins
        if self.stage >= 1:
            fin_points = [
                (self.x - self.width//2, self.y + rocket_height//2),
                (self.x - self.width//2 - 8, self.y + rocket_height//2 + 10),
                (self.x - self.width//2, self.y + rocket_height//2 + 5)
            ]
            pygame.draw.polygon(screen, (100, 100, 100), fin_points)
            
            # Mirror for right side
            fin_points_right = [(2*self.x - p[0], p[1]) for p in fin_points]
            pygame.draw.polygon(screen, (100, 100, 100), fin_points_right)
        
        # Stage separation effect
        if self.stage_separation_time > 0:
            for i in range(10):
                spark_x = self.x + random.randint(-15, 15)
                spark_y = self.y + random.randint(-10, 10)
                pygame.draw.circle(screen, YELLOW, (spark_x, spark_y), 2)
        
        # Fuel indicator
        fuel_bar_width = 60
        fuel_bar_height = 8
        fuel_x = self.x - fuel_bar_width // 2
        fuel_y = self.y - rocket_height // 2 - 30
        
        # Background
        pygame.draw.rect(screen, (50, 50, 50), 
                        (fuel_x, fuel_y, fuel_bar_width, fuel_bar_height))
        
        # Fuel level
        fuel_width = int((self.fuel / 100) * fuel_bar_width)
        fuel_color = GREEN if self.fuel > 30 else RED
        pygame.draw.rect(screen, fuel_color, 
                        (fuel_x, fuel_y, fuel_width, fuel_bar_height))
        
        # Stage indicator
        stage_text = f"Stage {self.stage}/{self.max_stages}"
        font = pygame.font.Font(None, 20)
        stage_surface = font.render(stage_text, True, WHITE)
        screen.blit(stage_surface, (self.x - 30, fuel_y - 20))
    
    def get_mission_progress(self):
        """Calculate mission progress as percentage"""
        return min(100, (self.distance_traveled / self.destination['distance']) * 100)
    
    def is_mission_complete(self):
        """Check if rocket has reached its destination"""
        return self.get_mission_progress() >= 100
    
    def get_altitude(self):
        """Get current altitude in km (simplified)"""
        altitude_km = max(0, (self.start_y - self.y) * 0.1)  # Scale factor
        return altitude_km