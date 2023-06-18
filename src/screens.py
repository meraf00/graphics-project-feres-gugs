from game_screen import Game
from home_screen import Home


class Screen:
    def __init__(self):
        self.screens = {"home": Home, "game": Game}
        self.current_screen = self.screens["home"]()
        self.current_screen = self.screens["game"]()

    def go(self, screen_name):
        self.current_screen = self.screens[screen_name]()


screens: Screen = Screen()
