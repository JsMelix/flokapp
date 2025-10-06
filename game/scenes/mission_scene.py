"""Mission selection scene"""
import pygame
from game.scenes.base_scene import BaseScene
from game.constants import *

class MissionScene(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.missions = [
            {
                'name': 'Mars Rover Navigation',
                'type': EXPLORATION,
                'description': 'Guide a rover through Martian terrain using NASA data',
                'difficulty': 'Beginner',
                'points': 100
            },
            {
                'name': 'ISS Collaboration',
                'type': COLLABORATION, 
                'description': 'Coordinate with international teams on space station',
                'difficulty': 'Intermediate',
                'points': 200
            },
            {
                'name': 'Exoplanet Discovery',
                'type': RESEARCH,
                'description': 'Analyze telescope data to find habitable worlds',
                'difficulty': 'Advanced',
                'points': 300
            },
            {
                'name': 'Asteroid Defense',
                'type': PROBLEM_SOLVING,
                'description': 'Calculate trajectories to protect Earth',
                'difficulty': 'Expert',
                'points': 500
            }
        ]
        self.selected_mission = 0
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_mission = (self.selected_mission - 1) % len(self.missions)
            elif event.key == pygame.K_DOWN:
                self.selected_mission = (self.selected_mission + 1) % len(self.missions)
            elif event.key == pygame.K_RETURN:
                self.start_mission()
            elif event.key == pygame.K_ESCAPE:
                self.game_manager.change_state(MENU)
    
    def start_mission(self):
        mission = self.missions[self.selected_mission]
        self.game_manager.player_data['current_mission'] = mission
        # Go to launch scene first, then to gameplay
        self.game_manager.change_state('launch')
    
    def render(self, screen):
        self.draw_stars(screen)
        
        # Title
        title = self.font_large.render("Mission Selection", True, CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(title, title_rect)
        
        # Mission list
        for i, mission in enumerate(self.missions):
            y_pos = 180 + i * 120
            
            # Mission card background
            card_rect = pygame.Rect(100, y_pos - 10, SCREEN_WIDTH - 200, 100)
            color = BLUE if i == self.selected_mission else (20, 30, 50)
            pygame.draw.rect(screen, color, card_rect)
            pygame.draw.rect(screen, WHITE, card_rect, 2)
            
            # Mission details
            name_text = self.font_medium.render(mission['name'], True, WHITE)
            screen.blit(name_text, (120, y_pos))
            
            desc_text = self.font_small.render(mission['description'], True, WHITE)
            screen.blit(desc_text, (120, y_pos + 30))
            
            diff_text = self.font_small.render(f"Difficulty: {mission['difficulty']}", True, YELLOW)
            screen.blit(diff_text, (120, y_pos + 50))
            
            points_text = self.font_small.render(f"Points: {mission['points']}", True, GREEN)
            screen.blit(points_text, (120, y_pos + 70))
        
        # Instructions
        instructions = self.font_small.render("↑↓ Navigate | ENTER Start Mission | ESC Back", True, WHITE)
        inst_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(instructions, inst_rect)