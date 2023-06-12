import pygame

from game import game_world
from gameobject import *

import numpy as np


class StickState:
    # states
    IDLE = 0
    ATTACK = 1

    def __init__(self):
        self.states = {}
        self.current_state: State

    def add(self, state: State):
        self.states[state.id] = state

    def switch_to(self, state_id):
        if self.current_state.is_animated:
            self.current_state.animator.stop()

        self.current_state = self.states[state_id]

        if self.current_state.is_animated:
            self.current_state.animator.play()


class Stick(GameObject):
    def __init__(self, id, top_screen, bottom_screen, player):
        super().__init__(id)

        self.player = player

        self.top_screen = top_screen

        self.bottom_screen = bottom_screen

        self.load()

    def draw(self, time_passed):
        frame, rect = self.rotate(self.frame, 90)

        self.position = self.player.position

        # offset position according to players position
        player_one_pos = game_world.game_objects[PLAYER_1].position
        player_two_pos = game_world.game_objects[PLAYER_2].position

        # draw on top and bottom screen
        offset = (
            self.top_screen.get_width() / 2,
            self.top_screen.get_height() / 4,
        )
        render_position = self.position - player_one_pos + offset
        top_rect = self.top_screen.blit(frame, render_position)

        render_position = self.position - player_two_pos + offset
        bottom_rect = self.bottom_screen.blit(frame, render_position)

        return top_rect, bottom_rect

    def load(self):
        path = "assets/stick/stick.png"

        self.frame = pygame.image.load(path).convert_alpha()

        self.height = self.frame.get_height()
        self.width = self.frame.get_width()
