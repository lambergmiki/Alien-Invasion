import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""
    

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.image = pygame.image.load('ship.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False


    def init_if_joseph_button(self):
            self.image = pygame.image.load('joseph minskad.bmp')
            self.rect = self.image.get_rect()
            self.rect.midbottom = self.screen_rect.midbottom
            self.x = float(self.rect.x)
            self.moving_right = False
            self.moving_left = False


    def center_ship(self):
        """Center ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)


    def update(self):
        """Update the ship's (self.rect) position (x) based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x


    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)