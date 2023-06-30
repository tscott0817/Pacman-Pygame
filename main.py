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
    sound_start_time = -1  # Probably don't leave in settings

def main():
    '''
        Default Inits
    '''
    settings = Settings()
    window = pygame.display.set_mode((settings.width, settings.height), pygame.SRCALPHA)
    # window = pygame.Surface((settings.width, settings.height), pygame.SRCALPHA)

    home_screen = HomeScreen(window)
    ls_screen = LevelSelectScreen(window)
    hs_screen = HighscoresScreen(window)
    game_loop = game.Game(window)
    game_state = "Home"
    clock = pygame.time.Clock()  # For binding refresh rate and framerate
    last_timestamp = pygame.time.get_ticks()  # Tracks
    running = True
    pygame.mixer.init()
    pygame.font.init()
    pygame.display.init()

    '''
        Sounds
    '''
    sound_menu = pygame.mixer.Sound("assets/audio/intermission.wav")
    def play_sound(self, sound, wait_time):
        global last_timestamp  # TODO: Would prefer to not use global (Please python let me use pointers)
        current_time = pygame.time.get_ticks()
        if current_time - last_timestamp >= wait_time:
            pygame.mixer.Sound.play(sound)
            pygame.mixer.music.stop()
            last_timestamp = current_time
        return last_timestamp  # TODO: Might have to do this since not member vars (not a class)

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
        if ls_screen.level1_button.is_clicked():
            print("level 1")
            game_loop.change_level(1)

        elif ls_screen.level2_button.is_clicked():
            print("level 2")
            game_loop.change_level(2)

        '''
            Screen States
        '''
        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_ESCAPE]:  # Always go back to home if ESC pressed
            # TODO: Need different approach, playing sound from most objects, want centralized control
            pygame.mixer.Sound.stop(game_loop.background_music)
            pygame.mixer.Sound.stop(game_loop.game_start_sound)
            game_state = "Home"

        if game_state == "Home":  #
            if home_screen.new_game_button.is_clicked():
                game_state = "Game"
            elif home_screen.level_select_button.is_clicked():
                game_state = "Level"
            elif home_screen.highscore_button.is_clicked():
                game_state = "Highscore"
            elif home_screen.quit_button.is_clicked() or key_input[pygame.K_q]:
                running = False

        if game_loop.game_over:
            game_loop.game_over = False
            game_state = "Home"  # TODO: Will want to alter logic here to just go to next level

        # if user presses the back button  or space bar go back to Start window
        if hs_screen.back_button.is_clicked():
            game_state = "Home"

        # if ls_screen.back_button.is_clicked():
        #     game_state = "Home"

        update(window, game_state, game_loop, home_screen, ls_screen, hs_screen)

    pygame.quit()


def update(window, game_state, game_loop, home_screen, ls_screen, hs_screen):  # TODO: Not sure that I like these params
    if game_state == "Home":
        home_screen.draw(window)
    elif game_state == "Game":
        game_loop.update()
    elif game_state == "Level":
        ls_screen.draw(window)
    elif game_state == "Highscore":
        hs_screen.draw(window)
    pygame.display.update()


class HomeScreen:
    def __init__(self, window):
        self.window = window
        self._logo_img = pygame.image.load("assets/img/logo4.png")
        self._new_game_img = pygame.image.load("assets/img/newGame2.png").convert_alpha()
        self._highscore_img = pygame.image.load("assets/img/highscores.png").convert_alpha()
        self._quit_img = pygame.image.load("assets/img/quit.png").convert_alpha()

        self._logo_button = button.Button(self.window, 400, 125, 0, 0, self._logo_img, 1, 'textured', 0)
        self.new_game_button = button.Button(self.window, 400, 225, 300, 75, self._new_game_img, 1, 'solid', 'Play')
        self.level_select_button = button.Button(self.window, 400, 325, 300, 75, self._new_game_img, 1, 'solid', 'Select Level')
        self.highscore_button = button.Button(self.window, 400, 425, 300, 75, self._highscore_img, 1, 'solid', 'Highscores')
        self.quit_button = button.Button(self.window, 400, 525, 300, 75, self._quit_img, 1, 'solid', 'Quit')
        # Load a custom cursor image
        # self.cursor_hover_image = pygame.image.load('cursor.png')
        # self.cursor_data, self.cursor_mask = pygame.cursors.compile(self.cursor_hover_image, black='.', white='X', xor='o')

    def draw(self, window):
        window.fill((25, 25, 25))  # Replaces game content
        self._logo_button.draw()
        self.new_game_button.draw()
        self.level_select_button.draw()
        self.highscore_button.draw()
        self.quit_button.draw()

        if self._logo_button.hover():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif self.new_game_button.hover():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif self.level_select_button.hover():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif self.highscore_button.hover():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif self.quit_button.hover():
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

class LevelSelectScreen:
    def __init__(self, window):
        self.window = window
        self._level1_img = pygame.image.load('assets/img/back.png').convert_alpha()
        self._level2_img = pygame.image.load('assets/img/back.png').convert_alpha()
        self.level1_button = button.Button(self.window, 400, 50, 300, 75, self._level1_img, 1, 'solid', 'Level 1')
        self.level2_button = button.Button(self.window, 400, 150, 300, 75, self._level2_img, 1, 'solid', 'Level 2')
        self.back_img = pygame.image.load('assets/img/back.png').convert_alpha()
        self.back_button = button.Button(window, 100, 550, 300, 75, self.back_img, 1, 'solid', 'Back')

    def draw(self, window):
        window.fill((25, 25, 25))  # Replaces game content
        self.level1_button.draw()
        self.level2_button.draw()
        self.back_button.draw()


# TODO: Put in own class
class HighscoresScreen:
    def __init__(self, window):
        pygame.font.init()
        self.call_reader = 0
        self.score = ""
        self.score_list = []
        self.filepath = "save_data/hi_scores.csv"
        self.save = save_to_file.SaveToFile(self.filepath)
        self.display_score = True
        self.back_img = pygame.image.load('assets/img/back.png').convert_alpha()
        self.back_button = button.Button(window, 100, 550, 300, 75, self.back_img, 1, 'solid', 'Back')
        self.hi_score_text = pygame.font.Font('freesansbold.ttf', 32).render("High Scores", True, (255, 255, 255))
        # self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.font = pygame.font.SysFont("arialblack", 40)
        self.h_font = pygame.font.SysFont("arialblack", 20)

    def draw(self, window):
        score_position = 150
        window.fill((25, 25, 25))
        window.blit(self.hi_score_text, (800 * .35, 100))

        if self.call_reader == 0:
            self.score_list = save.get_all_hi_scores()
            self.call_reader = 1

        # display the scores
        for user in self.score_list:
            score_position += 50

            # Username
            user_score = self.font.render(user[0], True, (255, 255, 255))
            window.blit(user_score, (800 * .3, score_position))

            # Score
            user_score = self.font.render(user[1], True, (255, 255, 255))
            window.blit(user_score, (800 * .6, score_position))

        self.back_button.draw()


if __name__ == "__main__":
    main()
