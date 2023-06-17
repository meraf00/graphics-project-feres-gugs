import pygame
from pygame.locals import *
from collectables import ShieldCollectable

from consts import *
from background import Background
from player import Player
from player_controller import PlayerController
from world import game_world
from spawner import Spawner


class Game:
    def __init__(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

        self.top_screen = screen.subsurface(0, 0, WIDTH, HEIGHT / 2)
        self.bottom_screen = screen.subsurface(0, HEIGHT / 2, WIDTH, HEIGHT / 2)

        self.player_one_controller = PlayerController(player=PLAYER_1)
        self.player_two_controller = PlayerController(player=PLAYER_2)

        game_world.instantiate(
            Player, self.top_screen, self.bottom_screen, self.player_one_controller
        )
        game_world.instantiate(
            Player, self.bottom_screen, self.top_screen, self.player_two_controller
        )

        self.player_one = game_world.game_objects[PLAYER_1]
        self.player_two = game_world.game_objects[PLAYER_2]

        self.top_background = Background(self.top_screen, self.player_one)
        self.bottom_background = Background(self.bottom_screen, self.player_two)

        collectables = Spawner(
            {
                ShieldCollectable: 10,
            },
            200.0,
            (0.0, 150.0),
            self.top_screen,
            self.bottom_screen,
        )
        collectables.spawn_items()

        self.clock = pygame.time.Clock()

    def mainloop(self):
        game_objects = list(game_world.game_objects.values())

        time_passed = self.clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    from screens import screens

                    screens.go("home")

            for game_object in game_objects:
                game_object.handle_event(event, time_passed)

        self.top_background.draw(time_passed)
        self.bottom_background.draw(time_passed)

        # for collision detection
        top_rects = []
        bottom_rects = []

        for game_object in game_objects:
            rects = game_object.draw(time_passed)

            # store top rect of player one
            # append bottom rect of player 1 to players two collision check list
            if game_object == self.player_one:
                player_1_rect = rects[0]
                bottom_rects.append((rects[1], self.player_one))

            # store bottom rect of plaer two
            # append top rect of player 2 to players 1 collision check list
            elif game_object == self.player_two:
                player_2_rect = rects[1]
                top_rects.append((rects[0], self.player_two))

            # store all rect of other game objects on both players collision check list
            else:
                top_rects.append((rects[0], game_object))
                bottom_rects.append((rects[1], game_object))

        # handle collision
        # for player 1
        for i in range(len(top_rects)):
            rect, game_obj = top_rects[i]

            if player_1_rect.colliderect(rect):
                self.player_one.on_collision(game_obj, time_passed)

        # handle collision
        # for player 2
        for i in range(len(bottom_rects)):
            rect, game_obj = bottom_rects[i]

            if player_2_rect.colliderect(rect):
                self.player_two.on_collision(game_obj, time_passed)
