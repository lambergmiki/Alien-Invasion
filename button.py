import pygame.font

class Button:
    """A class to build buttons for the game since pygame does not provide buttons"""

    def __init__(self, ai_game, msg, position = 'center', offset = 50):
        """Initialize button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = (315, 75)
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        if position == 'left':
            self.rect.midleft = (self.screen_rect.midleft[0] + offset,
                                 self.screen_rect.midleft[1])
        elif position == 'center':
            self.rect.center = self.screen_rect.center
        elif position == 'right':
            self.rect.midright = (self.screen_rect.midright[0] - offset,
                                  self.screen_rect.midleft[1])

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True,
                                         self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)