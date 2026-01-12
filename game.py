import pygame
from sys import exit
from constants import *
from random import randint, choice
from player import Player
from laser import Laser
from obstacle import Obstacle


class Game:
    def __init__(self):
        # Init game
        pygame.init()
        
        # Set clock
        self.clock = pygame.time.Clock()

        # Display Screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Laser jumper")

        # Vars
        self.game_active = False
        self.welcome_screen = True
        self.difficulty = None
        self.player_lives = PLAYER_LIVES



        # Set backgroud
        self.ground_surface = pygame.image.load(BACKGROUND_IMG).convert()
        self.ground_surface = pygame.transform.scale(self.ground_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Set font
        self.font = pygame.font.Font(FONT, 32)

        # Set score
        self.score = 0
        self.start_time = 0
        self.high_score = 0
        
        # Set player and enemy
        self.player = Player(PLAYER_LIVES)
        self.laser = pygame.sprite.Group()
        
        self.laser.add(Laser(0))
        
        self.obstacle_group = pygame.sprite.Group()
        self.obstacle_group.add(Obstacle())
     
        self.timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer, choice(range(600, 1500)))

        self.board_timer = pygame.USEREVENT + 2

        # Track which music is currently playing: "game" or "over"
        self.music_state = None

        self.background_x1 = 0
        self.background_x2 = self.ground_surface.get_width()
        self.scroll_speed = BOARD_SPEED

        # Obstacle
        self.obstacle_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.obstacle_timer, 1200)  # spawn every 1.2s


    # Display score
    def draw_score(self, text):
        display_score_surface = self.font.render(f"{text}: {self.score}", False, (168, 50, 145))
        display_score_rect = display_score_surface.get_rect(midtop = (SCREEN_WIDTH /2, 100))
        self.screen.blit(display_score_surface, display_score_rect)

    # Helper: play music only when switching states
    def play_music(self, state):
        # state should be "game" or "over"
        if self.music_state == state:
            return  # already playing correct music

        pygame.mixer.music.stop()

        if state == "game":
            pygame.mixer.music.load(AUDIO_TRACK)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(.4)

        if state == "over":
            pygame.mixer.music.load(GAME_OVER_AUDIO)
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(.4)

        self.music_state = state

    # Game Over
    def draw_game_over(self):
        # Switch to game-over
        self.play_music("over")

        self.screen.fill((94, 129, 162))
        self.draw_score("Your Score")

        # Print text to play again
        display_restart_game_surface = self.font.render(PLAY_AGAIN_STR, False, (168, 50, 145))
        display_restart_game_rect = display_restart_game_surface.get_rect(midbottom = (SCREEN_WIDTH / 2, 340))
        self.screen.blit(display_restart_game_surface, display_restart_game_rect)

        # Display high score
        high_score_font = pygame.font.Font(FONT, 64)
        high_score_surface = high_score_font.render(f"High Score: {self.high_score}", False, (168, 50, 145))
        high_score_rect = high_score_surface.get_rect(midbottom = (SCREEN_WIDTH / 2, 60))
        self.screen.blit(high_score_surface, high_score_rect)

    # Calc score
    def calculate_score(self):
        self.score = int((pygame.time.get_ticks() - self.start_time ) / 500)
        
        if self.score > self.high_score:
            self.high_score = self.score
    
    def scroll_background(self):
        width = self.ground_surface.get_width()

        self.background_x1 -= self.scroll_speed
        self.background_x2 -= self.scroll_speed

        if self.background_x1 <= -width:
            self.background_x1 = self.background_x2 + width

        if self.background_x2 <= -width:
            self.background_x2 = self.background_x1 + width

        self.screen.blit(self.ground_surface, (self.background_x1, 0))
        self.screen.blit(self.ground_surface, (self.background_x2 - 1, 0))

    # Handle user input
    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if self.welcome_screen:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.difficulty = 0
                        self.welcome_screen = False
                        self.game_active = True
                        self.start_time = pygame.time.get_ticks()
                        pygame.time.set_timer(self.obstacle_timer, 1200)

                    if event.key == pygame.K_2:
                        self.difficulty = 1
                        self.welcome_screen = False
                        self.game_active = True
                        self.start_time = pygame.time.get_ticks()
                        pygame.time.set_timer(self.obstacle_timer, 1200)


                    if event.key == pygame.K_3:
                        self.difficulty = 2
                        self.welcome_screen = False
                        self.game_active = True
                        self.start_time = pygame.time.get_ticks()
                        pygame.time.set_timer(self.obstacle_timer, 1200)

            

            elif not self.game_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_to_welcome()
            
            elif event.type == self.timer and self.game_active:
                if self.difficulty == 0:
                    self.laser.add(Laser(0))
                elif self.difficulty == 1:
                    self.laser.add(Laser(1))
                else:
                    self.laser.add(Laser(2))


                if self.difficulty == 0:
                    pygame.time.set_timer(self.timer, choice(range(600, 1500)))
                elif self.difficulty == 1:
                    pygame.time.set_timer(self.timer, choice(range(500, 1100)))
                else:
                    pygame.time.set_timer(self.timer, choice(range(300, 800)))
            
            elif event.type == self.obstacle_timer and self.game_active:
                if len(self.obstacle_group) == 0:
                    self.obstacle_group.add(Obstacle())
                else:
                    # find rightmost obstacle
                    rightmost_x = max(o.rect.right for o in self.obstacle_group.sprites())

                    # only spawn if there is enough space
                    if rightmost_x < SCREEN_WIDTH - MIN_OBSTACLE_GAP:
                        self.obstacle_group.add(Obstacle())


            else: pass

    def reset_to_welcome(self):
        self.game_active = False
        self.welcome_screen = True
        self.difficulty = None
        self.score = 0
        self.start_time = 0

        self.player = Player(PLAYER_LIVES)

        self.laser.empty()
        self.obstacle_group.empty()

        pygame.time.set_timer(self.obstacle_timer, 0)  # stop obstacle spawns

        pygame.mixer.music.stop()
        self.music_state = None

        self.background_x1 = 0
        self.background_x2 = self.ground_surface.get_width()


    def draw_welcome_screen(self):
        self.screen.fill((94, 129, 162))
        welcome_font = pygame.font.Font(FONT, 60)
        welcome_surface = welcome_font.render("Welcome to the laser game!!", False, (168, 50, 145))
        welcome_rect = welcome_surface.get_rect(midtop = (SCREEN_WIDTH /2, 50))
        self.screen.blit(welcome_surface, welcome_rect)

        level_choice_font = pygame.font.Font(FONT, 40)
        level_choice_surface = level_choice_font.render(LEVEL_CHOICE_STR, False, (168, 50, 145))
        level_choice_rect = level_choice_surface.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen.blit(level_choice_surface, level_choice_rect)
    

    #  Display changes based on events
    def update(self):


        if self.game_active:
            # Ensure game music is playing (only switches once)
            self.play_music("game")

            
            self.calculate_score()

            #
            self.player.update()


            self.laser.update()
      
            self.obstacle_group.update()
            
            if pygame.sprite.spritecollideany(self.player, self.laser):
                self.player.try_take_damage()
        
            if self.player.player_lives < 1:
                self.game_active = False
   

        else:
            pass

    def draw(self):
        if self.welcome_screen:
            self.draw_welcome_screen()
            

        elif self.game_active:
            self.scroll_background()
            self.player.draw_player_lives(self.screen)
            self.player.draw(self.screen)

            self.laser.draw(self.screen)          

            # if self.difficulty == 1:
            #     self.laser_medium.draw(self.screen)
            
            # if self.difficulty == 2:
            #     self.laser_medium.draw(self.screen)
            #     self.laser_hard.draw(self.screen)
            
            self.draw_score("Current Score")

            self.obstacle_group.draw(self.screen)
       
        else:
            self.draw_game_over()

    


    # Main
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(60)


Game().run()
