import pygame
from constants import PLAYER_IMG, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, FONT, PLAYER_HIT_AUD
class Player(pygame.sprite.Sprite):
    def __init__(self, player_lives):
        super().__init__()

        self.surface = pygame.image.load(PLAYER_IMG).convert_alpha()
        self.surface = pygame.transform.scale(self.surface, (32, 32))
        self.surface = pygame.transform.rotate(self.surface, 270)
        self.font = pygame.font.Font(FONT, 32)

        
        self.rect = self.surface.get_rect(center=(50, 300))
        self.player_lives = player_lives
        # Set dict for key presses
        self.moving = {
            "up": False,
            "down": False,
            "left": False,
            "right": False
        }
        
        self.last_hit_time = 0
        self.invincibility_ms = 1000  # 1 second of invincibility
        self.flash_time = 120

        self.hit_audio = pygame.mixer.Sound(PLAYER_HIT_AUD)
        self.hit_audio.set_volume(.5)
    def move(self):
            if self.moving["right"]:
                self.rect.x += PLAYER_SPEED
            if self.moving["left"]:
                self.rect.x -= PLAYER_SPEED
            if self.moving["up"]:
                self.rect.y -= PLAYER_SPEED
            if self.moving["down"]:
                self.rect.y += PLAYER_SPEED
            
            self.__is_in_bounds()
                        
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        self.moving["up"] = keys[pygame.K_w]
        self.moving["down"] = keys[pygame.K_s]
        self.moving["left"] = keys[pygame.K_a]
        self.moving["right"] = keys[pygame.K_d]

    def draw(self, screen):
        now = pygame.time.get_ticks()
        invincible = (now - self.last_hit_time) < self.invincibility_ms

        if invincible:
            # blink on/off during invincibility
            visible = ((now - self.last_hit_time) // self.flash_time) % 2 == 0
            if not visible:
                return  # skip drawing this frame

        screen.blit(self.surface, self.rect)


    def update(self):
        self.player_input()
        self.move()

    def __is_in_bounds(self):
        if self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        
        if self.rect.top <= 0:
            self.rect.top = 0
        
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        
    def try_take_damage(self):
        now = pygame.time.get_ticks()
        if now - self.last_hit_time >= self.invincibility_ms:
            self.player_lives -= 1
            self.last_hit_time = now
            self.hit_audio.play()

    def draw_player_lives(self, screen):
        player_lives_surface = self.font.render(f"Lives: {self.player_lives}", False, (168, 50, 145))
        player_lives_rect = player_lives_surface.get_rect(topleft = (25, 35))
        screen.blit(player_lives_surface, player_lives_rect)
