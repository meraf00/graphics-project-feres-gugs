import pygame
import numpy as np
from consts import *
from typing import Optional
from abc import ABC, abstractmethod


class GameObject(ABC):
    def __init__(self, id: int) -> None:
        self.id = id
        self.position = np.array((0.0, 0.0))
        self.direction = LEFT

    def rotate(
        self, frame: pygame.Surface, degrees: float
    ) -> tuple[pygame.Surface, pygame.Rect]:
        rot_image = pygame.transform.rotate(frame, degrees)
        rot_rect = rot_image.get_rect(center=frame.get_rect().center)
        return rot_image, rot_rect

    def translate(self, vector: np.array) -> None:
        self.position += vector

    def handle_event(self, event: pygame.event.Event, time_passed: float) -> None:
        ...

    @abstractmethod
    def draw(self, time_passed: float) -> Optional[pygame.Surface]:
        ...

    def __eq__(self, value: object) -> bool:
        return self.id == value.id

    def __hash__(self) -> int:
        return hash(self.id)


class Animator:
    def __init__(self, frames: list, framerate: int, loop: bool = True) -> None:
        self.framerate = framerate
        self.frames = frames
        self.frame_count = len(frames)
        self.loop = loop

        self.speed = 1

        self._start_time = None
        self._last_frame = frames[0]
        self._playing = False

    @property
    def is_playing(self):
        return self._playing

    def start(self) -> None:
        self._start_time = pygame.time.get_ticks()
        self._playing = True

    def stop(self) -> None:
        self._playing = False
        self._last_frame = self.frames[0]

    def pause(self) -> None:
        self._playing = False

    def play(self) -> None:
        if self._start_time == None:
            self.start()

        self._playing = True

    def get_frame(self) -> pygame.Surface:
        if self._playing:
            time_passed = (pygame.time.get_ticks() - self._start_time) * self.speed
            time_passed_seconds = time_passed / 1000.0

            frame_idx = int(self.framerate * time_passed_seconds)

            if self.loop:
                frame_idx = frame_idx % self.frame_count

            else:
                if frame_idx > self.frame_count:
                    self.stop()

                frame_idx = min(self.frame_count - 1, frame_idx)

            self._last_frame = self.frames[frame_idx]

            return self.frames[frame_idx]

        else:
            return self._last_frame


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

