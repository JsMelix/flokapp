"""Achievement and progress tracking scene"""
import pygame
from game.scenes.base_scene import BaseScene
from game.constants import *

class AchievementScene(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.achievements = [
            {
                'name': 'First Steps',
                'description': 'Complete your first mission',
                'icon': '🚀',
                'unlocked': False,
                'requirement': 'missions_completed >= 1'
            },
            {
                'name': 'Space Explorer',
                'description': 'Visit all planets in the solar system',
                'icon': '🌍',
                'unlocked': False,
                'requirement': 'planets_visited >= 4'
            },
            {
                'name': 'Knowledge Seeker',
                'description': 'Earn 500 knowledge points',
                'icon': '🧠',
                'unlocked': False,
                'requirement': 'knowledge_points >= 500'
            },
            {
                'name': 'Asteroid Miner',
                'description': 'Scan 10 asteroids',
                'icon': '⛏️',
                'unlocked': False,
                'requirement': 'asteroids_scanned >= 10'
            },
            {
                'name': 'International Collaborator',
                'description': 'Dock with the International Space Station',
                'icon': '🤝',
                'unlocked': False,
                'requirement': 'iss_docked >= 1'
            }
        ]
    
    def check_achievements(self, player_data):
        """Check and unlock achievements based on player progress"""
        newly_unlocked = []
        
        for achievement in self.achievements:
            if not achievement['unlocked']:
                # Simple evaluation of requirements
                req = achievement['requirement']
                if 'missions_completed' in req:
                    value = int(req.split('>=')[1].strip())
                    if player_data.get('missions_completed', 0) >= value:
                        achievement['unlocked'] = True
                        newly_unlocked.append(achievement)
                
                elif 'knowledge_points' in req:
                    value = int(req.split('>=')[1].strip())
                    if player_data.get('knowledge_points', 0) >= value:
                        achievement['unlocked'] = True
                        newly_unlocked.append(achievement)
        
        return newly_unlocked
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_manager.change_state(MENU)
    
    def render(self, screen):
        self.draw_stars(screen)
        
        # Title
        title = self.font_large.render("Achievements", True, CYAN)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(title, title_rect)
        
        # Achievement list
        for i, achievement in enumerate(self.achievements):
            y_pos = 150 + i * 80
            
            # Achievement card
            card_rect = pygame.Rect(100, y_pos, SCREEN_WIDTH - 200, 70)
            color = GREEN if achievement['unlocked'] else (50, 50, 50)
            pygame.draw.rect(screen, color, card_rect)
            pygame.draw.rect(screen, WHITE, card_rect, 2)
            
            # Icon
            icon_text = self.font_large.render(achievement['icon'], True, WHITE)
            screen.blit(icon_text, (120, y_pos + 10))
            
            # Name and description
            name_color = WHITE if achievement['unlocked'] else (150, 150, 150)
            name_text = self.font_medium.render(achievement['name'], True, name_color)
            screen.blit(name_text, (170, y_pos + 10))
            
            desc_text = self.font_small.render(achievement['description'], True, name_color)
            screen.blit(desc_text, (170, y_pos + 35))
            
            # Status
            status = "UNLOCKED" if achievement['unlocked'] else "LOCKED"
            status_color = YELLOW if achievement['unlocked'] else RED
            status_text = self.font_small.render(status, True, status_color)
            screen.blit(status_text, (SCREEN_WIDTH - 150, y_pos + 25))
        
        # Instructions
        instruction = self.font_small.render("ESC - Return to menu", True, WHITE)
        inst_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(instruction, inst_rect)