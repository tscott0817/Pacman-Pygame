import time

import pygame
import csv
from save_data import save_to_file
import button
import game
from game import *
import cProfile
import tracemalloc  # FOR MEMORY PROFILING


'''
    Initial Setup Values; Acting as Namespace
'''
class Settings:
    framerate = 60
    width = 800
    height = 600
    last_timestamp = 0
    sound_start_time = -1
    # window = pygame.display.set_mode((width, height))

def main():
    '''
        Default Inits
    '''
    settings = Settings()
    window = pygame.display.set_mode((settings.width, settings.height))

    home_screen = HomeScreen()
    hs_screen = HighscoresScreen()
    game_loop = game.Game(window)
    game_state = "Home"
    clock = pygame.time.Clock()  # For binding refresh rate and framerate
    running = True

    '''
        Sounds
    '''
    sound_menu = pygame.mixer.Sound("assets/audio/intermission.wav")

    def playSound(sound, wait_time):

        current_time = pygame.time.get_ticks()
        if current_time - settings.last_timestamp >= wait_time:
            pygame.mixer.Sound.play(sound)
            pygame.mixer.music.stop()
            settings.last_timestamp = current_time
            pygame.time.set_timer(pygame.USEREVENT, wait_time)


    # Main event loop
    while running:
        clock.tick(settings.framerate)

        # If user quits application
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        '''
            Sound
        '''
        # current_time = pygame.time.get_ticks()
        # if current_time - settings.sound_start_time >= sound_menu.get_length() * 1000:
        #     playSound(sound_menu, 5000)  # Play sound again once it has finished

        '''
            Select Level
        '''
        if home_screen.level1_button.is_drawn():
            print("level 1")
            game_loop.change_level(1)

        elif home_screen.level2_button.is_drawn():
            print("level 2")
            game_loop.change_level(2)

        '''
            Screen States
        '''
        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_ESCAPE]:  # Always go back to home if ESC pressed
            game_state = "Home"

        if game_state == "Home":  #
            if home_screen.new_game_button.is_drawn():
                game_state = "Game"
            elif home_screen.highscore_button.is_drawn():
                game_state = "Highscore"
            elif home_screen.quit_button.is_drawn() or key_input[pygame.K_q]:
                running = False

        if game_loop.game_over:
            game_loop.game_over = False
            game_state = "Home"  # TODO: Will want to alter logic here to just go to next level

        # if user presses the back button  or space bar go back to Start window
        if hs_screen.back_button.is_drawn() or key_input[pygame.K_ESCAPE]:
            game_state = "Home"

        update(window, game_state, game_loop, home_screen, hs_screen)

    pygame.quit()


def update(window, game_state, game_loop, home_screen, hs_screen):  # TODO: Not sure that I like these params
    if game_state == "Home":
        home_screen.draw(window)
    elif game_state == "Game":
        game_loop.update()
    elif game_state == "Highscore":
        hs_screen.draw(window)
    pygame.display.update()


class HomeScreen:
    def __init__(self):
        self._logo_img = pygame.image.load("assets/img/logo4.png")
        self._new_game_img = pygame.image.load("assets/img/newGame2.png").convert_alpha()
        self._highscore_img = pygame.image.load("assets/img/highscores.png").convert_alpha()
        self._quit_img = pygame.image.load("assets/img/quit.png").convert_alpha()
        self._level1_img = pygame.image.load('assets/img/back.png').convert_alpha()
        self._level2_img = pygame.image.load('assets/img/back.png').convert_alpha()

        self._logo_button = button.Button(20, 25, self._logo_img, 1)
        self.new_game_button = button.Button(285.5, 225, self._new_game_img, 1)
        self.highscore_button = button.Button(283.5, 325, self._highscore_img, 1)
        self.quit_button = button.Button(325, 415, self._quit_img, 1)
        self.level1_button = button.Button(550, 250, self._level1_img, 1)
        self.level2_button = button.Button(550, 350, self._level2_img, 1)

    def draw(self, window):
        window.fill((25, 25, 25))  # Replaces game content
        self._logo_button.draw(window)
        self.new_game_button.draw(window)
        self.highscore_button.draw(window)
        self.quit_button.draw(window)
        self.level1_button.draw(window)
        self.level2_button.draw(window)


# TODO: Put in own class
class HighscoresScreen:
    def __init__(self):
        self.call_reader = 0
        self.score = ""
        self.score_list = []
        self.filepath = "save_data/hi_scores.csv"
        self.save = save_to_file.SaveToFile(self.filepath)
        self.display_score = True
        self.back_img = pygame.image.load('assets/img/back.png').convert_alpha()
        self.back_button = button.Button(25, 500, self.back_img, 1)
        self.hi_score_text = font.render("High Scores", True, (255, 255, 255))
        self.font = pygame.font.SysFont("arialblack", 40)
        self.h_font = pygame.font.SysFont("arialblack", 20)

    def draw(self, window):
        score_position = 150
        window.fill(BLACK)
        window.blit(self.hi_score_text, (800 * .35, 100))

        if self.call_reader == 0:
            self.score_list = save.get_all_hi_scores()
            self.call_reader = 1

        # display the scores
        for user in self.score_list:
            score_position += 50

            # Username
            user_score = font.render(user[0], True, (255, 255, 255))
            window.blit(user_score, (800 * .3, score_position))

            # Score
            user_score = font.render(user[1], True, (255, 255, 255))
            window.blit(user_score, (800 * .6, score_position))

        self.back_button.draw(window)


if __name__ == "__main__":
    main()
