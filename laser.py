import pygame
from constants import *
from random  import randint

class Laser:
    IMAGE = LASER_IMG
    SCALE_TUPLE = LASER_SCALE_TUPLE
    SPEED_MULTIPLIER = SPEED_MULTIPLIER

    def __init__(self):
        self.surface = pygame.image.load(self.IMAGE).convert_alpha()
        self.surface = pygame.transform.scale(self.surface, self.SCALE_TUPLE)
        self.surface = pygame.transform.rotate(self.surface, 90)

        laser_y = randint(SPAWN_PADDING, SCREEN_HEIGHT - SPAWN_PADDING)
        self.rect = self.surface.get_rect(midleft=(SCREEN_WIDTH, laser_y))
        self.velocity = randint(VELOCITY_MIN, VELOCITY_MAX)

    def move(self):
        self.rect.x -= self.velocity * self.SPEED_MULTIPLIER
        self.is_in_bounds()

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def is_in_bounds(self):
        if self.rect.right <= 0:
            self.rect.left = SCREEN_WIDTH
            self.rect.y = randint(SPAWN_PADDING, SCREEN_HEIGHT - SPAWN_PADDING)
            self.velocity = randint(VELOCITY_MIN, VELOCITY_MAX)


class FastLaser(Laser):
    IMAGE = FAST_LASER_IMG
    SCALE_TUPLE = FASTER_LASER_SCALE_TUPLE
    SPEED_MULTIPLIER = SPEED_MULTIPLIER_FASTER
