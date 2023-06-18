from gameobject import GameObject


import pygame

from gameobject import *
from world import game_world


class ShieldCollectable(GameObject):
    def __init__(self, id, top_screen, bottom_screen, initial_position):
        super().__init__(id)

        self.position = np.array(initial_position)

        self.top_screen = top_screen

        self.bottom_screen = bottom_screen

        self.load()

    def draw(self, time_passed):
        # offset position according to players position
        player_one_pos = game_world.game_objects[PLAYER_1].position
        player_two_pos = game_world.game_objects[PLAYER_2].position

        # draw on top and bottom screen
        offset = (
            self.top_screen.get_width() / 2,
            self.top_screen.get_height() / 4,
        )

        render_position = self.position - player_one_pos + offset
        top_rect = self.top_screen.blit(self.frame, render_position)

        render_position = self.position - player_two_pos + offset
        bottom_rect = self.bottom_screen.blit(self.frame, render_position)

        return top_rect, bottom_rect

    def load(self):
        path = "assets/shield/shield-collectable.png"

        self.frame = pygame.image.load(path).convert_alpha()

        self.frame = pygame.transform.scale(self.frame, (100, 100))

        self.height = self.frame.get_height()
        self.width = self.frame.get_width()


class SpearCollectable(GameObject):
    def __init__(self, id, top_screen, bottom_screen, initial_position):
        super().__init__(id)

        self.position = np.array(initial_position)

        self.top_screen = top_screen

        self.bottom_screen = bottom_screen

        self.load()

    def draw(self, time_passed):
        # offset position according to players position
        player_one_pos = game_world.game_objects[PLAYER_1].position
        player_two_pos = game_world.game_objects[PLAYER_2].position

        # draw on top and bottom screen
        offset = (
            self.top_screen.get_width() / 2,
            self.top_screen.get_height() / 4,
        )

        render_position = self.position - player_one_pos + offset
        top_rect = self.top_screen.blit(self.frame, render_position)

        render_position = self.position - player_two_pos + offset
        bottom_rect = self.bottom_screen.blit(self.frame, render_position)

        return top_rect, bottom_rect

    def load(self):
        path = "assets/spear/spears-collectable.png"

        self.frame = pygame.image.load(path).convert_alpha()

        self.height = self.frame.get_height()
        self.width = self.frame.get_width()


class FlagCollectable(GameObject):
    def __init__(self, id, top_screen, bottom_screen, initial_position):
        super().__init__(id)

        self.position = np.array(initial_position)

        self.top_screen = top_screen

        self.bottom_screen = bottom_screen

        self.load()

    def draw(self, time_passed):
        # offset position according to players position
        player_one_pos = game_world.game_objects[PLAYER_1].position
        player_two_pos = game_world.game_objects[PLAYER_2].position

        # draw on top and bottom screen
        offset = (
            self.top_screen.get_width() / 2,
            self.top_screen.get_height() / 4,
        )

        render_position = self.position - player_one_pos + offset
        top_rect = self.top_screen.blit(self.frame, render_position)

        render_position = self.position - player_two_pos + offset
        bottom_rect = self.bottom_screen.blit(self.frame, render_position)

        return top_rect, bottom_rect

    def load(self):
        path = "assets/flag/flag.png"

        self.frame = pygame.image.load(path).convert_alpha()
        self.frame = pygame.transform.scale(self.frame, (100, 100))

        self.height = self.frame.get_height()
        self.width = self.frame.get_width()
