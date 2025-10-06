"""Main menu scene for Flokapp"""
import pygame
from game.scenes.base_scene import BaseScene
from game.constants import *

class MenuScene(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.menu_options = [
            "Start Mission",
            "Solar System Explorer",
            "Achievements", 
            "Mission Archive",
            "Settings",
            "Exit"
        ]
        self.selected_option = 0
        self.title_animation = 0
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                self.select_option()
    
    def select_option(self):
        if self.selected_option == 0:  # Start Mission
            self.game_manager.change_state(MISSION_SELECT)
        elif self.selected_option == 1:  # Solar System Explorer
            self.game_manager.change_state('solar_system')
        elif self.selected_option == 2:  # Achievements
            self.game_manager.change_state('achievements')
        elif self.selected_option == 3:  # Mission Archive
            pass  # TODO: Implement mission archive
        elif self.selected_option == 4:  # Settings
            pass  # TODO: Implement settings
        elif self.selected_option == 5:  # Exit
            pygame.quit()
            exit()
    
    def update(self, dt):
        self.title_animation += dt * 2
    
    def render(self, screen):
        self.draw_stars(screen)
        
        # Draw animated title
        title_y = 150 + int(10 * pygame.math.Vector2(0, 1).rotate(self.title_animation * 50).y)
        title_text = self.font_large.render("🚀 FLOKAPP", True, CYAN)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, title_y))
        screen.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle = self.font_medium.render("Connecting Minds to Conquer Space", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, title_y + 60))
        screen.blit(subtitle, subtitle_rect)
        
        # Draw menu options
        for i, option in enumerate(self.menu_options):
            color = YELLOW if i == self.selected_option else WHITE
            text = self.font_medium.render(option, True, color)
            y_pos = 350 + i * 50
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            screen.blit(text, text_rect)
            
            # Draw selection indicator
            if i == self.selected_option:
                pygame.draw.rect(screen, YELLOW, text_rect, 2)
        
        # Draw instructions
        instructions = self.font_small.render("Use ↑↓ to navigate, ENTER to select", True, WHITE)
        inst_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(instructions, inst_rect)