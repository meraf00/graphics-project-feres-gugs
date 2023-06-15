import random

import numpy as np

from game import game_world
from gameobject import GameObject


class Spawner:
    def __init__(
        self,
        spawn_items: dict[GameObject, int],
        spawn_gap,
        init_pos,
        top_screen,
        bottom_screen,
    ):
        self.spawn_gap = spawn_gap
        self.init_pos = np.array(init_pos)
        self.top_screen = top_screen
        self.bottom_screen = bottom_screen

        # { GameObject_class : max count }
        self.objects = spawn_items

    def spawn_items(self):
        last_spawn_position = self.init_pos

        for game_object_class, count in self.objects.items():
            for _ in range(count):
                last_x = last_spawn_position[0]

                position = last_spawn_position + (
                    random.randint(
                        last_x + self.spawn_gap, last_x + self.spawn_gap + 100
                    ),
                    0,
                )

                game_world.instantiate(
                    game_object_class, self.top_screen, self.bottom_screen, position
                )

                last_spawn_position = np.array(position)
