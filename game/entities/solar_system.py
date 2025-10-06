"""Solar system simulation with realistic orbital mechanics"""
import pygame
import math
from game.constants import *
from game.entities.planet import Planet
from game.entities.satellite import Satellite

class SolarSystem:
    def __init__(self):
        self.sun_x = SCREEN_WIDTH // 2
        self.sun_y = SCREEN_HEIGHT // 2
        self.sun_radius = 30
        
        # Planetary data with realistic relative sizes and distances
        self.planetary_data = [
            {
                'name': 'Mercury', 'color': (169, 169, 169), 'radius': 8,
                'orbit_radius': 80, 'orbit_speed': 2.0, 'angle': 0
            },
            {
                'name': 'Venus', 'color': (255, 198, 73), 'radius': 12,
                'orbit_radius': 110, 'orbit_speed': 1.5, 'angle': 1.2
            },
            {
                'name': 'Earth', 'color': PLANET_COLORS['earth'], 'radius': 13,
                'orbit_radius': 150, 'orbit_speed': 1.0, 'angle': 2.4
            },
            {
                'name': 'Mars', 'color': PLANET_COLORS['mars'], 'radius': 10,
                'orbit_radius': 190, 'orbit_speed': 0.8, 'angle': 4.1
            },
            {
                'name': 'Jupiter', 'color': PLANET_COLORS['jupiter'], 'radius': 25,
                'orbit_radius': 280, 'orbit_speed': 0.4, 'angle': 0.8
            },
            {
                'name': 'Saturn', 'color': (255, 215, 0), 'radius': 22,
                'orbit_radius': 350, 'orbit_speed': 0.3, 'angle': 3.7
            }
        ]
        
        self.planets = []
        self.satellites = []
        self.time_scale = 1.0
        
        self.create_planets()
        self.create_satellites()
    
    def create_planets(self):
        """Create planets with orbital mechanics"""
        for data in self.planetary_data:
            # Calculate initial position
            x = self.sun_x + math.cos(data['angle']) * data['orbit_radius']
            y = self.sun_y + math.sin(data['angle']) * data['orbit_radius']
            
            planet = Planet(x, y, data['name'], data['color'])
            planet.radius = data['radius']
            planet.orbit_radius = data['orbit_radius']
            planet.orbit_speed = data['orbit_speed']
            planet.orbit_angle = data['angle']
            
            self.planets.append(planet)
    
    def create_satellites(self):
        """Create satellites around Earth"""
        earth = next((p for p in self.planets if p.name == 'Earth'), None)
        if earth:
            # Create different types of satellites
            satellite_types = ['communication', 'weather', 'navigation', 'scientific']
            for i, sat_type in enumerate(satellite_types):
                satellite = Satellite(earth.x, earth.y, sat_type)
                satellite.orbit_angle = i * (math.pi / 2)  # Spread them out
                satellite.orbit_radius = 40 + i * 10  # Different orbital distances
                self.satellites.append(satellite)
    
    def update(self, dt):
        """Update solar system simulation"""
        dt *= self.time_scale
        
        # Update planetary orbits
        for planet in self.planets:
            planet.orbit_angle += planet.orbit_speed * dt * 0.1
            
            # Calculate new position
            planet.x = self.sun_x + math.cos(planet.orbit_angle) * planet.orbit_radius
            planet.y = self.sun_y + math.sin(planet.orbit_angle) * planet.orbit_radius
            
            planet.update(dt)
        
        # Update satellites (they orbit Earth)
        earth = next((p for p in self.planets if p.name == 'Earth'), None)
        if earth:
            for satellite in self.satellites:
                satellite.update(dt)
    
    def render(self, screen):
        """Render the solar system"""
        # Draw orbit paths
        for planet in self.planets:
            pygame.draw.circle(screen, (50, 50, 50), 
                             (int(self.sun_x), int(self.sun_y)), 
                             planet.orbit_radius, 1)
        
        # Draw the Sun
        pygame.draw.circle(screen, YELLOW, 
                         (int(self.sun_x), int(self.sun_y)), 
                         self.sun_radius)
        pygame.draw.circle(screen, (255, 255, 150), 
                         (int(self.sun_x), int(self.sun_y)), 
                         self.sun_radius - 5)
        
        # Draw planets
        for planet in self.planets:
            planet.render(screen)
        
        # Draw satellites around Earth
        earth = next((p for p in self.planets if p.name == 'Earth'), None)
        if earth:
            for satellite in self.satellites:
                satellite.render(screen, earth.x, earth.y)
        
        # Draw time scale indicator
        font = pygame.font.Font(None, 24)
        time_text = font.render(f"Time Scale: {self.time_scale:.1f}x", True, WHITE)
        screen.blit(time_text, (10, SCREEN_HEIGHT - 30))
    
    def get_planet_by_name(self, name):
        """Get a planet by its name"""
        return next((p for p in self.planets if p.name == name), None)
    
    def change_time_scale(self, delta):
        """Change the simulation time scale"""
        self.time_scale = max(0.1, min(5.0, self.time_scale + delta))
    
    def get_nearest_satellite(self, x, y, max_distance=50):
        """Get the nearest satellite to a position"""
        earth = next((p for p in self.planets if p.name == 'Earth'), None)
        if not earth:
            return None
        
        nearest_satellite = None
        min_distance = max_distance
        
        for satellite in self.satellites:
            sat_x, sat_y = satellite.get_orbital_position(earth.x, earth.y)
            distance = math.sqrt((x - sat_x)**2 + (y - sat_y)**2)
            
            if distance < min_distance:
                min_distance = distance
                nearest_satellite = satellite
        
        return nearest_satellite