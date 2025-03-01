"""Coroutines utils for async tasks."""

import asyncio
from collections.abc import Coroutine
from typing import Any, TypeVar

T = TypeVar("T")


async def gather_with_concurrency(
    max_concurrency: int, *coroutines: Coroutine[Any, Any, T]
) -> list[T | BaseException]:
    """Run coroutines with `max_concurrency`."""
    semaphore = asyncio.Semaphore(max_concurrency)

    async def sem_coroutine(coro: Coroutine[Any, Any, Any]) -> Any:
        async with semaphore:
            return await coro

    return await asyncio.gather(
        *(sem_coroutine(c) for c in coroutines), return_exceptions=True
    )
