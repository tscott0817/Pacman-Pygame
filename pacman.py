import pygame
import os


class Pacman:
    # TODO: file paths stored in file
    pacman_png_openMouth = os.path.join('assets',
                                        'pacmanOpenMouth.png')  # Use this because filepaths can be different between OS's (like '/' vs '\')
    pacman_png_CloseMouth = os.path.join('assets', 'pacmanCloseMouth.png')
    points = 0
    pygame.display.init()
    pygame.display.set_mode((800, 600))

    def __init__(self):
        self.PACMAN_IMG = pygame.image.load(self.pacman_png_openMouth).convert_alpha()
        self.PACMAN = pygame.transform.scale(self.PACMAN_IMG,
                                             (30, 30))  # For resizing images, needs to be same size as bounding box
        self.PACMAN_BB = pygame.Rect(600, 200, 40,
                                     40)  # The 'Bounding Box' (Start positions changed in game, so these don't matter)
        self.move_speed = 4
        self.mouthOpen = True
        self.mouthOpenDelay = 0
        self.num_lives = 3

    def draw(self, window):
        if self.mouthOpenDelay == 7:
            self.mouthOpenDelay = 0
            self.mouthOpen = not self.mouthOpen
        self.mouthOpenDelay += 1
        key_input = pygame.key.get_pressed()
        if self.mouthOpen:
            if key_input[pygame.K_RIGHT]:
                self.PACMAN_IMG = pygame.image.load(self.pacman_png_openMouth).convert_alpha()
                self.PACMAN = pygame.transform.scale(self.PACMAN_IMG, (30, 30))
            elif key_input[pygame.K_LEFT]:
                self.PACMAN_IMG = pygame.image.load(self.pacman_png_openMouth).convert_alpha()
                self.PACMAN = pygame.transform.scale(self.PACMAN_IMG, (30, 30))
                self.PACMAN = pygame.transform.flip(self.PACMAN, True, False)
            elif key_input[pygame.K_UP]:
                self.PACMAN_IMG = pygame.image.load(self.pacman_png_openMouth).convert_alpha()
                self.PACMAN = pygame.transform.scale(self.PACMAN_IMG, (30, 30))
                self.PACMAN = pygame.transform.rotate(self.PACMAN, 90)
            elif key_input[pygame.K_DOWN]:
                self.PACMAN_IMG = pygame.image.load(self.pacman_png_openMouth).convert_alpha()
                self.PACMAN = pygame.transform.scale(self.PACMAN_IMG, (30, 30))
                self.PACMAN = pygame.transform.rotate(self.PACMAN, -90)
        else:
            if key_input[pygame.K_RIGHT]:
                self.PACMAN_IMG = pygame.image.load(self.pacman_png_CloseMouth).convert_alpha()
                self.PACMAN = pygame.transform.scale(self.PACMAN_IMG, (30, 30))
            elif key_input[pygame.K_LEFT]:
                self.PACMAN_IMG = pygame.image.load(self.pacman_png_CloseMouth).convert_alpha()
                self.PACMAN = pygame.transform.scale(self.PACMAN_IMG, (30, 30))
                self.PACMAN = pygame.transform.flip(self.PACMAN, True, False)
            elif key_input[pygame.K_UP]:
                self.PACMAN_IMG = pygame.image.load(self.pacman_png_CloseMouth).convert_alpha()
                self.PACMAN = pygame.transform.scale(self.PACMAN_IMG, (30, 30))
                self.PACMAN = pygame.transform.rotate(self.PACMAN, 90)
            elif key_input[pygame.K_DOWN]:
                self.PACMAN_IMG = pygame.image.load(self.pacman_png_CloseMouth).convert_alpha()
                self.PACMAN = pygame.transform.scale(self.PACMAN_IMG, (30, 30))
                self.PACMAN = pygame.transform.rotate(self.PACMAN, -90)

        window.blit(self.PACMAN, (self.PACMAN_BB.x + 5, self.PACMAN_BB.y + 5))

    def move(self):
        key_input = pygame.key.get_pressed()
        # Just moves character in direction of arrow key
        if key_input[pygame.K_RIGHT]:
            self.PACMAN_BB.x += self.move_speed
        if key_input[pygame.K_LEFT]:
            self.PACMAN_BB.x -= self.move_speed
        if key_input[pygame.K_UP]:
            self.PACMAN_BB.y -= self.move_speed
        if key_input[pygame.K_DOWN]:
            self.PACMAN_BB.y += self.move_speed

    def lose_life(self):
        self.num_lives -= 1

    def die(self):
        if self.num_lives == 0:
            return True
        else:
            return False

    # Add an item to a list (like adding points)
    def collect_points(self, collector, item_collected, item_type):
        if collector.colliderect(item_collected) and item_type == 'tic_tac':
            self.points += 10
            # print("Number Points: {}".format(self.points))
            return True
        if collector.colliderect(item_collected) and item_type == 'power_pellet':
            self.points += 50
            # print("Number Points: {}".format(self.points))
            return True
        if collector.colliderect(item_collected) and item_type == 'ghost':
            self.points += 500
            # print("Number Points: {}".format(self.points))
            return True
        if collector.colliderect(item_collected) and item_type == 'fruit':
            self.points += 1000
            # print("Number Points: {}".format(self.points))
            return True
        else:
            return False

    def get_points(self):
        return self.points

    def chase_ghosts(self):
        return 0

    def tunnel_transport(self):
        # TODO: These values are only for 800x600 window
        if self.PACMAN_BB.x > 800:
            self.PACMAN_BB.x = -40
        elif self.PACMAN_BB.x < -40:
            self.PACMAN_BB.x = 800


