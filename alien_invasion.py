import sys
from time import sleep
import json
from pathlib import Path
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,
            self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.game_active = False

        self.ez_button = Button(self, "ez", 'left')
        self.normal_button = Button(self, "normal", 'center')
        self.hard_button = Button(self, "hard", 'right')

        self.joseph_button = None

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self.start_new_level()

            self._update_screen()
            self.clock.tick(60)


    def _exit_game(self):
        """Ensure high score is saved before exiting game"""
        self.stats._save_high_score(self.stats.high_score)
        sys.exit()


    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._exit_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_button_clicks(mouse_pos)


    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif (event.key == pygame.K_p) and (not self.game_active):
            self._start_game()
        elif (event.key == pygame.K_j):
            self._replace_normal_buttons()
            self.ship.init_if_joseph_button()
        elif event.key == pygame.K_q:
            self._exit_game()


    def _replace_normal_buttons(self):
        """Replaces normal modes with Josephs mode"""
        self.ez_button = None
        self.normal_button = None
        self.hard_button = None
        self.joseph_button = Button(self, 'The Joseph-special')


    def _check_button_clicks(self, mouse_pos):
        """Start a new game with chosen difficulty based on button click"""
        if not self.game_active:
            if self.joseph_button and self.joseph_button.rect and self.joseph_button.rect.collidepoint(mouse_pos):
                self._start_game(difficulty='The Joseph Rashid Maalouf-special')
            else:
                if self.ez_button and self.ez_button.rect and self.ez_button.rect.collidepoint(mouse_pos):
                    self._start_game(difficulty='ez')
                elif self.normal_button and self.normal_button.rect and self.normal_button.rect.collidepoint(mouse_pos):
                    self._start_game(difficulty='normal')
                elif self.hard_button and self.hard_button.rect and self.hard_button.rect.collidepoint(mouse_pos):
                    self._start_game(difficulty='hard')


    def _start_game(self, difficulty='normal'):
        """Start a new game."""
        self.settings.set_difficulty(difficulty)
        self.settings.initialize_dynamic_settings(difficulty)

        self.stats.reset_stats()
        self.game_active = True
        self.sb.prep_images()

        self.bullets.empty()
        self.aliens.empty()

        self._create_fleet()
        self.ship.center_ship()

        pygame.mouse.set_visible(False)


    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group in the init"""
        if (len(self.bullets)) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions"""
        if self.settings.difficulty == 'The Joseph Rashid Maalouf-special':
            collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens,
                False, True)
        else:
            collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()


    def start_new_level(self):
        """Starts a new level if there are no aliens on screen"""
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            
            self.stats.level += 1
            self.sb.prep_level()

            sleep(0.3)


    def _update_aliens(self):
        """Update the position of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()


    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet
            self.ship.center_ship()

            sleep(0.5)

        else:
            self.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break


    def _create_fleet(self):
        """Create fleet of aliens"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2*alien_width

            current_x = alien_width
            current_y += 2 * alien_height


    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""    
        new_alien = Alien(self) 
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """Drop the entire fleet and change fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        self.sb.show_score()

        if not self.game_active:
            if self.joseph_button:
                self.joseph_button.draw_button()
            else:
                self.ez_button.draw_button()
                self.normal_button.draw_button()
                self.hard_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()