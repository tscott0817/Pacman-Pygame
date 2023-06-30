import pygame
from pygame import gfxdraw

class Button():
    def __init__(self, window, x_pos, y_pos, width, height, image, scale, rec_type, text):
        self.window = window
        self.rec_type = rec_type
        pygame.font.init()

        if self.rec_type == "solid":
            self.button_color = (255, 255, 255, 0)
            self.button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            self.button_rect = self.button_surface.get_rect()
            self.button_rect.center = (x_pos, y_pos)

            # self.font_size = int((width + height) / 12)  # TODO: May want to not consider width (so width can't be same as text if I dont use outline)
            self.font_size = int((width + height) / 12)  # TODO: May want to not consider width (so width can't be same as text if I dont use outline)

            # self.font_color = (255, 255, 255)  # White font color
            self.font_color = (255, 235, 59)
            # self.font = pygame.font.Font('freesansbold.ttf', self.font_size)
            self.font = pygame.font.Font('assets/fonts/Grand9k Pixel.ttf', self.font_size)
            self.text = text
            self.text_surface = self.font.render(self.text, True, self.font_color)
            self.text_rect = self.text_surface.get_rect(center=self.button_rect.center)

        elif self.rec_type == "textured":
            self.width = image.get_width()
            self.height = image.get_height()
            self.image = pygame.transform.scale(image, (self.width * scale, self.height * scale))
            self.rect = self.image.get_rect()
            self.rect.center = (x_pos, y_pos)

        self.clicked = False

    def draw(self):
        # self.hover()
        if self.rec_type == "textured":
            self.window.blit(self.image, (self.rect.x, self.rect.y))
        if self.rec_type == "solid":
            # Shape
            # draw a rectangle using button_surface
            # pygame.draw.rect(self.window, self.button_color, self.button_rect, border_radius=25)  # TODO: Want to use window as member variable, not param
            # pygame.draw.rect(self.window, self.button_color, self.button_rect, 1, 25)
            self.window.blit(self.button_surface, (self.button_rect.x, self.button_rect.y))

            # Text
            self.window.blit(self.text_surface, self.text_rect)

    # def hover(self):
    #     if self.rec_type == "solid" or self.rec_type == "textured":
    #         mouse_pos = pygame.mouse.get_pos()
    #         if mouse_pos[0] > self.button_rect.x and mouse_pos[0] < self.button_rect.x + self.button_rect.width and mouse_pos[1] > self.button_rect.y and mouse_pos[1] < self.button_rect.y + self.button_rect.height:
    #             return True
    #         else:
    #             return False

    def hover_text(self):
        # TODO: Only considering non-textured buttons for this
        if self.rec_type == "solid":
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] > self.text_rect.x and mouse_pos[0] < self.text_rect.x + self.text_rect.width and mouse_pos[1] > self.text_rect.y and mouse_pos[1] < self.text_rect.y + self.text_rect.height:
                return True
            else:
                return False

    def is_clicked(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rec_type == "textured":
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    action = True

        # check if mouse is colliding and mouse being clicked
        elif self.rec_type == "solid":
            if self.button_rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action

    def is_clicked_text(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rec_type == "textured":
            if self.text_rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    action = True

        # check if mouse is colliding and mouse being clicked
        elif self.rec_type == "solid":
            if self.text_rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action


