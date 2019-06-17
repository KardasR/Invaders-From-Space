import pygame
from pygame.sprite import Sprite

class Lazer(Sprite):
    """Manages lazers fired from the ship."""
    def __init__(self, ai_settings, screen, ship):
        """Create a lazer object at the ship's current position."""
        super().__init__()
        self.screen = screen

        # Create a lazer rectangle at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, ai_settings.lazer_width, ai_settings.lazer_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store the lazer's position as a decimal.
        self.y = float(self.rect.y)

        self.color = ai_settings.lazer_color
        self.speed_factor = ai_settings.lazer_speed_factor

    def update(self):
        """Move the lazer up the screen."""
        # Update the decimal position of the lazer.
        self.y -= self.speed_factor
        # Update the rectangle position.
        self.rect.y = self.y

    def draw_lazer(self):
        """Draw the lazer to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)