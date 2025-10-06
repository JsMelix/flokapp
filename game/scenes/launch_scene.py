"""Rocket launch simulation scene"""
import pygame
from game.scenes.base_scene import BaseScene
from game.constants import *
from game.entities.rocket import Rocket
from game.ui.dialog_system import DialogSystem

class LaunchScene(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.rocket = None
        self.dialog_system = DialogSystem()
        self.launch_pad_x = SCREEN_WIDTH // 2
        self.launch_pad_y = SCREEN_HEIGHT - 100
        self.countdown = 10
        self.countdown_active = False
        self.mission_briefing_shown = False
        self.launch_successful = False
        
    def on_enter(self):
        """Initialize launch scene with current mission"""
        mission = self.game_manager.player_data.get('current_mission')
        if mission:
            self.rocket = Rocket(self.launch_pad_x, self.launch_pad_y, mission['type'])
            self.countdown = 10
            self.countdown_active = False
            self.mission_briefing_shown = False
            self.launch_successful = False
            
            # Show mission briefing
            self.show_mission_briefing(mission)
    
    def show_mission_briefing(self, mission):
        """Show detailed mission briefing"""
        destination = self.rocket.destination
        content = f"Mission: {mission['name']}\n\n"
        content += f"Objective: {mission['description']}\n\n"
        content += f"Destination: {destination['name']}\n"
        content += f"Distance: {destination['distance']:,} km\n\n"
        content += "Your rocket is fueled and ready for launch. This mission will advance our understanding of space and contribute to humanity's cosmic journey.\n\n"
        content += "Press SPACE to begin countdown sequence!"
        
        self.dialog_system.show_dialog({
            'type': 'info',
            'title': 'Mission Briefing',
            'content': content
        })
        self.mission_briefing_shown = True
    
    def handle_event(self, event):
        # Dialog system gets priority
        if self.dialog_system.handle_event(event):
            return
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_manager.change_state(MISSION_SELECT)
            elif event.key == pygame.K_SPACE:
                if self.mission_briefing_shown and not self.countdown_active and not self.rocket.launched:
                    self.start_countdown()
                elif self.countdown <= 0 and not self.rocket.launched:
                    self.launch_rocket()
    
    def start_countdown(self):
        """Start the launch countdown"""
        self.countdown_active = True
        self.countdown = 10
    
    def launch_rocket(self):
        """Launch the rocket"""
        if self.rocket:
            self.rocket.launch()
            self.launch_successful = True
    
    def update(self, dt):
        if self.rocket:
            self.rocket.update(dt)
            
            # Update countdown
            if self.countdown_active and self.countdown > 0:
                self.countdown -= dt
                if self.countdown <= 0:
                    self.countdown = 0
            
            # Check mission completion
            if self.rocket.is_mission_complete() and not self.dialog_system.active:
                self.show_mission_complete()
    
    def show_mission_complete(self):
        """Show mission completion dialog"""
        mission = self.game_manager.player_data.get('current_mission')
        self.game_manager.player_data['missions_completed'] += 1
        self.game_manager.player_data['knowledge_points'] += mission.get('points', 100)
        
        content = f"Mission Complete!\n\n"
        content += f"Congratulations! You have successfully completed the {mission['name']} mission.\n\n"
        content += f"Knowledge Points Earned: {mission.get('points', 100)}\n"
        content += f"Total Missions Completed: {self.game_manager.player_data['missions_completed']}\n\n"
        content += "Your contribution to space exploration helps advance human knowledge and inspires future generations of space explorers!"
        
        self.dialog_system.show_dialog({
            'type': 'info',
            'title': 'Mission Success!',
            'content': content
        })
    
    def render(self, screen):
        # Sky gradient background
        for y in range(SCREEN_HEIGHT):
            # Create gradient from space blue to lighter blue
            ratio = y / SCREEN_HEIGHT
            r = int(SPACE_BLUE[0] + (100 - SPACE_BLUE[0]) * ratio)
            g = int(SPACE_BLUE[1] + (150 - SPACE_BLUE[1]) * ratio)
            b = int(SPACE_BLUE[2] + (200 - SPACE_BLUE[2]) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Draw stars in upper portion
        if not self.rocket or not self.rocket.launched:
            self.draw_stars(screen)
        
        # Draw launch pad
        self.draw_launch_pad(screen)
        
        # Draw rocket
        if self.rocket:
            self.rocket.render(screen)
        
        # Draw UI
        self.draw_ui(screen)
        
        # Draw dialog system
        self.dialog_system.render(screen)
    
    def draw_launch_pad(self, screen):
        """Draw the rocket launch pad"""
        # Launch pad base
        pad_width = 100
        pad_height = 20
        pad_rect = pygame.Rect(self.launch_pad_x - pad_width//2, 
                              self.launch_pad_y + 30, 
                              pad_width, pad_height)
        pygame.draw.rect(screen, (100, 100, 100), pad_rect)
        pygame.draw.rect(screen, WHITE, pad_rect, 2)
        
        # Support towers
        tower_height = 80
        # Left tower
        pygame.draw.rect(screen, (80, 80, 80), 
                        (self.launch_pad_x - 60, self.launch_pad_y - tower_height + 30, 10, tower_height))
        # Right tower  
        pygame.draw.rect(screen, (80, 80, 80), 
                        (self.launch_pad_x + 50, self.launch_pad_y - tower_height + 30, 10, tower_height))
        
        # Connection cables
        if self.rocket and not self.rocket.launched:
            pygame.draw.line(screen, YELLOW, 
                           (self.launch_pad_x - 55, self.launch_pad_y - 20),
                           (self.launch_pad_x - 15, self.launch_pad_y - 10), 2)
            pygame.draw.line(screen, YELLOW,
                           (self.launch_pad_x + 55, self.launch_pad_y - 20), 
                           (self.launch_pad_x + 15, self.launch_pad_y - 10), 2)
    
    def draw_ui(self, screen):
        """Draw launch UI elements"""
        # Mission info
        mission = self.game_manager.player_data.get('current_mission')
        if mission:
            mission_text = self.font_medium.render(f"Mission: {mission['name']}", True, WHITE)
            screen.blit(mission_text, (10, 10))
        
        # Countdown
        if self.countdown_active:
            if self.countdown > 0:
                countdown_text = self.font_large.render(f"T-{int(self.countdown + 1)}", True, RED)
                countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
                screen.blit(countdown_text, countdown_rect)
            else:
                launch_text = self.font_large.render("LAUNCH!", True, GREEN)
                launch_rect = launch_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
                screen.blit(launch_text, launch_rect)
        
        # Rocket telemetry
        if self.rocket and self.rocket.launched:
            telemetry_y = 50
            
            # Altitude
            altitude_text = self.font_small.render(f"Altitude: {self.rocket.get_altitude():.1f} km", True, CYAN)
            screen.blit(altitude_text, (10, telemetry_y))
            
            # Mission progress
            progress = self.rocket.get_mission_progress()
            progress_text = self.font_small.render(f"Mission Progress: {progress:.1f}%", True, GREEN)
            screen.blit(progress_text, (10, telemetry_y + 25))
            
            # Destination
            dest_text = self.font_small.render(f"Destination: {self.rocket.destination['name']}", True, WHITE)
            screen.blit(dest_text, (10, telemetry_y + 50))
        
        # Instructions
        if not self.countdown_active and not self.rocket.launched:
            instruction = "Press SPACE to start countdown"
        elif self.countdown <= 0 and not self.rocket.launched:
            instruction = "Press SPACE to LAUNCH!"
        else:
            instruction = "ESC - Return to mission select"
        
        inst_text = self.font_small.render(instruction, True, YELLOW)
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(inst_text, inst_rect)