import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""
    

    def __init__(self, ai_game): # init för Ship har två parametrar: self, och instancen av spelet, dvs ai.game här (se huvudfilens AlienInvasion-Class)
                                 # instancen ai.game (via AlienInvasion Class) ger oss access till alla game resources i huvudfilen.
        """Initialize the ship and set its starting position"""
        super().__init__() # metod för att importa funktioner från parent, (Sprite)
        self.screen = ai_game.screen # assignar spelets screen en attribute från Ship (dvs )
        self.screen_rect = ai_game.screen.get_rect() # accessar skärmens rect attribute med get_rect() och assignar det till self.screen_rect.
                                                     # Det tillåter oss att lägga skeppet på rätt plats på skärmen.
        self.settings = ai_game.settings

        # Load the ship image and get its rect - rect betyder rectangle. Pygame behandlar objekt som rectangles,
        # även om dess form inte är rektangulär - det gör det enkelt och snabbt att avgöra om två objekt har kolliderat, t.ex.
        # rect är alltså 'hitboxen' för ett objekt, ofta kallat i spel.
        self.image = pygame.image.load('ship.bmp') # pygame.image.load()-metoden laddar en bild, som assignas på self.image inom classen Ship.
        self.rect = self.image.get_rect() # get_rect() accessar rect attributen hos (bilden av) skeppet så att vi kan använda den datan för att placera skeppet.

        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom # self.rect = skeppet. Tilldelas här positionen midbottom på screen_rect (skärmens rect-yta)
        
        # Store a float for the ship's exact horizontal position.
        self.x = float(self.rect.x) # konverterar valuet av self.rect.x till en float som jag assignar till self.x (skeppets position i x-led)

        # Movement flag; start with a ship that's not moving.
        self.moving_right = False
        self.moving_left = False


    def center_ship(self):
        """Center ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x) # resettar skeppets x-value som tillåter oss att tracka rörelsen


    def update(self):
        """Update the ship's (self.rect) position (x) based on the movement flag."""
        # Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right: # om moving_right är True (dvs skeppet färdas till höger) och
                                                                           # skeppets (self.rect) värde av högerkanten (.right) är mindre än värdet av skärmens högerkant:
            self.x += self.settings.ship_speed # addera till x-led värdet av ship_speed (som finnas i settings)

        if self.moving_left and self.rect.left > 0: # om moving_left är True (dvs skeppet färdas till vänster) och
                                                    # skeppets (self.rect) värde av vänsterkanten är mindre än värdet av skärmens vänsterkant:
            self.x -= self.settings.ship_speed # subtrahera från x-led värdet av ship_speed (som finnas i settings)
        
        # ovan används 2 if's ISTÄLLET för ett if + elif, för att skeppets värde i x-led ska kunna höjas och sänkas om både...
        # vänster och höger piltangent är nedtryckta. Då står skeppet still. Om jag använt elif för vänster hade höger piltangent
        # alltid haft prioritet.
        
        # Update rect object from self.x.
        self.rect.x = self.x

        # All uppdatering i kodblocket update ovan sker baserat på skeppets hastighet från ship_speed-variabeln i settings.

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)