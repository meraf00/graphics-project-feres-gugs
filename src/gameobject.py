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

    def rotate(self, degree: float) -> None:
        self.rotation += degree

    def translate(self, vector: np.array) -> None:
        self.position += vector

    @abstractmethod
    def handle_event(self, event: pygame.event.Event, time_passed: float) -> None:
        ...

    @abstractmethod
    def draw(self, time_passed: float) -> Optional[pygame.Surface]:
        ...


class Animator:
    def __init__(self, frames: list, framerate: int, loop: bool = True) -> None:
        self.framerate = framerate
        self.frames = frames
        self.frame_count = len(frames)
        self.loop = loop

        self._start_time = None
        self._last_frame = frames[0]
        self._playing = False

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
            time_passed = pygame.time.get_ticks() - self._start_time
            time_passed_seconds = time_passed / 1000.0

            frame_idx = int(self.framerate * time_passed_seconds)

            if self.loop:
                frame_idx = frame_idx % self.frame_count

            else:
                frame_idx = max(self.frame_count - 1, frame_idx)

            self._last_frame = self.frames[frame_idx]

            return self.frames[frame_idx]

        else:
            return self._last_frame
