"""Main game manager for Flokapp"""
import pygame
from game.constants import *
from game.scenes.menu_scene import MenuScene
from game.scenes.game_scene import GameScene
from game.scenes.mission_scene import MissionScene
from game.audio.sound_manager import SoundManager

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.current_state = MENU
        self.scenes = {}
        self.sound_manager = SoundManager()
        self.player_data = {
            'name': 'Space Explorer',
            'missions_completed': 0,
            'knowledge_points': 0,
            'current_mission': None,
            'planets_visited': 0,
            'asteroids_scanned': 0,
            'iss_docked': 0
        }
        
        # Initialize scenes
        self.scenes[MENU] = MenuScene(self)
        self.scenes[PLAYING] = GameScene(self)
        self.scenes[MISSION_SELECT] = MissionScene(self)
        
        # Import here to avoid circular imports
        from game.scenes.achievement_scene import AchievementScene
        from game.scenes.solar_system_scene import SolarSystemScene
        from game.scenes.launch_scene import LaunchScene
        self.scenes['achievements'] = AchievementScene(self)
        self.scenes['solar_system'] = SolarSystemScene(self)
        self.scenes['launch'] = LaunchScene(self)
        
    def change_state(self, new_state):
        """Change the current game state"""
        if new_state in self.scenes:
            self.current_state = new_state
            self.scenes[new_state].on_enter()
    
    def handle_event(self, event):
        """Handle pygame events"""
        if self.current_state in self.scenes:
            self.scenes[self.current_state].handle_event(event)
    
    def update(self, dt):
        """Update current scene"""
        if self.current_state in self.scenes:
            self.scenes[self.current_state].update(dt)
    
    def render(self):
        """Render current scene"""
        self.screen.fill(SPACE_BLUE)
        if self.current_state in self.scenes:
            self.scenes[self.current_state].render(self.screen)