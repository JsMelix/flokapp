"""Main gameplay scene"""
import pygame
import random
from game.scenes.base_scene import BaseScene
from game.constants import *
from game.entities.player import Player
from game.entities.planet import Planet
from game.entities.asteroid import Asteroid
from game.entities.space_station import SpaceStation
from game.entities.mission_objective import MissionObjective
from game.ui.dialog_system import DialogSystem

class GameScene(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.planets = []
        self.asteroids = []
        self.space_stations = []
        self.mission_progress = 0
        self.mission_text = ""
        self.current_objective = None
        self.dialog_system = DialogSystem()
        self.resources_collected = 0
        
        # Import particle system
        from game.utils.particle_system import ParticleSystem
        self.particle_system = ParticleSystem()
        
        self.create_planets()
        self.create_asteroids()
        self.create_space_stations()
    
    def on_enter(self):
        """Initialize mission when entering game scene"""
        mission = self.game_manager.player_data.get('current_mission')
        if mission:
            self.mission_text = f"Mission: {mission['name']}"
            self.mission_progress = 0
            self.current_objective = MissionObjective(mission['type'])
            
            # Show mission briefing
            self.dialog_system.show_dialog({
                'type': 'info',
                'title': mission['name'],
                'content': f"{mission['description']} Your objective is to explore, learn, and complete educational challenges to advance humanity's understanding of space."
            })
    
    def create_planets(self):
        """Create planets for exploration"""
        planet_data = [
            {'name': 'Earth', 'color': PLANET_COLORS['earth'], 'pos': (200, 200)},
            {'name': 'Mars', 'color': PLANET_COLORS['mars'], 'pos': (600, 300)},
            {'name': 'Moon', 'color': PLANET_COLORS['moon'], 'pos': (800, 150)},
            {'name': 'Jupiter', 'color': PLANET_COLORS['jupiter'], 'pos': (400, 500)}
        ]
        
        for data in planet_data:
            planet = Planet(data['pos'][0], data['pos'][1], data['name'], data['color'])
            self.planets.append(planet)
    
    def create_asteroids(self):
        """Create asteroids for resource collection"""
        for _ in range(8):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, SCREEN_HEIGHT - 100)
            # Avoid spawning too close to planets
            too_close = any(
                ((x - p.x)**2 + (y - p.y)**2)**0.5 < 100 
                for p in self.planets
            )
            if not too_close:
                asteroid = Asteroid(x, y)
                self.asteroids.append(asteroid)
    
    def create_space_stations(self):
        """Create space stations for collaboration missions"""
        station = SpaceStation(300, 600, "International Space Station")
        self.space_stations.append(station)
    
    def handle_event(self, event):
        # Dialog system gets priority
        if self.dialog_system.handle_event(event):
            return
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_manager.change_state(MENU)
            elif event.key == pygame.K_SPACE:
                self.scan_nearby_objects()
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                if self.current_objective and self.dialog_system.current_dialog:
                    if self.dialog_system.current_dialog.get('type') == 'question':
                        answer_index = event.key - pygame.K_1
                        self.answer_question(answer_index)
        
        self.player.handle_event(event)
    
    def update(self, dt):
        self.player.update(dt)
        
        # Update asteroids
        for asteroid in self.asteroids:
            asteroid.update(dt)
        
        # Update space stations
        for station in self.space_stations:
            station.update(dt)
        
        # Check interactions
        for planet in self.planets:
            if self.player.check_collision(planet):
                self.interact_with_planet(planet)
        
        for station in self.space_stations:
            distance = ((self.player.x - station.x)**2 + (self.player.y - station.y)**2)**0.5
            if distance < station.radius + self.player.radius + 20:
                self.interact_with_station(station)
        
        # Update particle system
        self.particle_system.update(dt)
        
        # Update mission progress
        if self.current_objective and self.current_objective.is_complete():
            self.mission_progress = 100
        elif self.current_objective:
            self.mission_progress = self.current_objective.progress
    
    def interact_with_planet(self, planet):
        """Handle planet interaction"""
        if not planet.visited:
            planet.visited = True
            self.game_manager.player_data['knowledge_points'] += 50
            self.game_manager.player_data['planets_visited'] += 1
            
            # Play success sound and add particles
            self.game_manager.sound_manager.play_sound('success')
            self.particle_system.add_explosion(planet.x, planet.y, planet.color)
            
            # Show educational content about the planet
            from game.data.nasa_facts import get_random_fact
            fact = get_random_fact(planet.name)
            
            self.dialog_system.show_dialog({
                'type': 'info',
                'title': f'Exploring {planet.name}',
                'content': f"Welcome to {planet.name}! {planet.get_fact()} Here's what NASA has discovered: {fact}"
            })
    
    def render(self, screen):
        self.draw_stars(screen)
        
        # Draw planets
        for planet in self.planets:
            planet.render(screen)
        
        # Draw asteroids
        for asteroid in self.asteroids:
            asteroid.render(screen)
        
        # Draw space stations
        for station in self.space_stations:
            station.render(screen)
        
        # Draw player
        self.player.render(screen)
        
        # Draw scan range indicator
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.draw.circle(screen, (0, 255, 0, 50), (int(self.player.x), int(self.player.y)), 80, 2)
        
        # Draw particle effects
        if hasattr(self, 'particle_system'):
            self.particle_system.render(screen)
        
        # Draw UI
        self.draw_ui(screen)
        
        # Draw dialog system
        self.dialog_system.render(screen)
    
    def draw_ui(self, screen):
        """Draw game UI elements"""
        # Mission info
        mission_text = self.font_medium.render(self.mission_text, True, WHITE)
        screen.blit(mission_text, (10, 10))
        
        # Progress bar
        progress_rect = pygame.Rect(10, 50, 300, 20)
        pygame.draw.rect(screen, WHITE, progress_rect, 2)
        fill_width = int((self.mission_progress / 100) * 298)
        fill_rect = pygame.Rect(11, 51, fill_width, 18)
        pygame.draw.rect(screen, GREEN, fill_rect)
        
        # Knowledge points
        points_text = self.font_small.render(
            f"Knowledge Points: {self.game_manager.player_data['knowledge_points']}", 
            True, YELLOW
        )
        screen.blit(points_text, (10, 80))
        
        # Resources collected
        resources_text = self.font_small.render(
            f"Resources Scanned: {self.resources_collected}", 
            True, CYAN
        )
        screen.blit(resources_text, (10, 110))
        
        # Instructions
        instructions = [
            "WASD - Move spacecraft",
            "SPACE - Scan objects/Answer questions",
            "Approach planets & stations",
            "ESC - Return to menu"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font_small.render(instruction, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH - 250, 10 + i * 25))
    
    def scan_nearby_objects(self):
        """Scan nearby asteroids and objects"""
        scan_range = 80
        scanned_something = False
        
        for asteroid in self.asteroids:
            distance = ((self.player.x - asteroid.x)**2 + (self.player.y - asteroid.y)**2)**0.5
            if distance < scan_range:
                scan_result = asteroid.scan()
                if scan_result:
                    scanned_something = True
                    self.resources_collected += 1
                    self.game_manager.player_data['knowledge_points'] += 25
                    self.game_manager.player_data['asteroids_scanned'] += 1
                    
                    # Play scan sound and add particles
                    self.game_manager.sound_manager.play_sound('scan')
                    self.particle_system.add_scan_particles(asteroid.x, asteroid.y)
                    
                    self.dialog_system.show_dialog({
                        'type': 'info',
                        'title': 'Asteroid Scan Complete',
                        'content': f"Discovered {scan_result['mineral']} asteroid! Size: {scan_result['size']}, Value: {scan_result['value']} credits. This data helps NASA understand asteroid composition for future mining missions."
                    })
                    break
        
        if not scanned_something:
            # Show educational question if no objects to scan
            if self.current_objective:
                question = self.current_objective.get_current_question()
                if question:
                    question_dialog = question.copy()
                    question_dialog['type'] = 'question'
                    self.dialog_system.show_dialog(question_dialog)
    
    def answer_question(self, answer_index):
        """Process educational question answer"""
        if self.current_objective:
            is_correct, explanation = self.current_objective.answer_question(answer_index)
            
            if is_correct:
                self.game_manager.player_data['knowledge_points'] += 50
                result_text = "Correct! " + explanation
                self.game_manager.sound_manager.play_sound('success')
                self.particle_system.add_success_particles(self.player.x, self.player.y)
            else:
                result_text = "Incorrect. " + explanation
                self.game_manager.sound_manager.play_sound('beep')
            
            self.dialog_system.show_dialog({
                'type': 'info',
                'title': 'Answer Result',
                'content': result_text
            })
    
    def interact_with_station(self, station):
        """Handle space station interaction"""
        if not station.docked:
            dock_result = station.dock()
            self.game_manager.player_data['knowledge_points'] += 100
            self.game_manager.player_data['iss_docked'] += 1
            
            # Play docking sound and effects
            self.game_manager.sound_manager.play_sound('dock')
            self.particle_system.add_warp_particles(station.x, station.y)
            
            crew_list = "\n".join(dock_result['crew'][:2])  # Show first 2 crew members
            
            self.dialog_system.show_dialog({
                'type': 'info',
                'title': 'Space Station Docked',
                'content': f"{dock_result['message']} You've connected with international crew members: {crew_list}. This collaboration represents humanity working together in space!"
            })