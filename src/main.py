import pygame
from pygame.locals import *
import os

pygame.init()

from screens import screens


os.environ["SDL_VIDEO_CENTERED"] = "0"

while True:
    screens.current_screen.mainloop()

    pygame.display.update()
