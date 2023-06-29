import pygame
import csv
from save_data import save_to_file

import button
import game
from game import *
import cProfile
import tracemalloc  # FOR MEMORY PROFILING

class Settings:
    framerate = 60
    width = 800
    height = 600
    window = pygame.display.set_mode((width, height))
    font = pygame.font.SysFont("arialblack", 40)
    h_font = pygame.font.SysFont("arialblack", 20)

class HomeScreen():

    def __init__(self):
        self._logo_img = pygame.image.load("assets/img/pacmanLogo.png")
        self._newGame_img = pygame.image.load("assets/img/newGame2.png").convert_alpha()
        self._highscore_img = pygame.image.load("assets/img/highscores.png").convert_alpha()
        self._quit_img = pygame.image.load("assets/img/quit.png").convert_alpha()
        self._level1_img = pygame.image.load('assets/img/back.png').convert_alpha()
        self._level2_img = pygame.image.load('assets/img/back.png').convert_alpha()
        # level3_img = pygame.image.load('assets/level3.png').convert_alpha()
        self._back_img = pygame.image.load('assets/img/back.png').convert_alpha()

        #create button instances
        self._logo_button = button.Button(63.5, -75, self._logo_img, 1)
        self.newGame_button = button.Button(285.5, 225, self._newGame_img, 1)
        self.highscore_button = button.Button(283.5, 325, self._highscore_img, 1)
        self.quit_button = button.Button(325, 415, self._quit_img, 1)
        self.level1_button = button.Button(550, 250, self._level1_img, 1)
        self.level2_button = button.Button(550, 350, self._level2_img, 1)
        # level3_button = button.Button(311, 325, level3_img, 1)
        # back_button = button.Button(settings.width * .4, 475, back_img, 1)
        self.back_button = button.Button(800 * .4, 475, self._back_img, 1)


        # filepath = "save_data/hi_scores.csv"
        # save = save_to_file.SaveToFile(filepath)
        # display_score = True

    def draw(self, window):
        window.fill(BLACK)  # Replaces game content
        self._logo_button.draw(window)
        self.newGame_button.draw(window)
        self.highscore_button.draw(window)
        self.quit_button.draw(window)
        self.level1_button.draw(window)
        self.level2_button.draw(window)

def main():
    '''
        Default Inits
    '''
    settings = Settings()
    home_screen = HomeScreen()


    # Init vars
    clock = pygame.time.Clock()  # For binding refresh rate and framerate
    running = True
    game_state = "Start"
    game_loop = game.Game(settings.window, 1)
    can_select_level = True

    # Main event loop
    while running:
        clock.tick(settings.framerate)

        # If user quits application
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if home_screen.level1_button.is_drawn() and can_select_level:
            print("level 1")
            game_loop.change_level(1)

        elif home_screen.level2_button.is_drawn() and can_select_level:
            print("level 2")
            game_loop.change_level(2)

        # Window States
        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_SPACE] or home_screen.newGame_button.is_drawn():
            game_loop.game_board_init()
            game_state = "Game"
            can_select_level = False

        if game_loop.game_over:
            game_loop.game_over = False
            game_state = "Start"

        if home_screen.highscore_button.is_drawn():
            game_state = "Highscore"

        # if user presses the back button  or space bar go back to Start window
        if home_screen.back_button.is_drawn() or key_input[pygame.K_SPACE]:
            game_state = "Start"

        # if user presses the button or hits the key "q" end the game
        if home_screen.quit_button.is_drawn() or key_input[pygame.K_q]:
            running = False

        update(game_state, game_loop, home_screen, settings)

    pygame.quit()

# Update what is being displayed  on screen
# Manages screen states
def update(game_state, game_loop, home_screen, settings):  # TODO: Not sure that I like these params

    if game_state == "Start":
        game_loop.points = 0  # TODO: Want this reset in game class
        home_screen.draw(settings.window)

    elif game_state == "Game":
        game_loop.update()

    elif game_state == "Highscore":
        highscore_window(settings)


    pygame.display.update()


# def start_window():
#     global can_select_level
#     can_select_level = True
#     window.fill(BLACK)  # Replaces game content
#     logo_button.draw(window)
#     newGame_button.draw(window)
#     highscore_button.draw(window)
#     quit_button.draw(window)
#     level1_button.draw(window)
#     level2_button.draw(window)


# TODO: Put in own class
call_reader = 0
score = ""
score_list = []
def highscore_window(settings):
    global call_reader
    global score_list
    global width, height
    score_pos = 150
    settings.window.fill(BLACK)
    hi_score_text = font.render("High Scores", True, (255, 255, 255))
    settings.window.blit(hi_score_text, (width * .35, 100))

    if call_reader == 0:
        score_list = save.get_all_hi_scores()
        call_reader = 1

    # display the scores
    for user in score_list:
        score_pos += 50

        # Username
        user_score = font.render(user[0], True, (255, 255, 255))
        settings.window.blit(user_score, (width * .3, score_pos))

        # Score
        user_score = font.render(user[1], True, (255, 255, 255))
        settings.window.blit(user_score, (width * .6, score_pos))

    # back_button.draw(settings.window)


if __name__ == "__main__":
    main()
