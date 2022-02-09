
from typing import Callable
from inspect import isfunction
from threading import Thread
from core.aesthetics import *
from time import sleep
import sys


def clear_line():
    # delete the last line
    sys.stdout.write("\x1b[2K")


def clear_lines(total=1):
    for _ in range(total):
        sys.stdout.write("\x1b[1A")  # cursor up one line
        sys.stdout.write("\x1b[2K")  # delete the last line

class SpinnerDots:
    def __init__(self,
        message: str,
        done_message: str = None,
        identifier: str = None,
        color: str = "yellow",
        _function: Callable = None,
        _args=(),
        _kwargs={}
    ) -> None:
        self.identifier = identifier
        self.message = message
        self.done_message = done_message
        self.color = color
        self.frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.len_frames = len(self.frames)
        self.index = 0
        self.completed = False

        if _function and isfunction(_function):
            self._function_thread = Thread(target=_function, args=_args, kwargs=_kwargs)


        # self.state = f"[{green(self.identifier)}] pending ..."


    def animate(self, _sleep: float = 0.1) -> None:
        self.start_thread()

        while self.is_done():
            self.next()
            self.print_state()
            sleep(_sleep)

        clear_line()
        self.done()
        self.print_state(_end="\n")


    def start_thread(self) -> None:
        self._function_thread.start()


    def is_done(self) -> bool:
        return self._function_thread.is_alive()


    def next(self) -> "SpinnerDots":
        if self.completed:
            return self

        self.state = f"{yellow(self.frames[self.index % self.len_frames])} {self.message}"
        # self.state = f"{self.frames[self.index % self.len_frames]} {self.message}"
        self.index += 1
        return self


    def done(self) -> "SpinnerDots":
        if self.done_message:
            self.state = f"{yellow('•')} {self.done_message} {green('✅')}"

        self.completed = True
        return self


    def print_state(self, _end="\r"):
        """
        Function: print_state
        Summary:
            this function must always be run after self.next()
        Examples: InsertHere
        Attributes:
            @param (self):InsertHere
            @param (__end) default="\r": InsertHere
        Returns: InsertHere
        """
        print(self.state, end=_end)


    def get_state(self) -> str:
        return self.state


def worker():
    for _ in range(2):
        sleep(1)

if __name__ == '__main__':
    spinner = SpinnerDots("git clone ...", done_message="done cloning", _function=worker)
    spinner.animate()
    sleep(2)