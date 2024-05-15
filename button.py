import pygame.font # module that lets us render text to the screen

class Button:
    """A class to build buttons for the game since pygame does not provide buttons"""

    def __init__(self, ai_game, msg, position = 'center'): # self, ai_game instance/object and msg (text on button)
        """Initialize button attributes"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0) # dark green
        self.text_color = (255, 255, 255) # white
        self.font = pygame.font.SysFont(None, 48) # None-argumentet säger åt Python att använda default font, 48 är size på font


        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        # Set the button position
        if position == 'left':
            self.rect.midleft = self.screen_rect.midleft
        elif position == 'center':
            self.rect.center = self.screen_rect.center
        elif position == 'right':
            self.rect.right = self.screen_rect.midright

        # The button message needs to be prepped only once
        self._prep_msg(msg) # msg är argumentet 'Play' i huvudfilen, rad 48.

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True,
                                         self.text_color, self.button_color) # render()-metoden från font turns text stored in msg into an image
                                                                                         # True/False-arget i metoden är boolean value för on/off på antialiasing, 
                                                                                         # dvs smooth edges
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect) # screen.fill() ritar den rektangulära biten av knappen
        self.screen.blit(self.msg_image, self.msg_image_rect) # screen.blit() ritar "textbilden" (msg_image genererad av font.render()) tack vare
                                                              # att jag matar den med 2 args: textbilden msg_image och rect-objektet msg_image_rect