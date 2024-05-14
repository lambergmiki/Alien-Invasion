import pygame
from pygame.sprite import Sprite


class Bullet(Sprite): # Bullet är CHILD (inherits from Sprite) till PARENT Sprite (Sprite importerat via pygame.sprite-modulen)
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game): # skapar en instance av Bullet, kräver då en instance av AlienInvasion som här är ai_game.
        """Create a bullet object at the ship's current position"""
        super().__init__() # super() makes sure methods from parent class (Sprite) are inherited properly.
                         # Det är alltså nödvändigt att ha super() i childens __init__ för att calla methods från Parent Class.
        
        self.screen = ai_game.screen # skapar attribute för screen
        self.settings = ai_game.settings # skapar attribute för settings
        self.color = self.settings.bullet_color # skapar attribute för bullets color


        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, 
                                      self.settings.bullet_height) # OBS: bullet settings ligger i settings-filen.
        self.rect.midtop = ai_game.ship.rect.midtop # assignar bulletens midtop rect till skeppets midtop rect. Innebär att 
                                                    # bulleten skjuts från skeppets midtop-rect. Som sig bör.

        # Store the bullet's position as a float

        self.y = float(self.rect.y) # Bulletens y-värde (self.rect.y) assignas som FLOAT på
                                    # self.y för att enkelt justera hastighet på bullet vid behov.
        
    def update(self): # 
        """Move the bullet up the screen"""
        # Update the exact position of the bullet.
        self.y -= self.settings.bullet_speed # för att förändra bulletens position decreasar vi y-koordinaten (så den färdas uppåt) med aktuell bullet_speed
        # Update the rect position.
        self.rect.y = self.y # den nya y-koordinaten assignas sedan till recten på bulleten som i sin tur då beräknar kollisioner med andra element
    

    def draw_bullet(self): # denna method 'ritar' bulleten på skärmen eftersom den inte är en bildfil (.bmp som skeppet).
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect) # fyller skärmen (screen) med bulletens färg (color) och sist recten för bulleten ('hitboxen')