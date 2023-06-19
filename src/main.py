import pygame
from pygame.locals import *
import os

from pygame import mixer

pygame.init()

mixer.init()

from sounds import Sounds

from screens import screens

os.environ["SDL_VIDEO_CENTERED"] = "0"


# background

mixer.Channel(0).play(Sounds.background, -1)
mixer.Channel(0).set_volume(0.1)


while True:
    screens.current_screen.mainloop()

    pygame.display.update()
