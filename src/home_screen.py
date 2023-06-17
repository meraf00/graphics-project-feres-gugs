import pygame
from pygame.locals import *

from consts import *


class Home:
    def __init__(self):
        
        self.screen = pygame.display.set_mode((640, 480), 0, 32)

        self.home_image = pygame.image.load("assets/ui/home.png").convert()

        self.font = pygame.font.SysFont("Corbel", 20)

        self.start_game = self.font.render("Start Game", True, WHITE)
        self.quit_game = self.font.render("Exit", True, WHITE)

        self.start_game_hover = self.font.render("Start Game", True, GREEN)
        self.quit_game_hover = self.font.render("Exit", True, RED)

        self.start_rect = (460, 210, 130, 40)
        self.quit_rect = (460, 260, 130, 40)

    def draw_start(self):
        pygame.draw.rect(self.screen, WHITE, (460, 210, 130, 40))
        pygame.draw.rect(self.screen, BROWN, (461, 211, 128, 38))
        self.screen.blit(self.start_game, (480, 220))

    def draw_quit(self):
        pygame.draw.rect(self.screen, WHITE, (460, 260, 130, 40))
        pygame.draw.rect(self.screen, BROWN, (461, 261, 128, 38))
        self.screen.blit(self.quit_game, (510, 270))

    def draw_start_hover(self):
        pygame.draw.rect(self.screen, GREEN, (460, 210, 130, 40))
        pygame.draw.rect(self.screen, BROWN, (461, 211, 128, 38))
        self.screen.blit(self.start_game_hover, (480, 220))

    def draw_quit_hover(self):
        pygame.draw.rect(self.screen, RED, (460, 260, 130, 40))
        pygame.draw.rect(self.screen, BROWN, (461, 261, 128, 38))
        self.screen.blit(self.quit_game_hover, (510, 270))

    def mainloop(self):
        mouse = pygame.mouse.get_pos()

        hover_on_start = pygame.Rect.collidepoint(Rect(self.start_rect), *mouse)
        hover_on_quit = pygame.Rect.collidepoint(Rect(self.quit_rect), *mouse)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()

            if event.type == MOUSEBUTTONDOWN:
                if hover_on_start:
                    from screens import screens

                    print("...")
                    screens.go("game")

                if hover_on_quit:
                    pygame.quit()
                    quit()

        self.screen.blit(self.home_image, (0, 0))

        if hover_on_start:
            self.draw_start_hover()
        else:
            self.draw_start()

        if hover_on_quit:
            self.draw_quit_hover()
        else:
            self.draw_quit()
