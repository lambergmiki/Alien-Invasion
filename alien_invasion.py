import sys # innehåller verktyg för att avsluta spelet när spelaren väljer att avsluta
from time import sleep # sleep()-funktionen tillåter oss att pausa spelet
import json
from pathlib import Path

import pygame # innehåller funkionaliteter för att skapa ett spel

from settings import Settings # class för alla settings
from ship import Ship # class för skeppet
from bullet import Bullet # class för bullets
from alien import Alien # class för aliens
from game_stats import GameStats # class för statistik
from button import Button # class för knappar (i huvudsak Play-knappen)
from scoreboard import Scoreboard # classen Scoreboard håller koll på poäng, high score, level och trycker det på skärmen


class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock() # skapar instance av importerad class Clock från modulen pygame (rad 2) som har en 'time'-modul, pygame.time.
        self.settings = Settings() # skapar en instance av importerad class Settings, sen används den instancen för att calla variabler/methods från Settings.
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,
            self.settings.screen_height)) # hämtar settings för width/height från settings-modulen som sen assignas till screen.
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self) # Create an instance to store game statistics
        self.sb = Scoreboard(self) # Create an instance to create a scoreboard

        self.ship = Ship(self) # Ship är importerad, vi callar Ship() med ett argument: en instance av AlienInvasion, dvs 'self' här,
                               # eftersom self är från AlienInvasions init. Ship får då hela spelets resources. Detta ship assignas slutligen
                               # till self.ship som är en instance av Ship.
        self.bullets = pygame.sprite.Group() # Gruppen håller alla bullets
        self.aliens = pygame.sprite.Group() # Gruppen håller alla aliens

        self._create_fleet() # hjälpmethod som skapar flotta av aliens

        # Start Alien Invasion in an inactive state
        self.game_active = False # spelet kan inte spelas nu förrän detta condition blir True (via en Playknapp, t.ex.)

        # Create the play buttons:
        self.ez_button = Button(self, "ez", 'left')
        self.normal_button = Button(self, "normal", 'center')
        self.hard_button = Button(self, "hard", 'right')


    def run_game(self):
        """Start the main loop for the game"""
        while True: # infinit loop för att hålla spelet körandes
                                 # check_events ska alltid köras för att detecta eventuell quit av spelaren ('q' eller krysset)
            self._check_events() # för att calla en method inuti en class, använd dot notation med self enl denna kodrad.

            if self.game_active: # detta kodblock behöver bara köras om spelet är aktivt
                self.ship.update() # callar metoden update från instancen ship (av class Ship) (om och om igen pga while-loopen i run_game)
                                    # hjälpmetoden _check_events() callas från denna (infinita) while loop utan att clustera kodblocket run_game.
                
                self._update_bullets() # som self.ship.update(), men här callas metoden mot en grupp (se kodrad 32) och denna update
                                    # gäller då alla sprites i gruppen (1 bullet = 1 sprite)

                self._update_aliens() # callar hjälpmetoden _update_aliens() som i sin tur callar update() på aliens-gruppen där alla aliens uppdateras.
                                    # precis som i _update_bullets() ovan.

                self.start_new_level() # callar metoden som undersöker om alla aliens är döda - om ja: ny level startar

            # dessa körs också alltid för att uppdatera skärmen medan spelaren väljer om hen ska starta ett nytt spel t.ex.
            self._update_screen() # samma sak här som _check_events(). Mindre cluster, enklare att förstå.
            self.clock.tick(60) # tick()-metoden tar ett arg: antalet frame rates för spelet. Här blir det 60 FPS.


    def _exit_game(self):
        """Ensure high score is saved before exiting game"""
        self.stats._save_high_score(self.stats.high_score)
        sys.exit()


    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get(): # for-loopen loopar konstant för att 'lyssna' efter actions. En sk event loop. get() hämtar alla events som skett från en 'lista'.
            if event.type == pygame.QUIT: # trycker spelaren på exitknappen (som motsvarar pygames 'pygame.QUIT'-event) stängs programmet av via sys.exit().
                self._exit_game()
            elif event.type == pygame.KEYDOWN: # kollar om en tangent trycks ned
                self._check_keydown_events(event) # callar help-methoden nedan som innehåller logiken
            elif event.type == pygame.KEYUP: # kollar om tangent är släppt (upp)
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos() # hämtar x- och y-koordinater vid tidpunkten för musklicket - dessa lagras i mouse_pos.
                self._check_button_clicks(mouse_pos)


    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT: # eftersom "event" är en parameter i methoden är det en lokal variabel. Den behöver inte adressas som self.event.
        # Move ship to the right
            self.ship.moving_right = True # så länge detta (moving_right, se ship.py för mer info) är True flyttas skeppet till höger
        elif event.key == pygame.K_LEFT:
        # Move ship to the left
            self.ship.moving_left = True # så länge detta (moving_left, se ship.py för mer info) är True flyttas skeppet till vänster
        # Fire bullet on pressed SPACE
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif (event.key == pygame.K_p) and (not self.game_active):
            self._start_game()
        elif event.key == pygame.K_q:
            self._exit_game()


    def _check_button_clicks(self, mouse_pos):
        """Start a new game with chosen difficulty based on button click"""
        print("Checking button clicks")
        if self.ez_button.rect.collidepoint(mouse_pos) and not self.game_active: # utvärderar om x- och y-koordinaterna vid musklicket (mouse_pos)
                                                                                 # kolliderar med knappen (isf True)
                                                                                 # samt om game_active är True/False och invertera det med "not".
                                                                                 # om spelet är aktivt (True) blir det False, eftersom "not True" = False
            print("Clicked EZ button")
            self._start_game(difficulty='ez')
        elif self.normal_button.rect.collidepoint(mouse_pos) and not self.game_active:
            print("Clicked Normal button")
            self._start_game(difficulty='normal')
        elif self.hard_button.rect.collidepoint(mouse_pos) and not self.game_active:
            print("Clicked Hard button")
            self._start_game(difficulty='hard')


    def _start_game(self, difficulty='normal'):
        """Start a new game."""
        print("Starting game with difficulty:", difficulty)
        # Set the game difficulty
        self.settings.set_difficulty(difficulty)

        # Reset the game settings (i.e. speeds tillbaka till default values)
        self.settings.initialize_dynamic_settings(difficulty)

        # Reset the game statistics.
        self.stats.reset_stats()
        self.game_active = True
        self.sb.prep_images()

        # Get rid of any remaining bullets and aliens.
        self.bullets.empty()
        self.aliens.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)


    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT: # eftersom "event" är en parameter i methoden är det en lokal variabel. Den behöver inte adressas som self.event.
            # Stop moving the ship to the right
            self.ship.moving_right = False # moving_right är då False, vilket betyder att skeppet inte rör sig till höger mer.
            # Stop moving the ship to the left
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False # moving_left är då False, vilket betyder att skeppet inte rör sig till vänster mer.


    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group (kodrad 32)"""
        if (len(self.bullets)) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        # Update bullet position
        self.bullets.update() # bullets är en grupp (via sprite classen, se init i denna fil)

        # Get rid of bullets that are off screen - LÄS MER OM DENNA LOOP I ANTECKNINGAR!!!
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0: # om bulletens undersida av recten är mindre än 0 (dvs toppen på skärmen):
                self.bullets.remove(bullet) # ta bort berörd bullet

        # Efter att bullets positioner har etablerats, kollas eventuella kollisioner via hjälpmetoden _check_bullet_alien_collisions() nedan.
        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        # Remove any bullets and aliens that have collided
        # If so, get rid of the bullet and the alien
        # groupcollide() nedan identifierar överlapp mellan bullets och aliens respektive rects och
        # skapar ett key-value-par i den dictionary som den returnerar (detta sker internt, pygame-logik)
        collisions = pygame.sprite.groupcollide( #En kollision = 1 poäng t.ex.
            self.bullets, self.aliens, True, True) # De två sista True-argen säger åt Python att deleta bullet och alien

        # POÄNGRÄKNING VIA COLLISIONS
        if collisions:
            for aliens in collisions.values(): # går igenom alla aliens (values) utan att ta hänsyn till dess keys (bullets)
                self.stats.score += self.settings.alien_points * len(aliens) # len räknar antalet träffar i values(). 1 alien = 1 träff i values()
                self.sb.prep_score() # callar metoden från scoreboard för att rendera bilden av nuvarande score
                self.sb.check_high_score() # callar metoden från scoreboard för att kolla om nuvarande score är större än high score
                                           # detta görs efter varje alien-collision för att vara nogrann med att varje nedskjutning av alien checkas mot high_score


    def start_new_level(self):
        """Starts a new level if there are no aliens on screen"""
        if not self.aliens: # Kollar om det finns värden i gruppen aliens. "if no aliens, do:" eller "not False" = True
            # Destroy existing bullets and create new fleet
            self.bullets.empty() # metoden empty() tar bort alla befintliga sprites från en grupp
            self._create_fleet()
            self.settings.increase_speed()
            
            # Increase the level
            self.stats.level += 1
            self.sb.prep_level()

            # Pause to allow player to prepare for next level
            sleep(0.3)


    def _update_aliens(self):
        """Update the position of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update() # aliens är en grupp (via sprite classen, se init i denna fil)

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens): # identifierar kollisioner mellan en sprite och en annan sprite från en grupp av sprites.
                                                                   # Här loopar den igenom gruppen av sprites och kollar om ngn sprite kolliderat med spriten 'ship'.
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()


    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0: # om spelaren har ships kvar så executas hela blocket nedan...
            
            # Decrement ships_left (from settings)
            self.stats.ships_left -= 1
            self.sb.prep_ships() # callar metoden som visar antalet skepp (liv) kvar - callas efter decrement på rad 208 för att uppdatering ska ske direkt efter.

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty() # empty() tar som bekant bort alla befintliga sprites från en viss grupp, här: bullets
            self.aliens.empty() # och här: aliens

            # Create a new fleet and center the ship.
            self._create_fleet
            self.ship.center_ship() # ????

            # Pause
            sleep(0.5) # pausar all execution av programmet i en halv sek. Dvs fryser hela programmet,
                    # när programmet resumas efter pausen så fortsätter koden vid _update_screen()-metoden
                    # som ritar den nya fleeten av aliens på skärmen.

        else: # om spelaren INTE har ships kvar så tar spelet slut (game_active i spelets init blir False och slutar köras)
            self.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height: # om aliens rect bottom värde är större än height på
                                                                      # skärmen (800), calla _ship_hit().
            # Treat this the same as if the ship got hit.
                self._ship_hit()
                break # break används för att inte kontrollera resten av alla kvarvarande aliens eftersom
                      # det räcker att EN alien träffat botten. Sparar minne, processorkraft och tid.


    def _create_fleet(self):
        """Create fleet of aliens"""
        # Create an alien and keep adding aliens until there is no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self) # en "instance" (?) av classen Alien skapas
        alien_width, alien_height = alien.rect.size # (en rects 'size' attributeär tuple av rectens height och width)

        current_x, current_y = alien_width, alien_height # current_x & y representerar position i x respektive y-led på NÄSTA alien jag önskar placera på skärmen. Dom assignas width och height på en alien.
        while current_y < (self.settings.screen_height - 3 * alien_height): # matteuttrycket betyder att en alien läggs till OM det finns utrymme
            while current_x < (self.settings.screen_width - 2 * alien_width): # för 2 aliens utifrån dess bredd / 3 aliens utifrån dess height
                self._create_alien(current_x, current_y)
                current_x += 2*alien_width # det nya x-värdet för NÄSTA alien uppdateras genom att värdet av 2 alienbreddar läggs till på variabel current_x.

        # Finished a row; reset x value, and increment y value
            current_x = alien_width # resettar x-koordinaten så att nästa rads första alien kan placeras på samma x-värde som föregående rader
            current_y += 2 * alien_height # till y-koordinaten adderas 2 * höjden av en alien för att säkerställa plats under den förra raden.


    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""    
        new_alien = Alien(self) 
        new_alien.x = x_position # assignar positionen i x-led för NÄSTA alien till den nya aliens x-värde (ur ett koordinatperspektiv, dvs dess horisontella pos)
        new_alien.rect.x = x_position # assignar samma pos i x-led för NÄSTA aliens rect
        new_alien.rect.y = y_position # assignar pos i y-led för NÄSTA aliens rect
        self.aliens.add(new_alien)  # "NÄSTA" alien läggs nu till i gruppen aliens (som är en sprite.Group likt bullets)


    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges(): # if True:
                self._change_fleet_direction() # callar fleet drop och direction change, sedan breakas loopen 
                break


    def _change_fleet_direction(self):
        """Drop the entire fleet and change fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed # lägger till fleet_drop_speed från settings till y-värdet på samtliga aliens i sprite-gruppen, dvs
                                                             # aktuellt y-värde + fleet_drop_speed, säg 10. Om alien är högst upp (0) droppar den lite neråt till 10. Längst ner är ju 800.
        self.settings.fleet_direction *= -1 # påminnelse: left är negativt (-1) värde, right är positivt (1) värde. Så om aktuellt värde är 1 (right)
                                            # så blir det left (1 * -1 = -1, simpel matte).


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color) # fill()-metoden fyller föregående variabel med färg.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme() # blitme()-metoden ritar skeppet (funktionen är skriven i Ship-modulen och skeppets rect + image är assignat variabeln 'ship' här)
        self.aliens.draw(self.screen) # draw()-metoden kräver en yta att rita på: screen här. Positionen objektet ritas på beror på dess rect yta, som kan ses i alien.py.

        # Draw the score information
        self.sb.show_score() # callar show_score-funktionen från scoreboard-modulen

        # Draw the play button if the game is inactive (man vill ju inte att knappen stör midgame)
        if not self.game_active:
            self.ez_button.draw_button()
            self.normal_button.draw_button()
            self.hard_button.draw_button()

        pygame.display.flip() # flyttar "bak" den gamla bilden och ersätter den med en ny display med ny info (t.ex. i samband med ett nedskjutet skepp, ett avlossat skott osv)

if __name__ == '__main__':
    # Make a new game instance, and run the game.
    ai = AlienInvasion() # ai (instance) skapas via AlienInvasion (class)
    ai.run_game() # instancen körs via run_game()-metoden som finns i AlienInvasion-classen.