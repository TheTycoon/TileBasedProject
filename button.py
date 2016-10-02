import pygame
import settings


class Button:
    def __init__(self, x, y, width, height, text=None):
        '''
        Consider making inherited classes: 1 for rects, 1 for using images, others for other generic shapes?
        Stuff if using images below
        self.image = image
        self.normal_image = image
        self.active_image = hover_image
        '''

        self.image = pygame.Surface((width, height))
        self.image.fill(settings.BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.text = text

    def draw_button(self, screen, mouse):
        if self.is_hovering(mouse):
            self.image.fill(settings.WHITE)
        else:
            self.image.fill(settings.SILVER)
        screen.blit(self.image, self.rect)

    def is_hovering(self, mouse):
        mouse_pos = mouse.get_pos()
        if self.rect.x < mouse_pos[0] < self.rect.x + self.rect.width and \
           self.rect.y < mouse_pos[1] < self.rect.y + self.rect.height:
                return True
        else:
            return False

    def is_clicked(self, mouse):
        mouse_click = mouse.get_pressed()
        if mouse_click[0] and self.is_hovering(mouse):
            return True
        else:
            return False
