import pygame
from consts import *

from player import Player


def draw_hud(player: Player, speed_image, shield_image):
    surface = player.player_screen

    width = surface.get_width()

    height = surface.get_height()

    hud_width = width / 4

    hud_height = height / 8

    hud_surface = pygame.Surface((hud_width, hud_height), pygame.SRCALPHA)

    hud_rect = hud_surface.get_rect()

    hud_surface.fill(BLUE_BLACK_ALPHA)

    # ========================================================
    #                           Speed
    # ========================================================

    speed_image_hud = pygame.transform.scale(speed_image, (hud_height, hud_height))
    hud_surface.blit(speed_image_hud, speed_image_hud.get_rect())

    speed_percentage = player.speed / player.max_speed

    pygame.draw.line(
        hud_surface,
        GRAY,
        (speed_image_hud.get_rect().width, speed_image_hud.get_rect().height / 2),
        (
            (speed_image_hud.get_rect().width + hud_width / 4),
            speed_image_hud.get_rect().height / 2,
        ),
        10,
    )

    # speed line
    if player.speed > 0:
        pygame.draw.line(
            hud_surface,
            GREEN,
            (speed_image_hud.get_rect().width, speed_image_hud.get_rect().height / 2),
            (
                (speed_image_hud.get_rect().width + hud_width * speed_percentage / 4),
                speed_image_hud.get_rect().height / 2,
            ),
            10,
        )

    # ========================================================
    #                           Shield
    # ========================================================

    if player.shield:
        sheild_image_hud = pygame.transform.scale(
            shield_image, (hud_height, hud_height)
        )

        sheild_rect = sheild_image_hud.get_rect()

        sheild_rect = hud_surface.blit(
            sheild_image_hud, (hud_width - sheild_rect.width, 0)
        )

        shield_percentage = player.shield.hitpoint / player.shield.max_hitpoint

        # shield capacity line
        pygame.draw.line(
            hud_surface,
            GRAY,
            (sheild_rect.left, sheild_rect.height / 2),
            (
                (sheild_rect.left - hud_width / 4),
                sheild_rect.height / 2,
            ),
            10,
        )
        # shield line
        if shield_percentage > 0:
            pygame.draw.line(
                hud_surface,
                GREEN,
                (sheild_rect.left, sheild_rect.height / 2),
                (
                    (sheild_rect.left - (hud_width * shield_percentage / 4)),
                    sheild_rect.height / 2,
                ),
                10,
            )

    w = width / 2 - hud_width / 2

    surface.blit(hud_surface, (w, 0, hud_width, hud_height))
