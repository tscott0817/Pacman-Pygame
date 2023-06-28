import pygame
import csv
from save_data import save_to_file

import button
import game
from game import *
import cProfile

import tracemalloc  # FOR MEMORY PROFILING

FRAMERATE = 60  # Update function tied to framerate, so should stay at 60.
width = 800
height = 600
window = pygame.display.set_mode((width, height))

game_state = ""
game_loop = game.Game(window)
can_select = True
font = pygame.font.SysFont("arialblack", 40)
h_font = pygame.font.SysFont("arialblack", 20)

#load button images
logo_img = pygame.image.load("assets/pacmanLogo.png")
newGame_img = pygame.image.load("assets/newGame2.png").convert_alpha()
highscore_img = pygame.image.load("assets/highscores.png").convert_alpha()
quit_img = pygame.image.load("assets/quit.png").convert_alpha()
# level1_img = pygame.image.load('assets/level1.png').convert_alpha()
# level2_img = pygame.image.load('assets/level2.png').convert_alpha()
# level3_img = pygame.image.load('assets/level3.png').convert_alpha()
back_img = pygame.image.load('assets/back.png').convert_alpha()

#create button instances
logo_button = button.Button(63.5, -75, logo_img, 1)
newGame_button = button.Button(285.5, 225, newGame_img, 1)
highscore_button = button.Button(283.5, 325, highscore_img, 1)
quit_button = button.Button(325, 415, quit_img, 1)
# level1_button = button.Button(311, 75, level1_img, 1)
# level2_button = button.Button(311, 200, level2_img, 1)
# level3_button = button.Button(311, 325, level3_img, 1)
back_button = button.Button(width * .4, 475, back_img, 1)

filepath = "save_data/hi_scores.csv"
save = save_to_file.SaveToFile(filepath)
display_score = True

def main():
    # Init vars
    clock = pygame.time.Clock()  # For binding refresh rate and framerate
    running = True
    global game_state
    game_state = "Start"
    global can_select

    # Main event loop
    while running:
        clock.tick(FRAMERATE)

        # If user quits application
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Window States
        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_SPACE] or newGame_button.is_drawn() and can_select:
            game_loop.game_board_init()
            game_state = "Game"
            can_select = False

        if game_loop.game_over:
            game_loop.game_over = False
            game_state = "Start"

        if highscore_button.is_drawn():
            game_state = "Highscore"

        # if user presses the back button  or space bar go back to Start window
        if back_button.is_drawn() or key_input[pygame.K_SPACE]:
            game_state = "Start"

        # if user presses the button or hits the key "q" end the game
        if quit_button.is_drawn() or key_input[pygame.K_q]:
            running = False

        update()

    pygame.quit()


def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  window.blit(img, (x, y))

# Update what is being displayed  on screen
# Manages screen states
def update():

    # Launches the main game
    global window
    global game_state

    if game_state == "Start":
        game_loop.points = 0  # TODO: Want this reset in game class
        start_window()

    if game_state == "Game":
        game_loop.update()

    if game_state == "Highscore":
        highscore_window()

    pygame.display.update()


def start_window():
    global can_select
    can_select = True
    window.fill(BLACK)  # Replaces game content
    logo_button.draw(window)
    newGame_button.draw(window)
    highscore_button.draw(window)
    quit_button.draw(window)

call_reader = 0
score = ""
score_list = []
def highscore_window():
    global call_reader
    global score_list
    global width, height
    score_pos = 150
    window.fill(BLACK)
    hi_score_text = font.render("High Scores", True, (255, 255, 255))
    window.blit(hi_score_text, (width * .35, 100))

    if call_reader == 0:
        score_list = save.get_all_hi_scores()
        call_reader = 1

    # display the scores
    for user in score_list:
        score_pos += 50

        # Username
        user_score = font.render(user[0], True, (255, 255, 255))
        window.blit(user_score, (width * .3, score_pos))

        # Score
        user_score = font.render(user[1], True, (255, 255, 255))
        window.blit(user_score, (width * .6, score_pos))

    back_button.draw(window)


if __name__ == "__main__":
    main()
