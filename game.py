import pygame
from colors import *
import collide
import pacman
import ghost
from save_data import save_to_file
import os
import random
import tracemalloc  # FOR MEMORY PROFILING

# Save data
filepath = "save_data/hi_scores.csv"
save = save_to_file.SaveToFile(filepath)
username = "Joe"  # TODO: This will be entered in by the user

class Game:
    pygame.mixer.init()  # TODO: Would prefer this only in main.py, but doesn't work with Ghost and Pacman class unless here.

    def __init__(self, window):
        self.square = 40
        self.window = window
        self.horizontal_offset = 0
        self.pellet_tick = None
        self.points = 0

        # Board components
        self.all_board_objects = []  # The game objects (rect, circle, etc), each at a tile position
        self.all_board_tiles = []  # The associated matrix coordinates for each board object
        self.traversal_tiles = []  # The possible tiles pacman and the ghosts can travel on
        self.decision_tiles = []  # The tiles where ghost makes decisions
        self.power_pellets = []  # The larger
        self.possible_ghost_directions = []  # Each list holds directions possible from each decision npe
        self.possible_food_locations = []
        self.board = []
        self.time_list = [2000, 5000, 8000]
        self.food_timer_choice = None
        self.can_spawn_food = False
        self.food_choice = None
        self.food_spawn_again = True
        self.food_tick = 0
        self.level = 1
        self.fruit_png = os.path.join('assets/img', 'fruit.png')
        self.life_png = os.path.join('assets/img', 'lives.png')
        self.fruit_img = pygame.image.load(self.fruit_png).convert_alpha()
        self.fruit = pygame.transform.scale(self.fruit_img, (30, 30))

        # Characters
        self.player = pacman.Pacman()
        self.blue_ghost = ghost.Ghost("Blue")
        self.red_ghost = ghost.Ghost("Red")
        self.yellow_ghost = ghost.Ghost("Yellow")
        self.pink_ghost = ghost.Ghost("Pink")

        # Used for resetting pacman after ghost catches it
        self.pacman_spawn_point = None

        # Used to make sure lists are filled once instead of every frame
        self.board_built = False
        self.game_over = False
        self.read_board_from_file()

        # Sounds
        self.game_start_sound = pygame.mixer.Sound("assets/audio/game_start.wav")
        self.background_music = pygame.mixer.Sound("assets/audio/siren_1.wav")
        self.background_music.set_volume(2)
        self.last_timestamp = pygame.time.get_ticks()
        self.frightened_sound = pygame.mixer.Sound("assets/audio/power_pellet.wav")
        self.frightened_sound.set_volume(0.3)

        # Text Stuff
        self.font = pygame.font.Font('freesansbold.ttf', 32)

        # Used so score is only added to file once per game
        self.save_score = True
        self.game_started = False

        self.game_board_init()



    def update(self):

        dead = self.player.die()
        if not dead and not self.game_won():
            self.window.fill(BACK_BLACK)
            self.game_board()
            self.player.move()
            self.player.tunnel_transport()
            self.player.draw(self.window)
            self.blue_ghost.draw(self.window)
            self.red_ghost.draw(self.window)
            self.yellow_ghost.draw(self.window)
            self.pink_ghost.draw(self.window)
            self.spawn_food()  # TODO: Need to re-write this entire function
            self.ghost_swap_state()  # All ghost movement calls are in this function
            self.draw_top()
            self.play_sound(self.background_music, 1550)

            # Sends pacman back to appropriate spawn point once caught by ghost
            # TODO: Don't quite like this approach, but works for right now
            for i, tile in enumerate(self.all_board_tiles):  # Checks all objects and gets the associated tile of the spawn point
                if tile == 0:
                    self.pacman_spawn_point = self.all_board_objects[i]
                i += 1
        else:
            if dead:
                self.draw_dead(200, 285)
                self.spawn_pacman(self.player.pacman_bb)
                self.player.num_lives = 3  # Reset number of lives after each game
                self.reset_board()
                self.player.points = 0
                self.points = 0
                self.game_over = True
                # TODO: Do I need this?
                # pygame.display.update()  # Don't call this outside of if statement, needed for time delay
                pygame.time.delay(5000)

            # global save_score
            if self.game_won():
                self.draw_won(325, 290)
                if self.save_score:
                    save.hi_scores(username, self.points)
                    self.save_score = False
                self.player.points = 0
                self.points = 0
                self.player.num_lives = 3
                self.reset_board()
                self.game_over = True
                self.spawn_pacman(self.player.pacman_bb)
                # Only allow adding score for one frame (will add score continuously otherwise)
                pygame.display.update()  # Don't call this outside of if statement, needed for time delay
                pygame.time.delay(5000)

    def read_board_from_file(self):
        # drawing board by reading files
        filename = "map" + str(self.level) + ".txt"
        game_board = open(filename, 'r')
        for line in game_board:
            row_one = line.split()
            row_new = []
            for num in row_one:
                row_new.append(int(num))
            self.board.append(row_new)

    def game_board_init(self):
        self.player.points = 0
        self.points = 0
        self.game_board()
        self.spawn_pacman(self.player.pacman_bb)
        self.spawn_ghost(self.blue_ghost.ghost_bb)
        self.spawn_ghost(self.red_ghost.ghost_bb)
        self.spawn_ghost(self.yellow_ghost.ghost_bb)
        self.spawn_ghost(self.pink_ghost.ghost_bb)

    def game_board(self):
        # Loop through matrix and place objects at appropriate coordinates
        for i in range(1, len(self.board) - 1):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0: # the initial position of pacman
                    spawn_point = pygame.draw.rect(self.window, GREEN, ((j * self.square) + (self.horizontal_offset), i * self.square, self.square, self.square), 1)

                    # Makes sure these are only added once (Get added every frame otherwise)
                    if not self.board_built:
                        self.all_board_objects.append(spawn_point)
                        self.all_board_tiles.append(self.board[i][j])
                        self.traversal_tiles.append(spawn_point)

                elif self.board[i][j] == 2:
                    tic_tac = pygame.draw.circle(self.window, YELLOW, ((j * self.square + self.square // 2) + (self.horizontal_offset), i * self.square + self.square // 2), self.square // 8)

                    if not self.board_built:
                        self.all_board_objects.append(tic_tac)
                        self.all_board_tiles.append(self.board[i][j])
                        self.traversal_tiles.append(tic_tac)

                    # If tic-tac has been collected then remove from board
                    collected = self.player.collect_points(self.player.pacman_bb, tic_tac, "tic_tac")  # Returns true if collected
                    if collected:
                        self.points = self.player.points
                        self.board[i][j] = 1
                        self.possible_food_locations.append(tic_tac)

                elif self.board[i][j] == 3:
                    wall = pygame.draw.rect(self.window, BLUE, ((j * self.square) + (self.horizontal_offset), i * self.square, self.square, self.square), 1)

                    if not self.board_built:
                        self.all_board_objects.append(wall)
                        self.all_board_tiles.append(self.board[i][j])

                    # Apply collision to between walls and characters
                    collide.collide_objects(self.player.pacman_bb, wall)
                    collide.collide_objects(self.blue_ghost.ghost_bb, wall)
                    collide.collide_objects(self.red_ghost.ghost_bb, wall)
                    collide.collide_objects(self.yellow_ghost.ghost_bb, wall)
                    collide.collide_objects(self.pink_ghost.ghost_bb, wall)

                elif self.board[i][j] == 5: # draw power pellet
                    power_pellet = pygame.draw.circle(self.window, ORANGE_YELLOW, ((j * self.square + self.square // 2) + (self.horizontal_offset), i * self.square + self.square // 2), self.square // 4)

                    if not self.board_built:
                        self.all_board_objects.append(power_pellet)
                        self.all_board_tiles.append(self.board[i][j])
                        self.traversal_tiles.append(power_pellet)

                    # If power-pellet has been collected then remove from board
                    collected = self.player.collect_points(self.player.pacman_bb, power_pellet, "power_pellet")  # Returns true if collected
                    if collected:
                        self.points = self.player.points
                        self.board[i][j] = 1
                        self.blue_ghost.scared = True  # Only need to set one ghost to scared
                        self.pellet_tick = pygame.time.get_ticks()

                        # TODO: Want a better place to start this, make a timer function
                        if self.food_spawn_again:
                            f_choice = random.randint(0, len(self.time_list) - 1)
                            self.food_timer_choice = self.time_list[f_choice]
                            print(self.food_timer_choice)
                            self.food_tick = pygame.time.get_ticks()
                            food_location = random.randint(0, len(self.possible_food_locations) - 1)
                            self.food_choice = self.possible_food_locations[food_location]
                            self.can_spawn_food = True

                elif self.board[i][j] == 6:
                    # For the decision tile list (Need them to be rectangles)
                    # decision_node = pygame.draw.rect(self.window, RED, ((j * self.square) + (self.horizontal_offset), i * self.square, self.square, self.square), 1)
                    decision_node = pygame.draw.rect(self.window, BACK_BLACK, ((j * self.square) + (self.horizontal_offset), i * self.square, self.square, self.square), 1)


                    # What the pacman collects
                    #tic_tac = pygame.draw.circle(self.window, GREEN, ((j * self.square + self.square // 2) + (self.horizontal_offset), i * self.square + self.square // 2), self.square // 4)
                    tic_tac = pygame.draw.circle(self.window, RED, ((j * self.square + self.square // 2) + (self.horizontal_offset), i * self.square + self.square // 2), self.square // 8)

                    if not self.board_built:
                        self.all_board_objects.append(decision_node)
                        self.all_board_tiles.append(self.board[i][j])
                        self.traversal_tiles.append(decision_node)
                        self.decision_tiles.append(decision_node)

                    # Make sure this stays here, caused massive slowdowns otherwise
                    collected = self.player.collect_points(self.player.pacman_bb, tic_tac, "tic_tac")  # Returns true if collected
                    if collected:
                        self.points = self.player.points
                        self.board[i][j] = 7
                    elif self.board[i][j] == 7:
                        # pygame.draw.rect(self.window, RED, ((j * self.square) + (self.horizontal_offset), i * self.square, self.square, self.square), 1)
                        pygame.draw.rect(self.window, BACK_BLACK, ((j * self.square) + (self.horizontal_offset), i * self.square, self.square, self.square), 1)


                elif self.board[i][j] == 9:
                    ghost_spawn = pygame.draw.rect(self.window, RED, ((j * self.square) + (self.horizontal_offset), i * self.square, self.square, self.square), 1)

                    if not self.board_built:
                        self.all_board_objects.append(ghost_spawn)
                        self.all_board_tiles.append(self.board[i][j])
                        self.decision_tiles.append(ghost_spawn)

        self.board_built = True  # Indicates the board has been built at least one time

    def draw_top(self):
        score = self.font.render("Score: " + str(self.points), True, (255, 255, 255))
        self.window.blit(score, (2*self.square, 7.5))

        for i in range(self.player.num_lives):
            lives_img = pygame.image.load(self.life_png).convert_alpha()
            lives = pygame.transform.scale(lives_img, (30, 30))
            self.window.blit(lives, ((17 - i)*self.square, 7.5))

    def draw_won(self, x, y):
        won = self.font.render("You Won!", True, (100, 255, 100))
        self.window.blit(won, (x, y))

    def draw_dead(self, x, y):
        dead = self.font.render("Out Of Lives. Game Over! ", True, (255, 100, 100))
        self.window.blit(dead, (x, y))

    def spawn_food(self):
        current_tick = pygame.time.get_ticks()
        if self.can_spawn_food and current_tick > self.food_tick + self.food_timer_choice and current_tick < self.food_tick + self.food_timer_choice + 5000:
            self.food_spawn_again = False

            if len(self.possible_food_locations) > 0:
                fruit_collectable = self.window.blit(self.fruit, (self.food_choice.x - 7.5, self.food_choice.y - 7.5))
                collected = self.player.collect_points(self.player.pacman_bb, fruit_collectable, "fruit")  # Returns true if collected
                if collected:
                    self.can_spawn_food = False
                    self.food_spawn_again = True

        elif self.can_spawn_food and current_tick > self.food_tick + self.food_timer_choice + 5000:
            self.food_spawn_again = True

    def spawn_pacman(self, pacman_obj):
        index = 0
        for tile in self.all_board_tiles:
            if tile == 0:
                spawn_point = self.all_board_objects[index]
                pacman_obj.center = spawn_point.center
            index += 1

    def spawn_ghost(self, ghost_obj):
        index = 0
        for tile in self.all_board_tiles:
            # TODO: Could use a few of these for each ghost color
            if tile == 9:
                spawn_point = self.all_board_objects[index]
                ghost_obj.center = spawn_point.center
            index += 1

    def ghost_swap_state(self):
        tick_itr = pygame.time.get_ticks()
        # If any ghost is frightened, then they all are
        # If 5 seconds have passed since the ghost have been scared, switch back to chase
        if self.blue_ghost.scared and tick_itr < self.pellet_tick + 5000:
            pygame.mixer.Sound.stop(self.background_music)  # TODO: Seems to work well, do with all sound
            self.blue_ghost.frightened(self.decision_tiles, self.player.pacman_bb)
            self.red_ghost.frightened(self.decision_tiles, self.player.pacman_bb)
            self.yellow_ghost.frightened(self.decision_tiles, self.player.pacman_bb)
            self.pink_ghost.frightened(self.decision_tiles, self.player.pacman_bb)
        else:
            pygame.mixer.Sound.stop(self.blue_ghost.frightened_sound)
            pygame.mixer.Sound.stop(self.red_ghost.frightened_sound)
            pygame.mixer.Sound.stop(self.yellow_ghost.frightened_sound)
            pygame.mixer.Sound.stop(self.pink_ghost.frightened_sound)
            self.blue_ghost.scared = False
            self.blue_ghost.chase(self.decision_tiles, self.player.pacman_bb)
            # self.blue_ghost.scatter(self.decision_tiles)
            self.red_ghost.scared = False
            self.red_ghost.chase(self.decision_tiles, self.player.pacman_bb)
            # self.red_ghost.scatter(self.decision_tiles)
            self.yellow_ghost.scared = False
            self.yellow_ghost.scatter(self.decision_tiles)
            #self.yellow_ghost.chase(self.decision_tiles, self.player.pacman_bb)
            self.pink_ghost.scared = False
            self.pink_ghost.scatter(self.decision_tiles)
            #self.pink_ghost.chase(self.decision_tiles, self.player.pacman_bb)

        if self.blue_ghost.scared:
            self.blue_ghost.eaten = self.player.collect_points(self.player.pacman_bb, self.blue_ghost.mouth, "ghost")
            self.red_ghost.eaten = self.player.collect_points(self.player.pacman_bb, self.red_ghost.mouth, "ghost")
            self.yellow_ghost.eaten = self.player.collect_points(self.player.pacman_bb, self.yellow_ghost.mouth, "ghost")
            self.pink_ghost.eaten = self.player.collect_points(self.player.pacman_bb, self.pink_ghost.mouth, "ghost")

            if self.blue_ghost.eaten:
                self.points = self.player.points
                self.blue_ghost.eaten = False
                pygame.time.delay(1000)
                self.spawn_ghost(self.blue_ghost.ghost_bb)

            elif self.red_ghost.eaten:
                self.points = self.player.points
                self.red_ghost.eaten = False
                pygame.time.delay(1000)
                self.spawn_ghost(self.red_ghost.ghost_bb)

            elif self.yellow_ghost.eaten:
                pygame.time.delay(1000)
                self.spawn_ghost(self.yellow_ghost.ghost_bb)
                self.yellow_ghost.eaten = False

            elif self.pink_ghost.eaten:
                pygame.time.delay(1000)
                self.spawn_ghost(self.pink_ghost.ghost_bb)
                self.pink_ghost.eaten = False

        # If not in the "Frightened" state, then the ghost can eat Pacman
        if not self.blue_ghost.scared:
            pacman_eaten_blue = self.blue_ghost.eat_pacman(self.player.pacman_bb, self.pacman_spawn_point)
            pacman_eaten_red = self.red_ghost.eat_pacman(self.player.pacman_bb, self.pacman_spawn_point)
            pacman_eaten_yellow = self.yellow_ghost.eat_pacman(self.player.pacman_bb, self.pacman_spawn_point)
            pacman_eaten_pink = self.pink_ghost.eat_pacman(self.player.pacman_bb, self.pacman_spawn_point)

            if pacman_eaten_blue or pacman_eaten_red or pacman_eaten_yellow or pacman_eaten_pink:
                self.player.lose_life()

    def play_sound(self, sound, wait_time):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_timestamp >= wait_time:
            pygame.mixer.Sound.play(sound)
            pygame.mixer.music.stop()
            self.last_timestamp = current_time

    def change_level(self, level):
        self.level = level
        self.board = []
        self.read_board_from_file()
        self.game_board_init()
        self.player.num_lives = 3
        self.player.points = 0
        self.points = 0
        self.game_over = False

    # This needs to be checked every frame so can't use the list of tiles
    def game_won(self):
        board_empty = True
        for i in range(0, len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 2 or self.board[i][j] == 5:
                    board_empty = False

        if board_empty:
            return True
        else:
            return False

    def reset_board(self):
        self.board = []
        self.read_board_from_file()

