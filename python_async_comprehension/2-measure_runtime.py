#!/usr/bin/env python3
"""
Module that measures the total execution time for running async_comprehension
four times concurrently using asyncio.gather.
"""
import asyncio
import time

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
    Execute async_comprehension four times concurrently using asyncio.gather,
    measure the total elapsed time, and return it.
    """
    start_time = time.perf_counter()
    await asyncio.gather(*(async_comprehension() for _ in range(4)))
    end_time = time.perf_counter()
    return end_time - start_time
