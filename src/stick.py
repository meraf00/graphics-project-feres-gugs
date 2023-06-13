import pygame

from game import game_world
from gameobject import *
from weapons import *

import numpy as np


class StickState:
    # states
    ATTACK = 0

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


class Stick(Weapon):
    def __init__(self, id, top_screen, bottom_screen, player):
        super().__init__(id, player)

        self.player = player

        self.top_screen = top_screen

        self.bottom_screen = bottom_screen

        self.states = StickState()

        self.damage_per_second = 200.0

        self.load()

        self.states.current_state.animator.play()

    def draw(self, time_passed):
        if not self.states.current_state.animator.is_playing:
            game_world.dispose(self)

        frame = self.states.current_state.get_frame()

        self.position = self.player.position + (-30, 50)

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
        path = "assets/stick/stick-attack.png"
        image = pygame.image.load(path).convert_alpha()
        w = image.get_width() * 0.8
        h = image.get_height() * 0.8
        image = pygame.transform.scale(image, (w, h))

        state_id = StickState.ATTACK

        n_frames = 17
        width = self.width = image.get_width() // n_frames
        height = self.height = image.get_height()

        frames = []

        for i in range(n_frames):
            frame = image.subsurface(i * width, 0, width, height)
            frame = frame.subsurface(0, 0, width, height)

            frames.append(frame)

        animator = Animator(frames, 20, False)
        animator.speed = 2

        state_id = StickState.ATTACK
        state = State(state_id, frames, animator)

        self.states.add(state)

        self.states.current_state = state
