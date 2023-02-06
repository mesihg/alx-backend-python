#!/usr/bin/env python3
"""Basics of async module"""
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """Wait for random delay between 0 and max_delay"""
    wait_time = random.random() * max_delay
    await asyncio.sleep(wait_time)
    return wait_time
