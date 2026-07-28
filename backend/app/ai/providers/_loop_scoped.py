import asyncio
from collections.abc import Callable
from typing import Generic, TypeVar, cast

T = TypeVar("T")


class LoopScopedValue(Generic[T]):
    def __init__(self, factory: Callable[[], T]):
        self._factory = factory
        self._value: T | None = None
        self._computed = False
        self._loop: asyncio.AbstractEventLoop | None = None

    def get(self) -> T:
        current_loop = asyncio.get_running_loop()
        if not self._computed or self._loop is not current_loop:
            self._value = self._factory()
            self._computed = True
            self._loop = current_loop
        return cast(T, self._value)
