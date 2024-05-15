"""Anledningen till en settingsmodul som innehåller alla settings, snarare än att ha settings
i huvudfilen är att det blir mindre clutter och enklare att jobba med en individuell setting än en hel setting-bank."""


class Settings:
    """A class to store all settings for Alien Invasion"""
    def __init__(self):
        """Initalize the game's static settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230) # motsvarar ljusgrått. 255, 0, 0 är rött. 0, 255, 0 är grönt och 0, 0, 255 är blått.

        # Ship settings
        self.ship_limit = 3 # antal möjliga skeppförluster innan game over

        # Bullet settings
        self.bullet_width = 6
        self.bullet_height = 12
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        # Alien settings
        self.fleet_drop_speed = 12 # Hastigheten samtliga aliens rör sig (I Y-LED) i justeras ENKELT här.

        # How quickly the game speeds up
        self.speedup_scale = 1.15 # (15%, 2 är dubbla, dvs 100%)
        
        # How quickly the alien points values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        # Dessa värden är alla startvärden men som KOMMER att förändras i samband med framgångar i spelet.
        self.ship_speed = 2.2 # Skeppets hastighet justeras ENKELT här och regleras i resterande block automatiskt.
        self.bullet_speed = 4 # Hastigheten kulan färdas i
        self.alien_speed = 2.5 # Hastigheten samtliga aliens rör sig (I X-LED) i justeras ENKELT här.
        
        # fleet_direction of 1 represents RIGHT; -1 represents LEFT
        # man skulle kunna använda right/left med if/else, men siffror är enklare för att...
        # för att flyttas till vänster = subtrahera från x-värde.
        # för att flyttas till höger = addera till x-värde.
        self.fleet_direction = 1

        # Scoring settings
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien points values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale) # skulle kunna vara self.alien_points *= self.score_scale, men med int() säkrar man att resultatet
                                                                      # visas i hela nummer utan decimaler. Men nu rundar det bl.a. till 75, 112 osv. Arkadspel räknar oftast 10-tal, så vi kör på det...

