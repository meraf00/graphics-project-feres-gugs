from gameobject import *


class Weapon(GameObject):
    def __init__(self, id: int, player: GameObject) -> None:
        super().__init__(id)

        self.damage_per_second = 0
        self.player = player


class Shield:
    def __init__(self):
        self.max_hitpoint = 10_000
        self.hitpoint = self.max_hitpoint
        self.enable_duration = 1  # second

        self._start_time = None
        self._enabled = False

    def enable(self):
        if not self._enabled:
            self._start_time = pygame.time.get_ticks()
            self._enabled = True

    @property
    def is_enabled(self):
        if self._start_time == None:
            return False

        time_passed = (pygame.time.get_ticks() - self._start_time) / 1000.0

        if time_passed > self.enable_duration:
            self._enabled = False

        return self._enabled

    def __str__(self) -> str:
        return str(self.hitpoint)


class Spear:
    def __init__(self):
        self.count = 3
        self.damage_per_second = 250.0
        self.cool_down_duration = 1  # seconds

        self._start_time = None
        self._thrown = False

    def throw(self):
        if not self._thrown:
            self._start_time = pygame.time.get_ticks()
            self.count -= 1
            self._thrown = True
            return True

        return False

    @property
    def is_thrown(self):
        if self._start_time == None:
            return False

        time_passed = (pygame.time.get_ticks() - self._start_time) / 1000.0

        if time_passed > self.cool_down_duration:
            self._thrown = False

        return self._thrown
