import pygame
from constants import OBSTACLE_IMG
from random import randint
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_SPEED

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(OBSTACLE_IMG).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width(), randint(self.image.get_height() *2, 5 * self.image.get_height())))
        spawn_x = SCREEN_WIDTH + randint(100, 400) 
        self.rect = self.image.get_rect(bottomleft=(spawn_x, SCREEN_HEIGHT))
        
    
        
    def update(self):
        self.rect.x -= BOARD_SPEED
        if self.rect.right < 0:
            self.kill()

    def is_on_screen(self):
        if self.rect.x < -10:
            return False
    
        return True