from pygame.locals import *

from consts import PLAYER_1


class PlayerController:
    def __init__(self, player):
        if player == PLAYER_1:
            self.move_left = K_a
            self.move_right = K_d
            self.enable_sheild = K_s
            self.attack = K_w

        else:
            self.move_left = K_j
            self.move_right = K_l
            self.enable_sheild = K_k
            self.attack = K_i