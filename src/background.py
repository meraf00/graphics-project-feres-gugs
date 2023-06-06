import os

import pygame
from pygame.locals import *

import numpy as np

from consts import *


class Background:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player

        self.backgrounds = []

        self.positions = []

        self.parallex_factor = 0.2

        self.width = screen.get_width()
        self.height = screen.get_height()

        self.clock = pygame.time.Clock()

        self.load()

    def load(self):
        for img in os.listdir("assets/background")[::-1]:
            image = pygame.image.load("assets/background/" + img).convert_alpha()
            image = pygame.transform.scale(image, (self.width, self.height))

            self.backgrounds.append(image)
            self.positions.append(np.zeros(2))

    def draw(self):
        time_passed = self.clock.tick(FPS) / 1000.0

        for idx, bg in enumerate(self.backgrounds):
            speed = self.player.speed * self.parallex_factor * idx

            self.positions[idx] += speed * time_passed * np.array(RIGHT)

            self.screen.blit(bg, self.positions[idx])

            self.screen.blit(bg, self.positions[idx] + (self.width, 0.0))

            self.screen.blit(bg, self.positions[idx] - (self.width, 0.0))

            if (
                self.positions[idx][0] + self.width <= 0
                or self.positions[idx][0] > self.width
            ):
                self.positions[idx] = NEUTRAL
