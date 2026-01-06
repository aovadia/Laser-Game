import pygame
from constants import *
from random  import randint

class Laser(pygame.sprite.Sprite):


    def __init__(self, difficulty):
        super().__init__()
        self.difficulty = difficulty
        self.__choice = randint(0,2)
        
        if self.__choice == 0 or self.difficulty == 0:
            self.image = pygame.image.load(LASER_IMG).convert_alpha()
            self.image = pygame.transform.scale(self.image, LASER_SCALE_TUPLE)
            self.image = pygame.transform.rotate(self.image, 90)
        else:
            self.image = pygame.image.load(FAST_LASER_IMG).convert_alpha()
            self.image = pygame.transform.scale(self.image, FASTER_LASER_SCALE_TUPLE)
            self.image = pygame.transform.rotate(self.image, 90)            

        laser_y = randint(SPAWN_PADDING, SCREEN_HEIGHT - SPAWN_PADDING)
        self.rect = self.image.get_rect(midleft=(SCREEN_WIDTH, laser_y))
        self.velocity = randint(VELOCITY_MIN, VELOCITY_MAX)



    def move(self):
        if self.difficulty == 0:
            self.rect.x -= self.velocity * SPEED_MULTIPLIER
        elif self.difficulty == 1:
            self.rect.x -= self.velocity * SPEED_MULTIPLIER_MEDIUM
        else:
            self.rect.x -= self.velocity * SPEED_MULTIPLIER_HARD

    def update(self):
        self.move()
        self.destroy()


    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
