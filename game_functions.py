import sys
from time import sleep

import pygame

from lazer import Lazer
from zonk import Zonk

def check_keydown_events(event, ai_settings, screen, ship, lazers):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right.
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Move the ship to the left.
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_lazer(ai_settings, screen, ship, lazers)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_lazer(ai_settings, screen, ship, lazers):
    # Create a new lazer and add it to the 'lazers' group.
    if len(lazers) < ai_settings.lazers_allowed:
        new_lazer = Lazer(ai_settings, screen, ship)
        lazers.add(new_lazer)

def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        # Stop moving the ship to the right.
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        # Stop moving the ship to the left.
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, zonks, lazers):
    """Respond to keyboard and mouse inputs."""
    # Check for keyboard and mouse input.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, lazers)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, zonks, lazers, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, zonks, lazers, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        # Empty the list of zonks and lazers.
        zonks.empty()
        lazers.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, zonks)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, zonk, lazers, play_button):
    """Update images on the screen each pass through the loop."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)

    # Redraw all lazers behind ship and aliens.
    for lazer in lazers.sprites():
        lazer.draw_lazer()
    ship.blitme()
    zonk.draw(screen)
    #zonk.blitme()      # Commented to get rid of error, line above accomplishes the same task

    # Draw the scoreboard
    sb.show_score()

    # Draw the play button if the game is inactive.
    if stats.game_active == False:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()    

def update_lazers(ai_settings, screen, stats, sb, ship, zonks, lazers):
    """Update position of lazers and destroy old lazers"""
    # Update lazer positions.
    lazers.update()

    # Get rid of lazers that have disappeared.
    for lazer in lazers.copy():
        if lazer.rect.bottom <= 0:
            lazers.remove(lazer)

    check_lazer_zonk_collisions(ai_settings, screen, stats, sb, ship, zonks, lazers)

def check_lazer_zonk_collisions(ai_settings, screen, stats, sb, ship, zonks, lazers):
    """Respond to a lazer-zonk collision"""
    # Check for any lazers that have hit zonks, get rid of hit zonks.
    collisions = pygame.sprite.groupcollide(lazers, zonks, True, True)

    if collisions:
        for zonks in collisions.values():
            stats.score += ai_settings.zonk_points * len(zonks)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(zonks) == 0:
        # Get rid of the currently fired lazers, speed up game, and create a new fleet.
        lazers.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, zonks)

        # Increase level.
        stats.level += 1
        sb.prep_level()

def get_number_of_zonk_x(ai_settings, zonk_width):
    """Determine the number of zonk that can fit in a row."""
    available_space_x = ai_settings.screen_width - (2 * zonk_width)
    number_zonk_x = int(available_space_x / (2 * zonk_width))
    return number_zonk_x

def create_zonk(ai_settings, screen, zonks, zonk_number, row_number):
    """Create a zonk and place it in the row."""
    zonk = Zonk(ai_settings, screen)
    zonk_width = zonk.rect.width
    zonk.x = zonk_width + 2 * zonk_width * zonk_number
    zonk.rect.x = zonk.x
    zonk.rect.y = zonk.rect.height + 2 * zonk.rect.height * row_number
    zonks.add(zonk)

def create_fleet(ai_settings, screen, ship, zonks):
    """Create a full fleet of zonk."""
    # Create a zonk and find the number of zonk in a row.
    zonk = Zonk(ai_settings, screen)
    number_zonk_x = get_number_of_zonk_x(ai_settings, zonk.rect.width)
    number_rows = get_number_of_rows(ai_settings, ship.rect.height, zonk.rect.height)

    # Create the first row of zonk.
    for row_number in range(number_rows):
        for zonk_number in range(number_zonk_x):
            create_zonk(ai_settings, screen, zonks, zonk_number, row_number)

def get_number_of_rows(ai_settings, ship_height, zonk_height):
    """Determine the amount of rows of zonk that fit on the screen."""
    available_space_y = (ai_settings.screen_height - (3 * zonk_height) - ship_height)
    number_rows = int(available_space_y / (2 * zonk_height))
    return number_rows

def check_fleet_edge(ai_settings, zonks):
    """Respond if any zonk have reached an edge."""
    for zonk in zonks.sprites():
        if zonk.check_edge():
            change_fleet_direction(ai_settings, zonks)
            break
def change_fleet_direction(ai_settings, zonks):
    """Drop the fleet and change the direction."""
    for zonk in zonks.sprites():
        zonk.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, zonks, lazers):
    """Respond to the ship being hit by an alien."""
    if stats.ships_left > 0:
        # Lower ships left.
        stats.ships_left -= 1

        # Update scoreboard.
        sb.prep_ships()

        # Empty the list of zonks and lazers.
        zonks.empty()
        lazers.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, zonks)
        ship.center_ship()

        # Pause.
        sleep(0.5)
    else:
        stats.game_active = False

def check_zonk_bottom(ai_settings, screen, stats, sb, ship, zonks, lazers):
    """Check if any zonk have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for zonk in zonks.sprites():
        if zonk.rect.bottom >= screen_rect.bottom:
            # Treat it like the ship has been hit
            ship_hit(ai_settings, screen, stats, sb, ship, zonks, lazers)
            break

def update_zonk(ai_settings, screen, stats, sb, ship, zonks, lazers):
    """Check if fleet is at an edge, then update positions of all zonk."""
    check_fleet_edge(ai_settings, zonks)
    zonks.update()

    # Look for zonk-ship collisions.
    if pygame.sprite.spritecollideany(ship, zonks):
        ship_hit(ai_settings, screen, stats, sb, ship, zonks, lazers)

    # Look for zonk hitting the bottom of the screen.
    check_zonk_bottom(ai_settings, screen, stats, sb, ship, zonks, lazers)

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()