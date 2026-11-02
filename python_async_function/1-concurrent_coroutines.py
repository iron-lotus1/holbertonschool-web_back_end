#!/usr/bin/env python3
"""
Let's execute multiple coroutines at the same time with async
"""
import asyncio
import heapq

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n, max_delay):
    tasks = [
        asyncio.create_task(wait_random(max_delay))
        for _ in range(n)
    ]

    delays = await asyncio.gather(*tasks)

    return heapq.nsmallest(n, delays)
