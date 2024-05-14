import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_game): # self och instance av spelet såklart, "ai_game"
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings


        # Load the alien image and set its rect attribute
        self.image = pygame.image.load("alien.bmp")
        self.rect = self.image.get_rect() # rectangle assignas på imagefilen som i sin tujr assignas på rect. Nu är "self.rect"
                                          # variabelnamnet på en alien med en bild + rect (hitbox).
        
        # GRUNDVALUE FÖR "self.rect.x" eller "self.rect.y" är ALLTID 0!!!!

        # Start each new alien near the top left screen (positioner)
        self.rect.x = self.rect.width # Lägger till utrymme till vänster om aliens bredd, likvärdigt dess bredd (på recten)
        self.rect.y = self.rect.height # Lägger till utrymme över om aliens höjd, likvärdigt dess höjd (på recten)

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x) # assignar positionen i x.led till self.x, nu en float.


    def check_edges(self):
        """Return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect() # ge screen en rect för att den ska jämföras mot alien (self.rect)
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= screen_rect.left) # OBS, FÖRFATTAREN HAR SKRIVIT self.rect.left <= 0 till skillnad från mig.

    def update(self):
        """Move the alien right or left"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction # dessa settings finns i filen settings.py
        self.rect.x = self.x
