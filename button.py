import pygame
# button class
# class to create rectangles shapes as buttons and fill with an image
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    # hower function so that buttons will change color
    def hower(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            action = True

        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action

    def draw(self, surface):
        # draw the button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))


    def is_drawn(self):
        action = False
        # get the position of the mouse
        pos = pygame.mouse.get_pos()

        # check if mouse is colliding and mouse being clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action