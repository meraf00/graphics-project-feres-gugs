import random

import numpy as np

from world import game_world
from gameobject import GameObject
from collectables import *


class Spawner:
    def __init__(
        self,
        top_screen,
        bottom_screen,
    ):
        self.top_screen = top_screen
        self.bottom_screen = bottom_screen

    def spawn_shield(self, position):
        game_world.instantiate(
            ShieldCollectable, self.top_screen, self.bottom_screen, position
        )

    def spawn_spear(self, position):
        game_world.instantiate(
            SpearCollectable, self.top_screen, self.bottom_screen, position
        )

    def spawn_items(self):
        shield_positions = []
        spear_positions = []

        gap = 500

        last_pos = 0

        for _ in range(20):
            last_pos = random.randint(last_pos + gap, last_pos + 2 * gap)

            if random.uniform(0, 1) > 0.5:
                spear_positions.append(last_pos)

            else:
                shield_positions.append(last_pos)

        spear_y = 100.0
        shield_y = 150.0

        for x in shield_positions:
            self.spawn_shield((x, shield_y))

        for x in spear_positions:
            self.spawn_spear((x, spear_y))

        flag_positions = [(8000, 120), (16_000, 120), (24_000, 120)]
        # flag_positions = [(500, 120), (1000, 120), (2000, 120)]

        for position in flag_positions:
            game_world.instantiate(
                FlagCollectable, self.top_screen, self.bottom_screen, position
            )
