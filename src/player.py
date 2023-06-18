import pygame
from collectables import *

from gameobject import *
from player_controller import PlayerController
from weapons import *
from world import game_world

from stick import *
from tor import Tor


class PlayerState:
    # states
    IDLE = 0
    RUNNING = 1
    HAS_SPEAR = 1 << 1
    SHIELD_ENABLED = 1 << 2

    def __init__(self):
        self.states = {}
        self.current_state: State

    def add(self, state: State):
        self.states[state.id] = state

    def switch_to(self, state_id):
        if self.current_state.is_animated:
            self.current_state.animator.stop()

        self.current_state = self.states[state_id]

        if self.current_state.is_animated:
            self.current_state.animator.play()

    @property
    def shield_enabled(self):
        return self.current_state.id & self.SHIELD_ENABLED

    @property
    def running(self):
        return self.current_state.id & self.RUNNING

    @property
    def has_spear(self):
        return self.current_state.id & self.HAS_SPEAR


class Player(GameObject):
    def __init__(
        self, id, player_screen, opponent_screen, controller: PlayerController
    ):
        super().__init__(id)

        self.player_screen = player_screen
        self.opponent_screen = opponent_screen
        self.controller = controller

        if self.id == PLAYER_1:
            self.top_screen = self.player_screen
            self.bottom_screen = self.opponent_screen

        else:
            self.bottom_screen = self.player_screen
            self.top_screen = self.opponent_screen

        self.max_speed: float = 950.0
        self.speed: float = 0.0
        self.acceleration: float = 400.0
        self.decceleration: float = 200.0

        self.shield: Shield = None
        self.spear: Spear = None
        self.flags: int = 0

        self.states = PlayerState()

        self.clock = pygame.time.Clock()

        self.load()

    def on_collision(self, game_object, time_passed):
        if isinstance(game_object, Weapon) and game_object.player != self:
            if self.states.shield_enabled:
                self.shield.hitpoint -= game_object.damage_per_second * time_passed

            else:
                self.speed -= game_object.damage_per_second * time_passed
                self.speed = max(self.speed, 0)

        if isinstance(game_object, ShieldCollectable):
            if game_object.id in game_world.game_objects:
                if self.shield == None:
                    game_world.dispose(game_object)
                    self.shield = Shield()

        if isinstance(game_object, SpearCollectable):
            if game_object.id in game_world.game_objects:
                if self.spear == None:
                    game_world.dispose(game_object)
                    self.spear = Spear()

        if isinstance(game_object, FlagCollectable):
            if game_object.id in game_world.game_objects:
                self.flags += 1
                game_world.dispose(game_object)

    def handle_movement(self, time_passed):
        keys = pygame.key.get_pressed()

        if keys[self.controller.move_right]:
            self.speed += self.acceleration * time_passed

        if not keys[self.controller.move_right]:
            self.speed -= self.decceleration * time_passed

        if keys[self.controller.move_left]:
            self.speed -= self.acceleration * time_passed

        self.speed = max(self.speed, 0)
        self.speed = min(self.speed, self.max_speed)

    def handle_event(self, event, time_passed) -> None:
        keys = pygame.key.get_pressed()

        self.handle_movement(time_passed)

        if keys[self.controller.attack]:
            game_world.instantiate(
                Stick,
                self.top_screen,
                self.bottom_screen,
                self,
            )

        if keys[self.controller.throw]:
            if self.spear:
                if not self.spear.is_thrown and self.spear.throw():
                    game_world.instantiate(
                        Tor,
                        self.top_screen,
                        self.bottom_screen,
                        self,
                        np.array(self.position),
                    )

        if keys[self.controller.enable_shield]:
            if self.shield:
                self.shield.enable()

    def update_state(self, time_passed):
        state_id = 0

        if self.speed == 0:
            state_id &= ~PlayerState.RUNNING

        else:
            state_id |= PlayerState.RUNNING

        if self.shield and self.shield.is_enabled:
            state_id |= PlayerState.SHIELD_ENABLED

        else:
            state_id &= ~PlayerState.SHIELD_ENABLED

        if self.shield and self.shield.hitpoint <= 0:
            self.shield = None
            state_id &= ~PlayerState.SHIELD_ENABLED

        if self.spear:
            # update thrown state
            self.spear.is_thrown
            state_id |= PlayerState.HAS_SPEAR

        else:
            state_id &= ~PlayerState.HAS_SPEAR

        if self.spear and self.spear.count <= 0:
            self.spear = None
            state_id &= ~PlayerState.HAS_SPEAR

        self.states.switch_to(state_id)

        self.handle_movement(time_passed)

    def draw(self, time_passed):
        self.update_state(time_passed)

        frame = self.states.current_state.get_frame()

        self.position += np.array(self.direction) * time_passed * self.speed

        # on players screen center horse
        screen_center = (
            self.player_screen.get_width() / 2 - frame.get_width() / 2,
            self.player_screen.get_height() - frame.get_height(),
        )

        rect_on_self_window = self.player_screen.blit(frame, screen_center)

        opponent_id = PLAYER_1 if self.id == PLAYER_2 else PLAYER_2

        opponent = game_world.game_objects[opponent_id]

        rect_on_opponent_window = self.opponent_screen.blit(
            frame,
            self.position
            - opponent.position
            + (
                self.opponent_screen.get_width() / 2 - frame.get_width() / 2,
                self.opponent_screen.get_height() - frame.get_height(),
            ),
        )

        # returns objects rect on top, bottom screen
        # my_rect is rect on this players screen
        # other rect is rect on opponent playsers screen
        if self.id == PLAYER_1:
            return rect_on_self_window, rect_on_opponent_window

        return rect_on_opponent_window, rect_on_self_window

    # =======================================================================================
    #                                       Load Assets
    # =======================================================================================
    def load(self):
        self._load_idle()
        self._load_idle_with_spear()
        self._load_idle_with_shield()
        self._load_idle_with_spear_shield()
        self._load_running()
        self._load_running_with_shield()
        self._load_running_with_spear()
        self._load_running_with_spear_shield()

    def _load_idle(self):
        path = "assets/horse/horse-idle.png"
        image = pygame.image.load(path).convert_alpha()

        state_id = PlayerState.IDLE

        state = State(state_id, [image])

        self.states.add(state)

        self.states.current_state = state

    def _load_idle_with_spear(self):
        path = "assets/horse/horse-idle-with-spear.png"
        image = pygame.image.load(path).convert_alpha()

        state_id = PlayerState.IDLE | PlayerState.HAS_SPEAR
        state = State(state_id, [image])

        self.states.add(state)

    def _load_idle_with_shield(self):
        path = "assets/horse/horse-idle-sheild.png"
        image = pygame.image.load(path).convert_alpha()

        state_id = PlayerState.IDLE | PlayerState.SHIELD_ENABLED
        state = State(state_id, [image])

        self.states.add(state)

    def _load_idle_with_spear_shield(self):
        path = "assets/horse/horse-idle-with-spear-sheild.png"
        image = pygame.image.load(path).convert_alpha()

        state_id = PlayerState.IDLE | PlayerState.HAS_SPEAR | PlayerState.SHIELD_ENABLED
        state = State(state_id, [image])

        self.states.add(state)

    def _load_running(self):
        path = "assets/horse/horse-running.png"
        image = pygame.image.load(path).convert_alpha()

        n_frames = 14
        width = image.get_width() // n_frames
        height = image.get_height()

        frames = []

        for i in range(n_frames):
            frame = image.subsurface(i * width, 0, width, height)
            frame = frame.subsurface(15, 0, width - 15, height)

            frames.append(frame)

        animator = Animator(frames, 20)

        state_id = PlayerState.RUNNING
        state = State(state_id, frames, animator)

        self.states.add(state)

    def _load_running_with_shield(self):
        path = "assets/horse/horse-running-sheild.png"
        image = pygame.image.load(path).convert_alpha()

        n_frames = 14
        width = image.get_width() // n_frames
        height = image.get_height()

        frames = []

        for i in range(n_frames):
            frame = image.subsurface(i * width, 0, width, height)
            frame = frame.subsurface(15, 0, width - 15, height)

            frames.append(frame)

        animator = Animator(frames, 20)

        state_id = PlayerState.RUNNING | PlayerState.SHIELD_ENABLED
        state = State(state_id, frames, animator)

        self.states.add(state)

    def _load_running_with_spear(self):
        path = "assets/horse/horse-running-with-spear.png"
        image = pygame.image.load(path).convert_alpha()

        n_frames = 14
        width = image.get_width() // n_frames
        height = image.get_height()

        frames = []

        for i in range(n_frames):
            frame = image.subsurface(i * width, 0, width, height)
            frame = frame.subsurface(15, 0, width - 15, height - 10)

            frames.append(frame)

        animator = Animator(frames, 20)

        state_id = PlayerState.RUNNING | PlayerState.HAS_SPEAR

        state = State(state_id, frames, animator)

        self.states.add(state)

    def _load_running_with_spear_shield(self):
        path = "assets/horse/horse-running-with-spear-sheild.png"
        image = pygame.image.load(path).convert_alpha()

        n_frames = 14
        width = image.get_width() // n_frames
        height = image.get_height()

        frames = []

        for i in range(n_frames):
            frame = image.subsurface(i * width, 0, width, height)
            frame = frame.subsurface(15, 0, width - 15, height - 10)

            frames.append(frame)

        animator = Animator(frames, 20)

        state_id = (
            PlayerState.RUNNING | PlayerState.HAS_SPEAR | PlayerState.SHIELD_ENABLED
        )

        state = State(state_id, frames, animator)

        self.states.add(state)
