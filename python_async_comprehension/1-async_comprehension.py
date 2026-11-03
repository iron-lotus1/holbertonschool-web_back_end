#!/usr/bin/env python3
"""
Module that contains a coroutine to collect numbers from an async generator.
"""
from typing import List

async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    """
    Collect 10 random numbers using an async comprehension over
    async_generator and return the resulting list of numbers.
    """
    return [i async for i in async_generator()]
