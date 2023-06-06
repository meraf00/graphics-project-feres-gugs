import pygame

from gameobject import *
from game import game_world


class State:
    def __init__(
        self, id: int, frames: list[pygame.Surface], animator: Animator = None
    ):
        self.id = id
        self.animator = animator
        self.frames = frames

    @property
    def is_animated(self) -> bool:
        return self.animator != None

    def get_frame(self) -> pygame.Surface:
        if self.animator:
            return self.animator.get_frame()

        return self.frames[0]

    def __eq__(self, other: "State"):
        return other.id == self.id

    def __hash__(self) -> int:
        return self.id


class PlayerState:
    # states
    IDLE = 0
    RUNNING = 1
    HAS_WEAPON = 1 << 1
    SHEILD_ENABLED = 1 << 2

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


class Player(GameObject):
    def __init__(self, id, player_screen, opponent_screen, controller):
        super().__init__(id)

        self.player_screen = player_screen
        self.opponent_screen = opponent_screen
        self.controller = controller

        self.max_speed: float = 550.0
        self.speed: float = 0.0
        self.acceleration: float = 200.0

        self.health: float = 25000.0

        self.states = PlayerState()

        self.clock = pygame.time.Clock()

        self.load()

    def on_collision(self, *args):
        ...

    def handle_movement(self, keys, time_passed):
        if keys[self.controller.move_right]:
            self.speed += self.acceleration * time_passed

        if keys[self.controller.move_left]:
            self.speed -= self.acceleration * time_passed

        self.speed = max(self.speed, 0)
        self.speed = min(self.speed, self.max_speed)

    def handle_event(self, event, time_passed) -> None:
        keys = pygame.key.get_pressed()

        self.handle_movement(keys, time_passed)

    def update_state(self):
        if self.speed == 0:
            self.states.switch_to(PlayerState.IDLE)

        else:
            self.states.switch_to(PlayerState.RUNNING)

    def draw(self, time_passed):
        self.update_state()

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
        self._load_idle_with_sheild()
        self._load_idle_with_spear_sheild()
        self._load_running()
        self._load_running_with_sheild()
        self._load_running_with_spear()
        self._load_running_with_spear_sheild()

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

        state_id = PlayerState.IDLE | PlayerState.HAS_WEAPON
        state = State(state_id, [image])

        self.states.add(state)

    def _load_idle_with_sheild(self):
        path = "assets/horse/horse-idle-sheild.png"
        image = pygame.image.load(path).convert_alpha()

        state_id = PlayerState.IDLE | PlayerState.SHEILD_ENABLED
        state = State(state_id, [image])

        self.states.add(state)

    def _load_idle_with_spear_sheild(self):
        path = "assets/horse/horse-idle-with-spear-sheild.png"
        image = pygame.image.load(path).convert_alpha()

        state_id = (
            PlayerState.IDLE | PlayerState.HAS_WEAPON | PlayerState.SHEILD_ENABLED
        )
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

    def _load_running_with_sheild(self):
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

        state_id = PlayerState.RUNNING | PlayerState.SHEILD_ENABLED
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

        state_id = PlayerState.RUNNING | PlayerState.HAS_WEAPON

        state = State(state_id, frames, animator)

        self.states.add(state)

    def _load_running_with_spear_sheild(self):
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
            PlayerState.RUNNING | PlayerState.HAS_WEAPON | PlayerState.SHEILD_ENABLED
        )

        state = State(state_id, frames, animator)

        self.states.add(state)
