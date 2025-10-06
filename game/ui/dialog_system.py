"""Dialog system for educational content and interactions"""
import pygame
from game.constants import *

class DialogSystem:
    def __init__(self):
        self.active = False
        self.current_dialog = None
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)
        
    def show_dialog(self, dialog_data):
        """Show a dialog with the given data"""
        self.current_dialog = dialog_data
        self.active = True
    
    def hide_dialog(self):
        """Hide the current dialog"""
        self.active = False
        self.current_dialog = None
    
    def handle_event(self, event):
        """Handle dialog events"""
        if not self.active:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                if self.current_dialog.get('type') == 'info':
                    self.hide_dialog()
                    return True
                elif self.current_dialog.get('type') == 'question':
                    # Handle question selection
                    pass
            elif event.key == pygame.K_ESCAPE:
                self.hide_dialog()
                return True
        
        return True  # Dialog consumed the event
    
    def render(self, screen):
        """Render the dialog if active"""
        if not self.active or not self.current_dialog:
            return
        
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Dialog box
        dialog_width = 600
        dialog_height = 400
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
        
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(screen, (20, 30, 50), dialog_rect)
        pygame.draw.rect(screen, WHITE, dialog_rect, 3)
        
        # Dialog content
        if self.current_dialog['type'] == 'info':
            self.render_info_dialog(screen, dialog_rect)
        elif self.current_dialog['type'] == 'question':
            self.render_question_dialog(screen, dialog_rect)
    
    def render_info_dialog(self, screen, rect):
        """Render an information dialog"""
        title = self.current_dialog.get('title', 'Information')
        content = self.current_dialog.get('content', '')
        
        # Title
        title_text = self.font_large.render(title, True, CYAN)
        title_rect = title_text.get_rect(center=(rect.centerx, rect.y + 40))
        screen.blit(title_text, title_rect)
        
        # Content (word wrap)
        words = content.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if self.font_medium.size(test_line)[0] < rect.width - 40:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Render lines
        for i, line in enumerate(lines):
            line_text = self.font_medium.render(line, True, WHITE)
            line_y = rect.y + 100 + i * 30
            screen.blit(line_text, (rect.x + 20, line_y))
        
        # Instructions
        instruction = self.font_small.render("Press SPACE or ENTER to continue", True, YELLOW)
        inst_rect = instruction.get_rect(center=(rect.centerx, rect.bottom - 30))
        screen.blit(instruction, inst_rect)
    
    def render_question_dialog(self, screen, rect):
        """Render a question dialog with multiple choice"""
        question_data = self.current_dialog
        
        # Question
        question_text = self.font_medium.render(question_data['question'], True, WHITE)
        question_rect = question_text.get_rect(center=(rect.centerx, rect.y + 50))
        screen.blit(question_text, question_rect)
        
        # Options
        for i, option in enumerate(question_data['options']):
            option_text = self.font_medium.render(f"{i+1}. {option}", True, WHITE)
            option_y = rect.y + 120 + i * 40
            screen.blit(option_text, (rect.x + 40, option_y))
        
        # Instructions
        instruction = self.font_small.render("Press 1-4 to select answer", True, YELLOW)
        inst_rect = instruction.get_rect(center=(rect.centerx, rect.bottom - 30))
        screen.blit(instruction, inst_rect)