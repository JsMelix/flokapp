"""Solar system exploration scene with realistic orbital mechanics"""
import pygame
from game.scenes.base_scene import BaseScene
from game.constants import *
from game.entities.player import Player
from game.entities.solar_system import SolarSystem
from game.ui.dialog_system import DialogSystem

class SolarSystemScene(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.player = Player(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
        self.solar_system = SolarSystem()
        self.dialog_system = DialogSystem()
        self.camera_x = 0
        self.camera_y = 0
        self.zoom = 1.0
        self.selected_planet = None
        self.data_collected = {}
        
    def handle_event(self, event):
        # Dialog system gets priority
        if self.dialog_system.handle_event(event):
            return
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_manager.change_state(MENU)
            elif event.key == pygame.K_SPACE:
                self.interact_with_objects()
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                self.solar_system.change_time_scale(0.5)
            elif event.key == pygame.K_MINUS:
                self.solar_system.change_time_scale(-0.5)
            elif event.key == pygame.K_z:
                self.zoom = min(2.0, self.zoom + 0.2)
            elif event.key == pygame.K_x:
                self.zoom = max(0.5, self.zoom - 0.2)
        
        self.player.handle_event(event)
    
    def interact_with_objects(self):
        """Interact with nearby planets and satellites"""
        # Check planet interactions
        for planet in self.solar_system.planets:
            distance = ((self.player.x - planet.x)**2 + (self.player.y - planet.y)**2)**0.5
            if distance < planet.radius + self.player.radius + 30:
                self.interact_with_planet(planet)
                return
        
        # Check satellite interactions
        satellite = self.solar_system.get_nearest_satellite(self.player.x, self.player.y, 60)
        if satellite:
            self.interact_with_satellite(satellite)
    
    def interact_with_planet(self, planet):
        """Handle planet interaction with detailed information"""
        if not planet.visited:
            planet.visited = True
            self.game_manager.player_data['knowledge_points'] += 100
        
        # Detailed planet information
        planet_info = {
            'Mercury': {
                'distance_from_sun': '58 million km',
                'day_length': '59 Earth days',
                'temperature': '-173°C to 427°C',
                'interesting_fact': 'Mercury has no atmosphere and extreme temperature variations.'
            },
            'Venus': {
                'distance_from_sun': '108 million km', 
                'day_length': '243 Earth days',
                'temperature': '462°C (hottest planet)',
                'interesting_fact': 'Venus rotates backwards and has a thick, toxic atmosphere.'
            },
            'Earth': {
                'distance_from_sun': '150 million km',
                'day_length': '24 hours',
                'temperature': '-89°C to 58°C',
                'interesting_fact': 'The only known planet with life, protected by a magnetic field.'
            },
            'Mars': {
                'distance_from_sun': '228 million km',
                'day_length': '24.6 hours', 
                'temperature': '-87°C to -5°C',
                'interesting_fact': 'Mars has the largest volcano and canyon in the solar system.'
            },
            'Jupiter': {
                'distance_from_sun': '778 million km',
                'day_length': '9.9 hours',
                'temperature': '-108°C',
                'interesting_fact': 'Jupiter is a gas giant with over 80 moons and protects inner planets.'
            },
            'Saturn': {
                'distance_from_sun': '1.4 billion km',
                'day_length': '10.7 hours',
                'temperature': '-139°C', 
                'interesting_fact': 'Saturn has spectacular rings made of ice and rock particles.'
            }
        }
        
        info = planet_info.get(planet.name, {})
        content = f"Welcome to {planet.name}!\n\n"
        content += f"Distance from Sun: {info.get('distance_from_sun', 'Unknown')}\n"
        content += f"Day Length: {info.get('day_length', 'Unknown')}\n"
        content += f"Temperature: {info.get('temperature', 'Unknown')}\n\n"
        content += info.get('interesting_fact', 'A fascinating world to explore!')
        
        self.dialog_system.show_dialog({
            'type': 'info',
            'title': f'Exploring {planet.name}',
            'content': content
        })
    
    def interact_with_satellite(self, satellite):
        """Handle satellite interaction and data collection"""
        data = satellite.interact()
        if data:
            satellite_type = satellite.type
            if satellite_type not in self.data_collected:
                self.data_collected[satellite_type] = 0
            
            self.data_collected[satellite_type] += data['amount']
            self.game_manager.player_data['knowledge_points'] += 50
            
            content = f"Connected to {data['name']}!\n\n"
            content += f"Function: {data['function']}\n\n"
            content += f"Data Collected: {data['amount']:.1f} units of {data['data_type']}\n\n"
            content += "This satellite data helps NASA monitor Earth and communicate with spacecraft!"
            
            self.dialog_system.show_dialog({
                'type': 'info',
                'title': 'Satellite Data Link',
                'content': content
            })
    
    def update(self, dt):
        self.player.update(dt)
        self.solar_system.update(dt)
        
        # Update camera to follow player (with some offset)
        target_camera_x = -self.player.x + SCREEN_WIDTH // 2
        target_camera_y = -self.player.y + SCREEN_HEIGHT // 2
        
        # Smooth camera movement
        self.camera_x += (target_camera_x - self.camera_x) * dt * 2
        self.camera_y += (target_camera_y - self.camera_y) * dt * 2
    
    def render(self, screen):
        # Clear screen with space background
        screen.fill(SPACE_BLUE)
        self.draw_stars(screen)
        
        # Apply camera transform
        camera_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        camera_surface.fill(SPACE_BLUE)
        
        # Draw solar system
        self.solar_system.render(camera_surface)
        
        # Draw player
        self.player.render(camera_surface)
        
        # Apply zoom and camera offset
        if self.zoom != 1.0:
            scaled_surface = pygame.transform.scale(
                camera_surface, 
                (int(SCREEN_WIDTH * self.zoom), int(SCREEN_HEIGHT * self.zoom))
            )
            zoom_offset_x = (SCREEN_WIDTH - scaled_surface.get_width()) // 2
            zoom_offset_y = (SCREEN_HEIGHT - scaled_surface.get_height()) // 2
            screen.blit(scaled_surface, (zoom_offset_x, zoom_offset_y))
        else:
            screen.blit(camera_surface, (self.camera_x, self.camera_y))
        
        # Draw UI
        self.draw_ui(screen)
        
        # Draw dialog system
        self.dialog_system.render(screen)
    
    def draw_ui(self, screen):
        """Draw UI elements"""
        # Knowledge points
        points_text = self.font_medium.render(
            f"Knowledge Points: {self.game_manager.player_data['knowledge_points']}", 
            True, YELLOW
        )
        screen.blit(points_text, (10, 10))
        
        # Data collected summary
        y_offset = 50
        for data_type, amount in self.data_collected.items():
            data_text = self.font_small.render(
                f"{data_type.title()} Data: {amount:.0f}", 
                True, CYAN
            )
            screen.blit(data_text, (10, y_offset))
            y_offset += 25
        
        # Controls
        controls = [
            "WASD - Move spacecraft",
            "SPACE - Interact with objects", 
            "+/- - Change time scale",
            "Z/X - Zoom in/out",
            "ESC - Return to menu"
        ]
        
        for i, control in enumerate(controls):
            text = self.font_small.render(control, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH - 250, 10 + i * 20))
        
        # Zoom indicator
        zoom_text = self.font_small.render(f"Zoom: {self.zoom:.1f}x", True, WHITE)
        screen.blit(zoom_text, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 30))