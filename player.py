import pygame
from constants import PLAYER_IMG, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED
class Player:
    def __init__(self):
        self.surface = pygame.image.load(PLAYER_IMG).convert_alpha()
        self.surface = pygame.transform.scale(self.surface, (32, 32))
        self.surface = pygame.transform.rotate(self.surface, 270)
        
        self.rect = self.surface.get_rect(center=(50, 300))

    def move(self, direction):
            if direction == "right":
                self.rect.x += PLAYER_SPEED
            if direction == "left":
                self.rect.x -= PLAYER_SPEED
            if direction == "up":
                self.rect.y -= PLAYER_SPEED
            if direction == "down":
                self.rect.y += PLAYER_SPEED
            
            self.__is_in_bounds()
                        

    def draw(self, screen):
             

        screen.blit(self.surface, self.rect)


    def __is_in_bounds(self):
        if self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        
        if self.rect.top <= 0:
            self.rect.top = 0
        
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        
         