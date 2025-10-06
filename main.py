import pygame
import sys
from game.game_manager import GameManager
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

def main():
    """Main entry point for Flokapp"""
    pygame.init()
    
    # Set up display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flokapp - Space Explorer")
    clock = pygame.time.Clock()
    
    # Initialize game manager
    game_manager = GameManager(screen)
    
    # Main game loop
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game_manager.handle_event(event)
        
        # Update game state
        game_manager.update(dt)
        
        # Render everything
        game_manager.render()
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()