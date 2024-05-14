import pygame.font # eftersom Scoreboard skriver text på skärmen importerar vi pygame.font-modulen.
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """A class to report scoring information"""
    
    def __init__(self, ai_game): # vi ger __init__:en ai_game parametern så att den har access till
                                 # settings, screen och stats som är nödvändiga för tracking av score
        """Initialize scorekeeping attributes"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats # se kodrad 24

        # Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48) # återigen, None är default font, 48 är storlek

        # Callar metoden som preppar alla scores (text-till-bild)
        self.prep_images()


    def prep_images(self):
        """Prepare the initial score image - genererar texten i form av en bild"""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_ships(self):
        """Show how many ships are left"""
        self.ships = Group() # skapar en tom grupp (ships)
        for ship_number in range(self.stats.ships_left): # för varje skepp i range (hämtar från ships_left som är 3 vid uppstart)
            ship = Ship(self.ai_game) # skapar ett skepp
            ship.rect.x = 10 + ship_number * ship.rect.width # assignar skeppets rect: 10 på x-led + skeppets nr (0, 1, 2 - totalt 3 skepp) * bredden på skeppet
                                                             # 10 + 0 + bredd = 10 + 0 (bredd x 0 = 0), skepp nr 2: 10 + 1 * bredd = 10 + bredd
            ship.rect.y = 10 # assignar skeppets rect: 10 på y-led
            self.ships.add(ship) # lägger till ett skepp i gruppen ships. Vid uppstart sker alltså: 3 skepp läggs till då värdet i ships_left är 3.


    def prep_score(self): # funktionen för att förvandla text till bild
        """Turn the score into a rendered image"""
        # self.stats.score tar nummervärdet från stats.score (som kommer från huvudfilen, som i sin tur hämtar från GameStats)
        rounded_score = round(self.stats.score, -1) # säger åt Python att avrunda aktuell score (self.stats.score), med ett andra arg (-1) att avrunda till närmaste 10-tal.
                                                    # det är upphöjt till som gäller som formula, dvs score -2 är score upphöjt till -2, alltså närmaste 100-tal. -3 är 1000.
        score_str = f"{rounded_score:,}" # format-specifier (f) används för att modifiera hur variabeln presenteras - här säger man åt Python att presentera score med , där det är lämpligt. 1,000,000 t.ex.
        self.score_image = self.font.render(f"Poäng {score_str}", True, 
                                            self.text_color, self.settings.bg_color) # sedan matas det till font.render()
                                                                                     # som gör det till en bild
        
        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20 # placerar score_recten på höger sida av skärmen, - 20 pixlar
        self.score_rect.top = 20 # placerar score_recten på toppen, med en marginal på 20 neråt (top = 0, bottom = 800)

    def prep_level(self):
        """Turn the level into a rendered image"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(f"Nivå {level_str}", True,
                                                self.text_color, self.settings.bg_color)
        
        # Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right # sätter level_rect på samma x-pos som score_rect ovan
        self.level_rect.top = self.score_rect.bottom + 10 # sätter level_rect på samma y-höjd som score_rect, men +10

    def prep_high_score(self):
        """Turn the high score into a rendered image"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}" # format-specifier (f) används för att modifiera hur variabeln presenteras - här säger man åt Python att presentera score med , där det är lämpligt.
        self.high_score_image = self.font.render(f"High Score {high_score_str}", True,
                                                self.text_color, self.settings.bg_color)
        
        # Center high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Check to see if there's a new high score"""
        if self.stats.score > self.stats.high_score: # om nuvarande score är större än highscore:
            self.stats.high_score = self.stats.score # assigna nuvarande score till high_score
            self.prep_high_score() # callar prep_high_score() för att uppdatera high-score-bilden.

    def show_score(self):
        """Draw scores and level to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)