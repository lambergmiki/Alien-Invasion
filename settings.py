class Settings:
    """A class to store all settings for Alien Invasion"""
    def __init__(self):
        """Initalize the game's settings"""
        self.initialize_static_settings()
        self.initialize_dynamic_settings()


    def initialize_static_settings(self):
        """Initialize settings that do not change throughout the game"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_limit = 3
        self.bullet_width = 6
        self.bullet_height = 12
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5
        self.fleet_drop_speed = 12
        self.fleet_direction = 1
        self.speedup_scale = 1.15
        self.score_scale = 1.5


    def initialize_dynamic_settings(self, difficulty = 'normal'):
        """Initialize settings that change throughout the game"""
        self.difficulty = difficulty
        self.set_difficulty(difficulty)
        self.alien_points = 50


    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        if difficulty == 'ez':
            self.ship_speed = 2.8
            self.bullet_speed = 5
            self.alien_speed = 2.4
        elif difficulty == 'normal':
            self.ship_speed = 2.2
            self.bullet_speed = 4
            self.alien_speed = 2.5
        elif difficulty == 'hard':
            self.ship_speed = 1.4
            self.bullet_speed = 3
            self.alien_speed = 3.2
        elif difficulty == 'The Joseph Rashid Maalouf-special':
            self.ship_speed = 10
            self.bullet_speed = 6
            self.alien_speed = 3
            self.bullets_allowed = 100


    def increase_speed(self):
        """Increase speed settings and alien points values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
