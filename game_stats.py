import json

class GameStats:
    """Tracks statistics for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        # High score should never be reset
        self._load_high_score()


    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1


    def check_high_score(self):
        """Check to see if there's a new high score"""
        if self.score > self.high_score:
            self.high_score = self.score
            self._save_high_score(self.high_score)

    
    def _save_high_score(self, high_score):
        try:
            with open('high_score.json', 'w') as file:
                json.dump(high_score, file)
                print("High score saved successfully:", high_score)
        except Exception as e:
            print("An error occurred while saving the high score:", e)


    def _load_high_score(self):
        try:    
            with open('high_score.json', 'r') as file:
                self.high_score = json.load(file)
                print("High score loaded successfully:", self.high_score)
        except FileNotFoundError:
            self.high_score = 0
            print("High score file not found. Setting high score to 0.")
        except Exception as e:
            print("An error occurred while loading the high score:", e)
            self.high_score = 0
