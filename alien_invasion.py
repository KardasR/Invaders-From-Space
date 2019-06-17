# Let's start off with some inputs.
import sys

import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from zonk import Zonk

import game_functions as gf


def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the play button.
    play_button = Button(ai_settings, screen, "Play")

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make the Enterprise.
    ship = Ship(ai_settings, screen)

    # Make a group to store lazers in.
    lazers = Group()

    # Make a group of zonk.
    zonks = Group()

    # Create the fleet of zonk.
    gf.create_fleet(ai_settings, screen, ship, zonks)

    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, zonks, lazers)
        gf.update_screen(ai_settings, screen, stats, sb, ship, zonks, lazers, play_button)

        if stats.game_active:
            ship.update()
            gf.update_lazers(ai_settings, screen, stats, sb, ship, zonks, lazers)
            gf.update_zonk(ai_settings, screen, stats, sb, ship, zonks, lazers)

run_game()
