"""Mission objectives and educational content"""
import pygame
import random
from game.constants import *

class MissionObjective:
    def __init__(self, objective_type, target_planet=None):
        self.type = objective_type
        self.target_planet = target_planet
        self.completed = False
        self.progress = 0
        self.max_progress = 100
        
        # Educational questions based on mission type
        self.questions = self.generate_questions()
        self.current_question = 0
        
    def generate_questions(self):
        """Generate educational questions based on mission type"""
        question_bank = {
            EXPLORATION: [
                {
                    'question': 'What is the average distance from Earth to Mars?',
                    'options': ['225 million km', '54.6 million km', '401 million km', '150 million km'],
                    'correct': 0,
                    'explanation': 'Mars is on average 225 million km from Earth, but this varies greatly due to orbital mechanics.'
                },
                {
                    'question': 'Which rover was the first to successfully land on Mars?',
                    'options': ['Curiosity', 'Sojourner', 'Opportunity', 'Perseverance'],
                    'correct': 1,
                    'explanation': 'Sojourner was part of the Mars Pathfinder mission in 1997, the first successful rover on Mars.'
                }
            ],
            RESEARCH: [
                {
                    'question': 'What method do we use to detect exoplanets?',
                    'options': ['Direct imaging', 'Transit method', 'Radial velocity', 'All of the above'],
                    'correct': 3,
                    'explanation': 'Scientists use multiple methods including transit photometry, radial velocity, and direct imaging.'
                },
                {
                    'question': 'What is the habitable zone around a star?',
                    'options': ['Where life exists', 'Where water can be liquid', 'The asteroid belt', 'The magnetic field'],
                    'correct': 1,
                    'explanation': 'The habitable zone is where temperatures allow liquid water to exist on a planet\'s surface.'
                }
            ],
            COLLABORATION: [
                {
                    'question': 'How many countries participate in the ISS program?',
                    'options': ['5', '15', '25', '50'],
                    'correct': 1,
                    'explanation': 'The ISS is a collaboration between 15 countries including USA, Russia, Japan, Canada, and 11 European nations.'
                }
            ],
            PROBLEM_SOLVING: [
                {
                    'question': 'What is the main threat from near-Earth asteroids?',
                    'options': ['Radiation', 'Impact collision', 'Gravitational pull', 'Magnetic interference'],
                    'correct': 1,
                    'explanation': 'The primary concern is potential impact with Earth, which could cause significant damage.'
                }
            ]
        }
        
        return question_bank.get(self.type, question_bank[EXPLORATION])
    
    def get_current_question(self):
        """Get the current question data"""
        if self.current_question < len(self.questions):
            return self.questions[self.current_question]
        return None
    
    def answer_question(self, answer_index):
        """Process answer and return if correct"""
        question = self.get_current_question()
        if question:
            is_correct = answer_index == question['correct']
            if is_correct:
                self.progress += 25
                self.current_question += 1
            return is_correct, question['explanation']
        return False, ""
    
    def is_complete(self):
        """Check if objective is complete"""
        return self.progress >= self.max_progress or self.current_question >= len(self.questions)