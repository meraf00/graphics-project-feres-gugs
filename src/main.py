import pygame
from pygame.locals import *

from consts import *
from background import Background
from player import Player
from player_controller import PlayerController
from game import game_world

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

top_screen = screen.subsurface(0, 0, WIDTH, HEIGHT / 2)
bottom_screen = screen.subsurface(0, HEIGHT / 2, WIDTH, HEIGHT / 2)


player_one_controller = PlayerController(player=PLAYER_1)
player_two_controller = PlayerController(player=PLAYER_2)

game_world.instantiate(Player, top_screen, bottom_screen, player_one_controller)
game_world.instantiate(Player, bottom_screen, top_screen, player_two_controller)


player_one = game_world.game_objects[PLAYER_1]
player_two = game_world.game_objects[PLAYER_2]


top_background = Background(top_screen, player_one)
bottom_background = Background(bottom_screen, player_two)


clock = pygame.time.Clock()


while True:
    time_passed = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                quit()

        for game_object in game_world.game_objects.values():
            game_object.handle_event(event, time_passed)

    top_background.draw()
    bottom_background.draw()

    # for collision detection
    top_rects = []
    bottom_rects = []

    for game_object in list(game_world.game_objects.values()):
        rects = game_object.draw(time_passed)

        # store top rect of player one
        # append bottom rect of player 1 to players two collision check list
        if game_object == player_one:
            player_1_rect = rects[0]
            bottom_rects.append((rects[1], player_one))

        # store bottom rect of plaer two
        # append top rect of player 2 to players 1 collision check list
        elif game_object == player_two:
            player_2_rect = rects[1]
            top_rects.append((rects[0], player_two))

        # store all rect of other game objects on both players collision check list
        else:
            top_rects.append((rects[0], game_object))
            bottom_rects.append((rects[1], game_object))

    # handle collision
    # for player 1
    for i in range(len(top_rects)):
        rect, game_obj = top_rects[i]

        if player_1_rect.colliderect(rect):
            player_one.on_collision(game_obj)

    # handle collision
    # for player 2
    for i in range(len(bottom_rects)):
        rect, game_obj = bottom_rects[i]

        if player_2_rect.colliderect(rect):
            player_two.on_collision(game_obj)

    pygame.display.update()
