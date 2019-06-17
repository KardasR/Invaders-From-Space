class Settings():
    """A Class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (135, 206, 250)

        # Ship settings
        self.ship_limit = 3

        # Lazer settings
        self.lazer_width = 3
        self.lazer_height = 15
        self.lazer_color = 250, 0, 0
        self.lazers_allowed = 5

        # Zonk settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.2

        # How quickly the zonk point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change during the game."""
        self.ship_speed_factor = 1.5
        self.lazer_speed_factor = 1
        self.zonk_speed_factor = 1

        # 1 = right, -1 = left
        self.fleet_direction = 1

        # Scoring
        self.zonk_points = 50

    def increase_speed(self):
        """Increase speed settings and zonk point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.lazer_speed_factor *= self.speedup_scale
        self.zonk_speed_factor *= self.speedup_scale
        self.zonk_points = int(self.zonk_points * self.score_scale)