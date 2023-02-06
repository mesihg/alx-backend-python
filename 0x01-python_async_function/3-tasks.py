#!/usr/bin/env python3
"""Non async function module"""
import asyncio


wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """Returns an asynchronous task without async function"""
    return asyncio.create_task(wait_random(max_delay))
