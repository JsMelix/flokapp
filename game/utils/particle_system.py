"""Particle system for visual effects"""
import pygame
import math
import random
from game.constants import *

class Particle:
    def __init__(self, x, y, velocity_x, velocity_y, color, life, size=2):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.color = color
        self.life = life
        self.max_life = life
        self.size = size
        self.gravity = 0
    
    def update(self, dt):
        """Update particle position and life"""
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.velocity_y += self.gravity * dt
        self.life -= dt
        return self.life > 0
    
    def render(self, screen):
        """Render the particle"""
        if self.life > 0:
            # Fade alpha based on remaining life
            alpha_ratio = self.life / self.max_life
            alpha = int(255 * alpha_ratio)
            
            # Create surface with per-pixel alpha
            particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            color_with_alpha = (*self.color, alpha)
            pygame.draw.circle(particle_surface, self.color, (self.size, self.size), self.size)
            
            screen.blit(particle_surface, (int(self.x - self.size), int(self.y - self.size)))

class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def add_explosion(self, x, y, color=WHITE, count=20):
        """Add explosion particles"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed
            life = random.uniform(0.5, 1.5)
            size = random.randint(2, 4)
            
            particle = Particle(x, y, velocity_x, velocity_y, color, life, size)
            self.particles.append(particle)
    
    def add_thrust_particles(self, x, y, direction_angle, color=RED, count=5):
        """Add rocket thrust particles"""
        for _ in range(count):
            # Particles go opposite to thrust direction
            angle = direction_angle + math.pi + random.uniform(-0.5, 0.5)
            speed = random.uniform(100, 200)
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed
            life = random.uniform(0.3, 0.8)
            size = random.randint(1, 3)
            
            particle = Particle(x, y, velocity_x, velocity_y, color, life, size)
            particle.gravity = 50  # Slight gravity effect
            self.particles.append(particle)
    
    def add_scan_particles(self, x, y, radius=50, color=CYAN):
        """Add scanning effect particles"""
        count = 15
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            start_radius = radius * 0.8
            end_radius = radius * 1.2
            
            start_x = x + math.cos(angle) * start_radius
            start_y = y + math.sin(angle) * start_radius
            
            # Particles move outward
            velocity_x = math.cos(angle) * 80
            velocity_y = math.sin(angle) * 80
            life = 1.0
            size = 2
            
            particle = Particle(start_x, start_y, velocity_x, velocity_y, color, life, size)
            self.particles.append(particle)
    
    def add_warp_particles(self, x, y, color=PURPLE, count=30):
        """Add warp/teleport effect particles"""
        for _ in range(count):
            # Spiral pattern
            angle = random.uniform(0, 4 * math.pi)
            radius = random.uniform(10, 60)
            
            start_x = x + math.cos(angle) * radius
            start_y = y + math.sin(angle) * radius
            
            # Particles converge to center
            velocity_x = (x - start_x) * 2
            velocity_y = (y - start_y) * 2
            life = random.uniform(0.5, 1.0)
            size = random.randint(1, 3)
            
            particle = Particle(start_x, start_y, velocity_x, velocity_y, color, life, size)
            self.particles.append(particle)
    
    def add_success_particles(self, x, y):
        """Add celebration particles"""
        colors = [YELLOW, GREEN, CYAN, WHITE]
        for _ in range(40):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(80, 180)
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed - 50  # Slight upward bias
            
            color = random.choice(colors)
            life = random.uniform(1.0, 2.0)
            size = random.randint(2, 5)
            
            particle = Particle(x, y, velocity_x, velocity_y, color, life, size)
            particle.gravity = 100  # Gravity for firework effect
            self.particles.append(particle)
    
    def update(self, dt):
        """Update all particles"""
        self.particles = [p for p in self.particles if p.update(dt)]
    
    def render(self, screen):
        """Render all particles"""
        for particle in self.particles:
            particle.render(screen)
    
    def clear(self):
        """Clear all particles"""
        self.particles.clear()