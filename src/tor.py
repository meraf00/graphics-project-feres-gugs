import pygame

from gameobject import *
from world import game_world


class Tor(GameObject):
    def __init__(self, id, top_screen, bottom_screen, initial_position: list = None):
        super().__init__(id)

        if initial_position:
            self.position = np.array(initial_position)

        self.top_screen = top_screen

        self.bottom_screen = bottom_screen

        self.speed = np.array((750.0, -100.0))

        self.acceleration = np.array(GRAVITY)

        self.load()

    def draw(self, time_passed):
        # destroy object when it falls of the screen
        if self.position[1] > HEIGHT:
            game_world.dispose(self)

        # calculate projectile
        self.speed += self.acceleration * time_passed
        self.position += self.speed * time_passed

        # rotate image according to speed vector
        angle = np.angle(np.dot(self.speed, [1, -1j]), deg=True)
        frame, rect = self.rotate(self.frame, angle)

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
        path = "assets/spear/spear.png"

        self.frame = pygame.image.load(path).convert_alpha()

        self.height = self.frame.get_height()
        self.width = self.frame.get_width()
