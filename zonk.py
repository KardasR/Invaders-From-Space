import pygame

from pygame.sprite import Sprite

class Zonk(Sprite):
    """A class to represent a single zonk in the fleet"""

    def __init__(self, ai_settings, screen):
        """Initialize the Zonk and set its starting position"""
        super(Zonk, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the zonk image and set its rectangle attribute.
        self.image = pygame.image.load('Python/Projects/alien_invasion/images/zonk_invader.bmp')
        self.rect = self.image.get_rect()

        # Start each new zonk near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the zonk's exact position.
        self.x = float(self.rect.x)        

    def blitme(self):
        """Draw the zonk at its current location."""
        self.screen.blit(self.image, self.rect)

    def check_edge(self):
        """Return True if a zonk is at the edge of the screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move zonk to the left or right."""
        self.x += (self.ai_settings.zonk_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x