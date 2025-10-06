"""Sound effects and music manager for Flokapp"""
import pygame
import math
import numpy as np

class SoundManager:
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        self.generate_sounds()
    
    def generate_sounds(self):
        """Generate procedural sound effects"""
        # Create basic sound effects using pygame
        self.sounds['beep'] = self.generate_beep(440, 0.1)
        self.sounds['launch'] = self.generate_rocket_sound()
        self.sounds['scan'] = self.generate_scan_sound()
        self.sounds['success'] = self.generate_success_sound()
        self.sounds['menu_select'] = self.generate_beep(880, 0.05)
        self.sounds['dock'] = self.generate_dock_sound()
    
    def generate_beep(self, frequency, duration):
        """Generate a simple beep sound"""
        sample_rate = 22050
        frames = int(duration * sample_rate)
        arr = []
        
        for i in range(frames):
            time = float(i) / sample_rate
            wave = math.sin(2 * math.pi * frequency * time)
            # Apply envelope to avoid clicks
            envelope = min(1.0, min(i / (frames * 0.1), (frames - i) / (frames * 0.1)))
            arr.append([int(wave * envelope * 32767 * 0.3), int(wave * envelope * 32767 * 0.3)])
        
        sound = pygame.sndarray.make_sound(np.array(arr, dtype=np.int16))
        return sound
    
    def generate_rocket_sound(self):
        """Generate rocket launch sound effect"""
        sample_rate = 22050
        duration = 2.0
        frames = int(duration * sample_rate)
        arr = []
        
        for i in range(frames):
            time = float(i) / sample_rate
            # Low frequency rumble with some noise
            base_freq = 60 + time * 20
            noise = (hash(i) % 1000 - 500) / 10000.0
            wave = math.sin(2 * math.pi * base_freq * time) * 0.3 + noise * 0.2
            
            # Fade in effect
            envelope = min(1.0, time / 0.5)
            arr.append([int(wave * envelope * 32767 * 0.4), int(wave * envelope * 32767 * 0.4)])
        
        sound = pygame.sndarray.make_sound(np.array(arr, dtype=np.int16))
        return sound
    
    def generate_scan_sound(self):
        """Generate scanning sound effect"""
        sample_rate = 22050
        duration = 0.8
        frames = int(duration * sample_rate)
        arr = []
        
        for i in range(frames):
            time = float(i) / sample_rate
            # Sweeping frequency
            freq = 200 + math.sin(time * 8) * 100
            wave = math.sin(2 * math.pi * freq * time)
            
            # Pulse envelope
            pulse = (math.sin(time * 20) + 1) / 2
            envelope = max(0, 1 - time / duration)
            
            arr.append([int(wave * pulse * envelope * 32767 * 0.2), 
                       int(wave * pulse * envelope * 32767 * 0.2)])
        
        sound = pygame.sndarray.make_sound(np.array(arr, dtype=np.int16))
        return sound
    
    def generate_success_sound(self):
        """Generate success/achievement sound"""
        sample_rate = 22050
        duration = 1.0
        frames = int(duration * sample_rate)
        arr = []
        
        # Ascending chord progression
        frequencies = [261.63, 329.63, 392.00, 523.25]  # C, E, G, C
        
        for i in range(frames):
            time = float(i) / sample_rate
            wave = 0
            
            for j, freq in enumerate(frequencies):
                note_start = j * 0.2
                if time >= note_start:
                    note_time = time - note_start
                    note_wave = math.sin(2 * math.pi * freq * note_time)
                    note_envelope = max(0, 1 - note_time / 0.4)
                    wave += note_wave * note_envelope * 0.25
            
            arr.append([int(wave * 32767 * 0.3), int(wave * 32767 * 0.3)])
        
        sound = pygame.sndarray.make_sound(np.array(arr, dtype=np.int16))
        return sound
    
    def generate_dock_sound(self):
        """Generate docking sound effect"""
        sample_rate = 22050
        duration = 1.5
        frames = int(duration * sample_rate)
        arr = []
        
        for i in range(frames):
            time = float(i) / sample_rate
            
            # Mechanical docking sound
            if time < 0.5:
                # Approach phase
                freq = 150 + time * 50
                wave = math.sin(2 * math.pi * freq * time) * 0.3
            elif time < 1.0:
                # Contact phase
                freq = 200
                wave = math.sin(2 * math.pi * freq * time) * 0.4
                # Add some mechanical noise
                if int(time * 20) % 2:
                    wave += 0.1
            else:
                # Lock phase
                freq = 300
                wave = math.sin(2 * math.pi * freq * time) * 0.2
            
            envelope = max(0, 1 - (time - 0.5) / 1.0) if time > 0.5 else 1
            arr.append([int(wave * envelope * 32767 * 0.3), int(wave * envelope * 32767 * 0.3)])
        
        sound = pygame.sndarray.make_sound(np.array(arr, dtype=np.int16))
        return sound
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if sound_name in self.sounds:
            sound = self.sounds[sound_name]
            sound.set_volume(self.sfx_volume)
            sound.play()
    
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)