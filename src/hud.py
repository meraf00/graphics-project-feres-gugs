import pygame
from consts import *

from player import Player


def draw_flags(player, flag_image, font):
    surface = player.player_screen

    width = surface.get_width()

    height = surface.get_height()

    hud_width = flag_image.get_rect().width * 2

    hud_height = height / 8

    hud_surface = pygame.Surface((hud_width, hud_height), pygame.SRCALPHA)

    hud_rect = hud_surface.get_rect()

    hud_surface.fill(BLUE_BLACK_ALPHA)

    # ========================================================
    #                           Flag
    # ========================================================
    # spear

    flag_image_hud = pygame.transform.scale(flag_image, (hud_height, hud_height))

    hud_surface.blit(
        flag_image_hud,
        (
            hud_rect.centerx - flag_image_hud.get_rect().centerx,
            hud_rect.centery - flag_image_hud.get_rect().centery,
        ),
    )

    text = font.render(str(player.flags), True, WHITE)

    hud_surface.blit(
        text,
        (
            hud_rect.centerx - text.get_rect().centerx,
            hud_rect.centery - text.get_rect().centery,
        ),
    )

    w = width - hud_width * 2

    surface.blit(hud_surface, (w, 0, hud_width, hud_height))


def draw_hud(player: Player, speed_image, shield_image, spear_image, flag_image, font):
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
    #                           Spear
    # ========================================================
    # spear

    spear_image_hud = pygame.transform.scale(spear_image, (hud_height, hud_height))

    hud_surface.blit(
        spear_image_hud,
        (
            hud_rect.centerx - spear_image_hud.get_rect().centerx,
            hud_rect.centery - spear_image_hud.get_rect().centery,
        ),
    )

    if player.spear:
        text = font.render(str(player.spear.count), True, WHITE)

    else:
        text = font.render(str(0), True, WHITE)

    hud_surface.blit(
        text,
        (
            hud_rect.centerx - text.get_rect().centerx,
            hud_rect.centery - text.get_rect().centery,
        ),
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

    draw_flags(player, flag_image, font)
